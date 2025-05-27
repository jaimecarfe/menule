import sqlite3
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UserVo import UserVo

class UserDao(Conexion):
    SQL_INSERT = """
        INSERT INTO Usuarios(dni, nombre, apellido, email, contrasena_hash, telefono, fecha_alta, credencial_activa, tipo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                user.fecha_alta.strftime('%Y-%m-%d'),
                user.activo,
                user.rol
            ))
            cursor.execute("SELECT LAST_INSERT_ID()")  # Para MySQL
            return cursor.fetchone()[0]
        except Exception as e:
            print("Error insertando usuario:", e)
            return None

    def find_by_correo(self, correo):
        cursor = self.getCursor()
        cursor.execute(self.SQL_FIND_BY_CORREO, (correo,))
        row = cursor.fetchone()
        if row:
            idUser, dni, nombre, apellido, correo, contrasena_hash, telefono, fecha_alta, activo, tipo = row
            return UserVo(
                idUser=idUser,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                contrasena=contrasena_hash,
                rol=tipo,
                tui=None,
                dni=dni,
                telefono=telefono,
                fecha_alta=fecha_alta,
                activo=activo
            )
        return None

    def select(self):
        cursor = self.getCursor()
        cursor.execute(self.SQL_SELECT)
        usuarios = []
        for row in cursor.fetchall():
            idUser, dni, nombre, apellido, correo, contrasena_hash, telefono, fecha_alta, activo, tipo = row
            usuario = UserVo(
                idUser=idUser,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                contrasena=contrasena_hash,
                rol=tipo,
                tui=None,
                dni=dni,
                telefono=telefono,
                fecha_alta=fecha_alta,
                activo=activo
            )
            usuarios.append(usuario)
        return usuarios

    def update_saldo(self, id_usuario, nuevo_saldo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_UPDATE_SALDO, (nuevo_saldo, id_usuario))
            return True
        except Exception as e:
            print("Error actualizando saldo:", e)
            return False        
