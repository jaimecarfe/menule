from src.modelo.conexion.Conexion  import Conexion
from src.modelo.vo.UserVo import UserVo
from typing import List

class UserDao(Conexion):
    SQL_SELECT = "SELECT idUser, nombre, apellido, correo, contrasena FROM usuario"
    SQL_INSERT = "INSERT INTO usuario(nombre, apellido, correo, contrasena) VALUES(?, ?, ?, ?)" #agora
    SQL_CONSULTA = "SELECT * FROM usuario WHERE nombre = ?"

    def consultalogin(self, loginVO):
        cursor = self.getCursor()
        cursor.execute(self.SQL_CONSULTA, [loginVO.nombre])
        result = cursor.fetchall()
        return result

    def select(self) -> List[UserVo]:
        cursor = self.getCursor()
        usuarios = []
        try:
            cursor.execute(self.SQL_SELECT)
            rows = cursor.fetchall()
            for row in rows:
                idUser, nombre, apellido, correo, contrasena = row
                usuario = UserVo(idUser, nombre, apellido, correo, contrasena)
                usuarios.append(usuario)

        except Exception as e:
            print("e")
        
        return usuarios