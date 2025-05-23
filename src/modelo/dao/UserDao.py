import sqlite3
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UserVo import UserVo

class UserDao(Conexion):
    SQL_INSERT = """
        INSERT INTO Usuarios(dni, nombre, apellido, email, contrasena_hash, telefono, fecha_alta, credencial_activa, tipo)
        VALUES (?, ?, ?, ?, ?, ?, DATE('now'), ?, ?)
    """
    SQL_SELECT = "SELECT * FROM Usuarios"
    SQL_FIND_BY_CORREO = "SELECT * FROM Usuarios WHERE email = ?"
    SQL_UPDATE_SALDO = "UPDATE Usuarios SET saldo = ? WHERE id_usuario = ?"

    def insert(self, user: UserVo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_INSERT, (
                user.dni,
                user.nombre,
                user.apellido,
                user.correo,
                user.contrasena,
                user.telefono,
                user.activo,
                user.rol
            ))
            self.conexion.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error insertando usuario:", e)
            return None

    def find_by_correo(self, correo):
        cursor = self.getCursor()
        cursor.execute(self.SQL_FIND_BY_CORREO, (correo,))
        row = cursor.fetchone()
        if row:
            return UserVo(*row)
        return None

    def select(self):
        cursor = self.getCursor()
        cursor.execute(self.SQL_SELECT)
        return [UserVo(*row) for row in cursor.fetchall()]

    def update_saldo(self, id_usuario, nuevo_saldo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE_SALDO, (nuevo_saldo, id_usuario))
            self.conexion.commit()
            return True
        except Exception as e:
            print("Error actualizando saldo:", e)
            return False
