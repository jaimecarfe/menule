from sqlalchemy import String
from sqlalchemy.orm import Session, joinedload

from app.models import Menu, Plato


class PlatoService:

    # ==========================================
    # OBTENER TODOS
    # ==========================================
    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Plato)
            .options(joinedload(Plato.menus))
            .order_by(Plato.nombre.asc())
            .all()
        )

    # ==========================================
    # BUSCAR
    # ==========================================
    @staticmethod
    def search(
        db: Session,
        text: str,
    ):
        query = db.query(Plato).options(joinedload(Plato.menus))

        if text.strip():
            pattern = f"%{text.strip()}%"
            query = query.filter(
                (Plato.nombre.ilike(pattern))
                | (Plato.tipo.ilike(pattern))
                | (Plato.alergenos.cast(String).ilike(pattern))
            )

        return query.order_by(Plato.nombre.asc()).all()

    # ==========================================
    # OBTENER POR ID
    # ==========================================
    @staticmethod
    def get_by_id(
        db: Session,
        id_plato: int,
    ):
        return (
            db.query(Plato)
            .options(joinedload(Plato.menus))
            .filter(Plato.id_plato == id_plato)
            .first()
        )

    # ==========================================
    # CREAR
    # ==========================================
    @staticmethod
    def create(
        db: Session,
        nombre: str,
        tipo: str,
        alergenos: str,
        activo: bool = True,
    ):
        plato = Plato(
            nombre=nombre.strip(),
            tipo=tipo,
            alergenos=alergenos.strip() if alergenos else "Ninguno",
            activo=activo,
        )

        db.add(plato)
        db.commit()
        db.refresh(plato)

        return plato

    # ==========================================
    # EDITAR (ACTUALIZADO: Acepta y guarda el campo 'activo')
    # ==========================================
    @staticmethod
    def update(
        db: Session,
        id_plato: int,
        nombre: str,
        tipo: str,
        alergenos: str,
        activo: bool = True,
    ):
        plato = (
            db.query(Plato)
            .filter(Plato.id_plato == id_plato)
            .first()
        )

        if plato is None:
            return None

        plato.nombre = nombre.strip()
        plato.tipo = tipo
        plato.alergenos = (
            alergenos.strip()
            if alergenos
            else "Ninguno"
        )
        plato.activo = activo  # 👈 CORREGIDO: Se persiste la desactivación

        db.commit()
        db.refresh(plato)

        return plato

    # ==========================================
    # ELIMINAR
    # ==========================================
    @staticmethod
    def delete(
        db: Session,
        id_plato: int,
    ):
        plato = (
            db.query(Plato)
            .options(joinedload(Plato.menus))
            .filter(Plato.id_plato == id_plato)
            .first()
        )

        if plato is None:
            return False

        plato.menus.clear()
        db.delete(plato)
        db.commit()

        return True

    # ==========================================
    # MENÚS DEL PLATO
    # ==========================================
    @staticmethod
    def get_menus(
        db: Session,
        id_plato: int,
    ):
        plato = (
            db.query(Plato)
            .options(joinedload(Plato.menus))
            .filter(Plato.id_plato == id_plato)
            .first()
        )

        if plato is None:
            return []

        return plato.menus

    # ==========================================
    # PLATOS DE UN MENÚ
    # ==========================================
    @staticmethod
    def get_by_menu(
        db: Session,
        id_menu: int,
    ):
        menu = (
            db.query(Menu)
            .options(joinedload(Menu.platos))
            .filter(Menu.id_menu == id_menu)
            .first()
        )

        if menu is None:
            return []

        return menu.platos

    # ==========================================
    # AÑADIR PLATO A MENÚ
    # ==========================================
    @staticmethod
    def add_to_menu(
        db: Session,
        id_menu: int,
        id_plato: int,
    ):
        menu = (
            db.query(Menu)
            .options(joinedload(Menu.platos))
            .filter(Menu.id_menu == id_menu)
            .first()
        )

        plato = (
            db.query(Plato)
            .filter(Plato.id_plato == id_plato)
            .first()
        )

        if menu is None or plato is None:
            return False

        if plato not in menu.platos:
            menu.platos.append(plato)

        db.commit()

        return True

    # ==========================================
    # CREAR Y AÑADIR A MENÚ
    # ==========================================
    @staticmethod
    def create_and_add_to_menu(
        db: Session,
        id_menu: int,
        nombre: str,
        tipo: str,
        alergenos: str,
    ):
        plato = PlatoService.create(
            db=db,
            nombre=nombre,
            tipo=tipo,
            alergenos=alergenos,
            activo=True,
        )

        PlatoService.add_to_menu(
            db,
            id_menu,
            plato.id_plato,
        )

        return plato

    # ==========================================
    # QUITAR DE MENÚ
    # ==========================================
    @staticmethod
    def remove_from_menu(
        db: Session,
        id_menu: int,
        id_plato: int,
    ):
        menu = (
            db.query(Menu)
            .options(joinedload(Menu.platos))
            .filter(Menu.id_menu == id_menu)
            .first()
        )

        if menu is None:
            return False

        plato = (
            db.query(Plato)
            .filter(Plato.id_plato == id_plato)
            .first()
        )

        if plato is None:
            return False

        if plato in menu.platos:
            menu.platos.remove(plato)

        db.commit()

        return True

    # ==========================================
    # ELIMINAR SI NO SE USA
    # ==========================================
    @staticmethod
    def delete_if_unused(
        db: Session,
        id_plato: int,
    ):
        plato = (
            db.query(Plato)
            .options(joinedload(Plato.menus))
            .filter(Plato.id_plato == id_plato)
            .first()
        )

        if plato is None:
            return False

        if len(plato.menus) == 0:
            db.delete(plato)
            db.commit()

        return True

    # ==========================================
    # QUITAR DEL MENÚ Y BORRAR SI QUEDA LIBRE
    # ==========================================
    @staticmethod
    def remove_and_delete_if_unused(
        db: Session,
        id_menu: int,
        id_plato: int,
    ):
        PlatoService.remove_from_menu(
            db,
            id_menu,
            id_plato,
        )

        PlatoService.delete_if_unused(
            db,
            id_plato,
        )

        return True