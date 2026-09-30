from datetime import date
from typing import Optional
from sqlalchemy import String, or_
from sqlalchemy.orm import Session, joinedload
from app.models import Reserva, Usuario, Menu


class PedidoService:

    @staticmethod
    def get_pedidos_comedor(
        db: Session,
        fecha: Optional[date] = None,
        search_text: str = "",
        estado_filtro: str = "todos"
    ):
        """Obtiene las reservas/pedidos junto con el usuario y datos asociados."""
        query = (
            db.query(Reserva)
            .options(
                joinedload(Reserva.usuario),
                joinedload(Reserva.menu)
            )
        )

        if fecha:
            query = query.filter(Reserva.fecha_reserva >= fecha)

        if estado_filtro == "pendientes":
            query = query.filter(Reserva.estado == "confirmada", Reserva.estado_bit == 0)
        elif estado_filtro == "recogidos":
            query = query.filter(or_(Reserva.estado == "recogida", Reserva.estado_bit == 1))
        elif estado_filtro == "cancelados":
            query = query.filter(Reserva.estado == "cancelada")

        if search_text.strip():
            pattern = f"%{search_text.strip()}%"
            query = query.join(Usuario).filter(
                (Usuario.email.ilike(pattern)) |
                (Reserva.id_reserva.cast(String).ilike(pattern))
            )

        return query.order_by(Reserva.fecha_reserva.desc()).all()

    @staticmethod
    def get_platos_por_reserva(reserva: Reserva) -> list[str]:
        """Obtiene de forma estricta los platos elegidos en la comanda."""
        # 1. Si la reserva tiene asignados platos específicamente
        if hasattr(reserva, "platos") and reserva.platos:
            return [p.nombre for p in reserva.platos if hasattr(p, "nombre")]
            
        # 2. Si la reserva los guarda en tabla intermedia (reserva_platos)
        if hasattr(reserva, "reserva_platos") and reserva.reserva_platos:
            platos_encontrados = []
            for rp in reserva.reserva_platos:
                if hasattr(rp, "plato") and rp.plato:
                    platos_encontrados.append(rp.plato.nombre)
            if platos_encontrados:
                return platos_encontrados

        # 3. Muestra el identificador del menú asignado si no hay platos personalizados guardados
        return [f"Menú #{reserva.id_menu} Standard"]

    @staticmethod
    def actualizar_estado_pedido(db: Session, id_reserva: int, nuevo_estado: str) -> bool:
        """Actualiza el estado textual y el bit de estado de la reserva."""
        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
        if not reserva:
            return False

        if nuevo_estado == "recogida":
            reserva.estado = "recogida"
            reserva.estado_bit = True
        elif nuevo_estado == "cancelada":
            reserva.estado = "cancelada"
            reserva.estado_bit = False
        elif nuevo_estado == "confirmada":
            reserva.estado = "confirmada"
            reserva.estado_bit = False

        db.commit()
        return True