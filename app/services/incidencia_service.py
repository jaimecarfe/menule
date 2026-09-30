from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from sqlalchemy.orm import Session, joinedload
from app.models import Incidencia, Usuario
from app.utils.email_utils import enviar_correo


class IncidenciaService:

    @staticmethod
    def get_all(
        db: Session,
        search_text: str = "",
        estado_filtro: str = "todos",
        user_role: str = "administrador",
        user_id: Optional[int] = None
    ) -> List[Incidencia]:
        """Obtiene las incidencias con información del usuario y filtrado según el rol y/o ID de usuario."""
        query = db.query(Incidencia).options(joinedload(Incidencia.usuario))

        # Si es un estudiante o profesor, únicamente visualiza sus propios reportes
        if user_role.lower() in ["estudiante", "profesor"] and user_id is not None:
            query = query.filter(Incidencia.id_usuario == user_id)
        # Si el rol es personal_comedor, solo visualiza las incidencias destinadas a cocina
        elif user_role.lower() == "personal_comedor":
            query = query.filter(Incidencia.destino == "cocina")

        if estado_filtro and estado_filtro != "todos":
            query = query.filter(Incidencia.estado == estado_filtro)

        if search_text.strip():
            patron = f"%{search_text.strip()}%"
            query = query.join(Usuario, isouter=True).filter(
                (Incidencia.titulo.ilike(patron)) |
                (Incidencia.numero_seguimiento.ilike(patron)) |
                (Usuario.email.ilike(patron))
            )

        return query.order_by(Incidencia.fecha_reporte.desc()).all()

    @staticmethod
    def get_kpis(db: Session, user_role: str = "administrador", user_id: Optional[int] = None) -> Dict[str, Any]:
        """Obtiene métricas clave filtrando por el rol del usuario actual."""
        base_query = db.query(Incidencia)
        
        if user_role.lower() in ["estudiante", "profesor"] and user_id is not None:
            base_query = base_query.filter(Incidencia.id_usuario == user_id)
        elif user_role.lower() == "personal_comedor":
            base_query = base_query.filter(Incidencia.destino == "cocina")

        total = base_query.count()
        abiertas = base_query.filter(Incidencia.estado == "abierta").count()
        en_proceso = base_query.filter(Incidencia.estado == "en_proceso").count()
        resueltas = base_query.filter(Incidencia.estado == "resuelta").count()

        return {
            "total": total,
            "abiertas": abiertas,
            "en_proceso": en_proceso,
            "resueltas": resueltas,
            "por_rol": {}
        }

    @staticmethod
    def crear(
        db: Session,
        id_usuario: int,
        titulo: str,
        descripcion: str,
        destino: str
    ) -> Incidencia:
        """Crea una nueva incidencia para el usuario autenticado."""
        numero_seguimiento = f"INC-{uuid.uuid4().hex[:8].upper()}"

        nueva_incidencia = Incidencia(
            id_usuario=id_usuario,
            titulo=titulo,
            descripcion=descripcion,
            destino=destino,
            numero_seguimiento=numero_seguimiento,
            estado="abierta",
            prioridad="media",
            fecha_reporte=datetime.now()
        )

        db.add(nueva_incidencia)
        db.commit()
        db.refresh(nueva_incidencia)

        return nueva_incidencia

    @staticmethod
    def responder(db: Session, id_incidencia: int, respuesta: str, id_admin: Optional[int] = None) -> Optional[Incidencia]:
        """Guarda la respuesta del personal/admin y envía el correo electrónico."""
        incidencia = db.query(Incidencia).options(joinedload(Incidencia.usuario)).filter(Incidencia.id_incidencia == id_incidencia).first()
        if not incidencia:
            return None

        incidencia.solucion = respuesta
        incidencia.estado = "resuelta"
        incidencia.fecha_resolucion = datetime.now()
        if id_admin:
            incidencia.id_responsable = id_admin

        db.commit()
        db.refresh(incidencia)

        correo_destino = incidencia.usuario.email if incidencia.usuario else None
        if correo_destino:
            asunto = f"Tu incidencia '{incidencia.titulo}' ha sido resuelta"
            cuerpo = (
                f"¡Hola!\n\n"
                f"Tu incidencia ha sido resuelta:\n\n"
                f"Título: {incidencia.titulo}\n"
                f"Número de seguimiento: {incidencia.numero_seguimiento}\n"
                f"Respuesta: {respuesta}\n\n"
                f"Gracias por contactar con MenULE.\n"
            )
            try:
                enviar_correo(correo_destino, asunto, cuerpo)
            except Exception as e:
                print(f"Error al enviar email de respuesta: {e}")

        return incidencia

    @staticmethod
    def cambiar_estado(db: Session, id_incidencia: int, nuevo_estado: str):
        """Actualiza el estado de la incidencia (ej. 'en_proceso', 'resuelta')."""
        incidencia = db.query(Incidencia).filter(Incidencia.id_incidencia == id_incidencia).first()
        if incidencia:
            incidencia.estado = nuevo_estado
            db.commit()