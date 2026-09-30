from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import Usuario


class UserService:

    # =====================================================
    # READ
    # =====================================================

    @staticmethod
    def get_all_users(db: Session):
        """Obtener todos los usuarios."""
        return (
            db.query(Usuario)
            .order_by(Usuario.id_usuario)
            .all()
        )

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        """Buscar un usuario por ID."""
        return (
            db.query(Usuario)
            .filter(Usuario.id_usuario == user_id)
            .first()
        )

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """Buscar un usuario por email."""
        return (
            db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

    @staticmethod
    def search_users(db: Session, search: str):
        """Buscar usuarios por nombre, apellido o email."""
        return (
            db.query(Usuario)
            .filter(
                or_(
                    Usuario.nombre.ilike(f"%{search}%"),
                    Usuario.apellido.ilike(f"%{search}%"),
                    Usuario.email.ilike(f"%{search}%"),
                )
            )
            .order_by(Usuario.id_usuario)
            .all()
        )

    @staticmethod
    def count_users(db: Session):
        """Número total de usuarios."""
        return db.query(Usuario).count()

    # =====================================================
    # CREATE
    # =====================================================

    @staticmethod
    def create_user(
        db: Session,
        nombre: str,
        apellido: str,
        email: str,
        contrasena_hash: str,
        tipo: str,
        dni: str = None,
        telefono: str = None,
    ):
        """Crear un nuevo usuario."""

        user = Usuario(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            email=email,
            contrasena_hash=contrasena_hash,
            tipo=tipo,
            telefono=telefono,
            credencial_activa=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    # =====================================================
    # UPDATE
    # =====================================================

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        **kwargs,
    ):
        """Actualizar un usuario."""

        user = UserService.get_user_by_id(db, user_id)

        if user is None:
            return None

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return user

    # =====================================================
    # DELETE
    # =====================================================

    @staticmethod
    def delete_user(
        db: Session,
        user_id: int,
    ):
        """Eliminar un usuario."""

        user = UserService.get_user_by_id(db, user_id)

        if user is None:
            return False

        db.delete(user)
        db.commit()

        return True

    # =====================================================
    # EXISTS
    # =====================================================

    @staticmethod
    def email_exists(
        db: Session,
        email: str,
    ):
        """Comprobar si un email ya existe."""

        return (
            db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
            is not None
        )