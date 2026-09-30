from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import String, cast, func
from app.models import Pago, Usuario, Estudiante, Profesor


class PagoService:

    @staticmethod
    def get_all(db: Session, search_text: str = "", metodo_filtro: str = "todos") -> List[Pago]:
        """Obtiene el historial de pagos con filtros aplicados."""
        query = db.query(Pago).options(
            joinedload(Pago.usuario),
            joinedload(Pago.reserva)
        )

        if metodo_filtro and metodo_filtro != "todos":
            query = query.filter(Pago.metodo == metodo_filtro)

        if search_text.strip():
            patron = f"%{search_text.strip()}%"
            query = query.join(Usuario, isouter=True).filter(
                (cast(Pago.id_pago, String).ilike(patron)) |
                (cast(Pago.id_reserva, String).ilike(patron)) |
                (Usuario.email.ilike(patron)) |
                (Pago.correo.ilike(patron))
            )

        return query.order_by(Pago.fecha_pago.desc()).all()

    @staticmethod
    def get_kpis(db: Session) -> Dict[str, Any]:
        """Calcula agregados y estadísticas de los pagos para el panel."""
        ingresos_completados = db.query(func.sum(Pago.monto)).filter(Pago.estado == "completado").scalar() or 0.0
        ingresos_pendientes = db.query(func.sum(Pago.monto)).filter(Pago.estado == "pendiente").scalar() or 0.0
        total_operaciones = db.query(func.count(Pago.id_pago)).scalar() or 0
        tui_bonos = db.query(func.count(Pago.id_pago)).filter(Pago.metodo.in_(["tui", "bono"])).scalar() or 0
        visitantes = db.query(func.count(Pago.id_pago)).filter(Pago.id_usuario == 0).scalar() or 0

        return {
            "total_ingresos": float(ingresos_completados),
            "ingresos_pendientes": float(ingresos_pendientes),
            "total_operaciones": int(total_operaciones),
            "tui_bonos": int(tui_bonos),
            "visitantes": int(visitantes),
        }

    @staticmethod
    def cambiar_estado(db: Session, id_pago: int, nuevo_estado: str) -> Optional[Pago]:
        """Actualiza el estado de un pago en la base de datos."""
        pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
        if pago:
            pago.estado = nuevo_estado
            db.commit()
            db.refresh(pago)
        return pago

    @staticmethod
    def recargar_saldo_usuario(db: Session, user_id: int, monto: float, metodo: str = "tarjeta") -> bool:
        """Añade saldo al estudiante o profesor y registra el pago correspondiente."""
        est = db.query(Estudiante).filter(Estudiante.id_usuario == user_id).first()
        if est:
            est.saldo = float(est.saldo or 0.0) + monto
        else:
            prof = db.query(Profesor).filter(Profesor.id_usuario == user_id).first()
            if prof:
                prof.saldo = float(prof.saldo or 0.0) + monto
            else:
                return False

        # Registrar la transacción
        nuevo_pago = Pago(
            id_usuario=user_id,
            monto=monto,
            metodo=metodo,
            fecha_pago=datetime.now(),
            estado="completado"
        )
        db.add(nuevo_pago)
        db.commit()
        return True