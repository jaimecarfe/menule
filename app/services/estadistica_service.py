from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from app.models import Pago, Incidencia, Usuario


class EstadisticaService:

    @staticmethod
    def obtener_pagos_por_rol(db: Session) -> List[Dict[str, Any]]:
        """Agrupa ingresos totales y conteo de pagos según el 'tipo' de usuario."""
        resultados = (
            db.query(
                func.coalesce(Usuario.tipo, "visitante").label("rol"),
                func.coalesce(func.sum(Pago.monto), 0.0).label("total_pagado"),
                func.count(Pago.id_pago).label("cantidad_pagos")
            )
            .outerjoin(Usuario, Pago.id_usuario == Usuario.id_usuario)
            .group_by(Usuario.tipo)
            .all()
        )

        return [
            {
                "rol": str(row.rol).replace("_", " ").capitalize(),
                "total_pagado": float(row.total_pagado),
                "cantidad_pagos": int(row.cantidad_pagos)
            }
            for row in resultados
        ]

    @staticmethod
    def obtener_incidencias_por_rol(db: Session) -> List[Dict[str, Any]]:
        """Agrupa el número de incidencias reportadas según el 'tipo' de usuario."""
        resultados = (
            db.query(
                func.coalesce(Usuario.tipo, "visitante").label("rol"),
                func.count(Incidencia.id_incidencia).label("cantidad_incidencias")
            )
            .outerjoin(Usuario, Incidencia.id_usuario == Usuario.id_usuario)
            .group_by(Usuario.tipo)
            .all()
        )

        return [
            {
                "rol": str(row.rol).replace("_", " ").capitalize(),
                "cantidad_incidencias": int(row.cantidad_incidencias)
            }
            for row in resultados
        ]

    @staticmethod
    def obtener_estadisticas_diarias(db: Session) -> List[Dict[str, Any]]:
        """Consulta la vista SQL 'VistaEstadisticasDiarias'."""
        query = text("""
            SELECT fecha, total_reservas, ingresos 
            FROM VistaEstadisticasDiarias 
            ORDER BY fecha ASC 
            LIMIT 30
        """)
        
        try:
            resultados = db.execute(query).fetchall()
            return [
                {
                    "fecha": str(row.fecha),
                    "total_reservas": int(row.total_reservas or 0),
                    "ingresos": float(row.ingresos or 0.0)
                }
                for row in resultados
            ]
        except Exception as e:
            print(f"Nota/Aviso con VistaEstadisticasDiarias: {e}")
            return []