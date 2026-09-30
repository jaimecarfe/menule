from sqlalchemy.orm import Session
from app.models import Usuario
import bcrypt

class PerfilService:
    @staticmethod
    def cambiar_contrasena(db: Session, user_id: int, pass_actual: str, pass_nueva: str) -> tuple[bool, str]:
        user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
        if not user:
            return False, "Usuario no encontrado."

        # Convertimos las contraseñas a bytes para bcrypt
        pass_actual_bytes = pass_actual.encode('utf-8')
        pass_bd_bytes = user.contrasena_hash.encode('utf-8') if isinstance(user.contrasena_hash, str) else user.contrasena_hash

        # Validar la contraseña actual con bcrypt
        try:
            if not bcrypt.checkpw(pass_actual_bytes, pass_bd_bytes):
                return False, "La contraseña actual no es correcta."
        except Exception as e:
            # En caso de que haya contraseñas antiguas en texto plano durante la migración
            if user.contrasena_hash != pass_actual:
                return False, "La contraseña actual no es correcta."

        # Hashear la nueva contraseña con salt
        salt = bcrypt.gensalt()
        hashed_nueva = bcrypt.hashpw(pass_nueva.encode('utf-8'), salt)

        # Guardar como string decodificado en BD
        user.contrasena_hash = hashed_nueva.decode('utf-8')
        db.commit()

        return True, "Contraseña actualizada correctamente."