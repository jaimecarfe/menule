from datetime import date
from typing import Any
import traceback

from sqlalchemy.orm import joinedload

from app.database import SessionLocal
from app.models import (
    Usuario,
    Menu,
    Reserva,
    Incidencia,
)


class HomeService:

    @staticmethod
    def get_dashboard_stats() -> dict[str, int]:
        """Obtiene las estadísticas principales del dashboard."""
        db = SessionLocal()

        try:
            total_users = db.query(Usuario).count()
            total_menus = db.query(Menu).count()
            total_reservations = db.query(Reserva).count()
            total_incidents = db.query(Incidencia).count()

            return {
                "total_users": int(total_users or 0),
                "total_menus": int(total_menus or 0),
                "total_reservations": int(total_reservations or 0),
                "total_incidents": int(total_incidents or 0),
            }
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            traceback.print_exc()
            return {
                "total_users": 0,
                "total_menus": 0,
                "total_reservations": 0,
                "total_incidents": 0,
            }
        finally:
            db.close()

    @staticmethod
    def get_upcoming_menus() -> list[dict[str, Any]]:
        """Obtiene los próximos menús programados."""
        db = SessionLocal()

        try:

            menus = (
                db.query(Menu)
                .options(joinedload(Menu.platos))
                .filter(Menu.fecha >= date.today())
                .order_by(Menu.fecha.asc())
                .limit(5)
                .all()
            )


            resultado = []

            for menu in menus:
                nombres_platos = [
                    plato.nombre for plato in menu.platos
                ] if hasattr(menu, "platos") and menu.platos else []

                resultado.append(
                    {
                        "fecha": menu.fecha.strftime("%d/%m/%Y") if menu.fecha else "",
                        "servicio": menu.tipo.capitalize() if menu.tipo else "Servicio",
                        "principal": " + ".join(nombres_platos) if nombres_platos else "Sin platos asignados",
                        "estado": "Disponible" if getattr(menu, "disponible", True) else "Completo",
                        "badge_color": "green" if getattr(menu, "disponible", True) else "red",
                    }
                )

            return resultado
        except Exception as e:
            print(f"Error al obtener menús: {e}")
            traceback.print_exc()
            return []
        finally:
            db.close()