import bcrypt
from datetime import date
from sqlalchemy.orm import Session
from app.models import Usuario


class RegisterService:

    @staticmethod
    def hash_password(password_raw: str) -> str:
        """Genera el hash de la contraseña usando bcrypt."""
        pwd_bytes = password_raw.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd_bytes, salt)
        return hashed.decode("utf-8")

    @staticmethod
    def email_exists(db: Session, email: str) -> bool:
        """Comprueba si un correo ya existe en la BD."""
        return db.query(Usuario).filter(Usuario.email == email.strip().lower()).first() is not None

    @staticmethod
    def dni_exists(db: Session, dni: str) -> bool:
        """Comprueba si un DNI ya existe en la BD."""
        return db.query(Usuario).filter(Usuario.dni == dni.strip().upper()).first() is not None

    @staticmethod
    def register_user(
        db: Session,
        nombre: str,
        apellido: str,
        email: str,
        password: str,
        dni: str,
        telefono: str,
        tipo: str,
    ) -> Usuario:
        """Crea y guarda el usuario con la contraseña procesada con bcrypt."""
        password_hashed = RegisterService.hash_password(password)

        nuevo_usuario = Usuario(
            dni=dni.strip().upper(),
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            email=email.strip().lower(),
            contrasena_hash=password_hashed,
            telefono=telefono.strip(),
            fecha_alta=date.today(),
            credencial_activa=True,
            tipo=tipo,
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        return nuevo_usuario