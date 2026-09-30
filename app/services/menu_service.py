from datetime import date
from typing import Optional
from sqlalchemy import String, func
from sqlalchemy.orm import Session, joinedload
from app.models import Menu, Reserva


class MenuService:

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Menu)
            .options(joinedload(Menu.platos))
            .order_by(Menu.fecha.desc())
            .all()
        )

    @staticmethod
    def search(db: Session, text: str):
        query = (
            db.query(Menu)
            .options(joinedload(Menu.platos))
        )

        if text.strip():
            pattern = f"%{text.strip()}%"
            query = query.filter(
                (Menu.tipo.ilike(pattern))
                | (Menu.fecha.cast(String).ilike(pattern))
            )

        return (
            query.order_by(Menu.fecha.desc())
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        id_menu: int,
    ):
        return (
            db.query(Menu)
            .options(joinedload(Menu.platos))
            .filter(Menu.id_menu == id_menu)
            .first()
        )

    @staticmethod
    def get_menu_del_dia(db: Session, fecha_consulta: Optional[date] = None) -> Optional[Menu]:
        """Obtiene el menú disponible para una fecha específica (por defecto la fecha actual)."""
        target_date = fecha_consulta or date.today()
        return (
            db.query(Menu)
            .options(joinedload(Menu.platos))
            .filter(Menu.fecha == target_date, Menu.disponible == True)
            .first()
        )

    @staticmethod
    def count_reservas_dia(db: Session, target_date: Optional[date] = None) -> int:
        """Cuenta las reservas confirmadas asociadas a menús de una fecha."""
        fecha_val = target_date or date.today()
        return (
            db.query(func.count(Reserva.id_reserva))
            .join(Menu, Reserva.id_menu == Menu.id_menu)
            .filter(Menu.fecha == fecha_val, Reserva.estado == "confirmada")
            .scalar() or 0
        )

    @staticmethod
    def create(
        db: Session,
        fecha: date,
        tipo: str,
        max_reservas: int,
        disponible: bool,
    ):
        menu = Menu(
            fecha=fecha,
            tipo=tipo,
            max_reservas=max_reservas,
            disponible=disponible,
        )

        db.add(menu)
        db.commit()
        db.refresh(menu)

        return menu

    @staticmethod
    def update(
        db: Session,
        id_menu: int,
        fecha: date,
        tipo: str,
        max_reservas: int,
        disponible: bool,
    ):
        menu = (
            db.query(Menu)
            .filter(Menu.id_menu == id_menu)
            .first()
        )

        if not menu:
            return None

        menu.fecha = fecha
        menu.tipo = tipo
        menu.max_reservas = max_reservas
        menu.disponible = disponible

        db.commit()

        return menu

    @staticmethod
    def delete(
        db: Session,
        id_menu: int,
    ):
        menu = (
            db.query(Menu)
            .filter(Menu.id_menu == id_menu)
            .first()
        )

        if not menu:
            return False

        db.delete(menu)
        db.commit()

        return True