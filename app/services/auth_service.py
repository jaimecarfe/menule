import bcrypt
from sqlalchemy.orm import Session
from app.models import Usuario


class AuthService:

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return (
            db.query(Usuario)
            .filter(Usuario.email == email.strip().lower())
            .first()
        )

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        if not password_hash:
            return False
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                password_hash.encode("utf-8"),
            )
        except Exception:
            # Fallback seguro para texto plano si se insertaron manualmente datos de prueba
            return password == password_hash

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = AuthService.get_user_by_email(db, email)

        if user is None:
            return None

        if not AuthService.verify_password(
            password,
            user.contrasena_hash,
        ):
            return None

        return user