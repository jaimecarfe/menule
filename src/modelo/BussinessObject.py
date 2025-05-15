from src.modelo.dao.UserDao import UserDao
from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UserVo import UserVo
import bcrypt  # Para manejo seguro de contraseñas

class BussinessObject:

    def comprobarLogin(self, loginVO: LoginVO) -> UserVo | None:
        """
        Valida el login: busca usuario por correo y compara contraseñas (hasheadas).
        Devuelve UserVo si correcto, None si fallo.
        """
        user_dao = UserDao()
        user = user_dao.find_by_correo(loginVO.correo)
        if user and bcrypt.checkpw(loginVO.contrasena.encode(), user.contrasena.encode()):
            return user
        return None

    def registrarUsuario(self, user: UserVo) -> int | None:
        """
        Registra un usuario nuevo en la BD.
        Hace hash de la contraseña antes de insertar.
        Devuelve el id generado o None si error.
        """
        user_dao = UserDao()
        # Hashear la contraseña
        hashed_pw = bcrypt.hashpw(user.contrasena.encode(), bcrypt.gensalt())
        user.contrasena = hashed_pw.decode()
        
        # Insertar usuario
        return user_dao.insert(user)

    def actualizarSaldo(self, idUser: int, nuevo_saldo: float) -> bool:
        """
        Actualiza el saldo del usuario.
        Devuelve True si OK, False si error.
        """
        user_dao = UserDao()
        return user_dao.update_saldo(idUser, nuevo_saldo)

    def obtenerUsuarioPorCorreo(self, correo: str) -> UserVo | None:
        """
        Obtiene un usuario dado su correo.
        """
        user_dao = UserDao()
        return user_dao.find_by_correo(correo)
