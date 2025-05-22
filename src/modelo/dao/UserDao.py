from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UserVo import UserVo
from src.modelo.vo.LoginVO import LoginVO
from typing import List
import bcrypt

class UserDao(Conexion):
    # Consultas SQL
    SQL_SELECT = """
        SELECT idUser, nombre, apellido, correo, contrasena, rol, saldo, tui FROM usuario
    """
    SQL_INSERT = """
        INSERT INTO usuario(nombre, apellido, correo, contrasena, rol, saldo, tui)
        VALUES(?, ?, ?, ?, ?, ?, ?)
    """
    SQL_CONSULTA_CORREO = "SELECT * FROM usuario WHERE correo = ?"
    SQL_UPDATE_SALDO = "UPDATE usuario SET saldo = ? WHERE idUser = ?"

    def select(self) -> List[UserVo]:
        cursor = self.getCursor()
        usuarios = []
        try:
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()
            for row in rows:
                idUser, nombre, apellido, correo, contrasena, rol, saldo, tui = row
                usuario = UserVo(idUser, nombre, apellido, correo, contrasena, rol, saldo, tui)
                usuarios.append(usuario)
        except Exception as e:
            print("Error en select:", e)
        return usuarios

    def insert(self, user: UserVo):
        cursor = self.getCursor()
        try:
            # Hash de contraseña antes de insertar
            hashed_password = bcrypt.hashpw(user.contrasena.encode(), bcrypt.gensalt()).decode()

            cursor.execute(self.SQL_INSERT, (
                user.nombre,
                user.apellido,
                user.correo,
                hashed_password,
                user.rol,
                user.saldo,
                user.tui
            ))
            self.conexion.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error insertando usuario:", e)
            return None

    def find_by_correo(self, correo: str):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_CONSULTA_CORREO, [correo])
            row = cursor.fetchone()
            if row:
                idUser, nombre, apellido, correo, contrasena, rol, saldo, tui = row
                return UserVo(idUser, nombre, apellido, correo, contrasena, rol, saldo, tui)
        except Exception as e:
            print("Error en find_by_correo:", e)
        return None

    def consultarUsuarioPorCorreo(self, loginVO: LoginVO):
        return self.find_by_correo(loginVO.correo)

    def update_saldo(self, idUser: int, nuevo_saldo: float):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE_SALDO, (nuevo_saldo, idUser))
            self.conexion.commit()
            return True
        except Exception as e:
            print("Error actualizando saldo:", e)
            return False
