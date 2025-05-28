import sqlite3
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UserVo import UserVo

class UserDao(Conexion):
    SQL_INSERT = """
        INSERT INTO Usuarios(dni, nombre, apellido, email, contrasena_hash, telefono, fecha_alta, credencial_activa, tipo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    SQL_SELECT = "SELECT * FROM Usuarios WHERE credencial_activa = TRUE"
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

    def eliminar_usuario_logico(self, user_id):
        """
        Marca un usuario como inactivo (eliminación lógica).
        :param user_id: ID del usuario a desactivar
        :return: True si se realizó la operación, False si falló
        """
        try:
            conexion = Conexion()
            cursor = conexion.getCursor()
            cursor.execute("UPDATE usuarios SET credencial_activa = FALSE WHERE id_usuario = ?", (user_id,))
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False
        
    def find_by_correo(self, correo):
        """
        Devuelve un usuario activo por correo. Solo si credencial_activa = 1.
        """
        cursor = self.getCursor()
        cursor.execute("SELECT * FROM Usuarios WHERE email = ? AND credencial_activa = 1", (correo,))
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


    def eliminar_usuario_logico(self, user_id):
        """
        Elimina completamente al usuario de la base de datos, excepto si es administrador.
        """
        try:
            cursor = self.getCursor()
            cursor.execute("SELECT tipo FROM Usuarios WHERE id_usuario = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                print("Usuario no encontrado.")
                return False

            rol = row[0]
            if rol == "administrador":
                print("No se puede eliminar un administrador.")
                return False

            cursor.execute("DELETE FROM Estudiantes WHERE id_usuario = ?", (user_id,))
            cursor.execute("DELETE FROM Usuarios WHERE id_usuario = ?", (user_id,))
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False
    
    def listarUsuarios(self):
        query = "SELECT * FROM usuarios"
        cursor = self.getCursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [UserVo(*row) for row in rows]

    def actualizar_contrasena(self, id_usuario, nueva_contrasena_hash):
        cursor = self.getCursor()
        try:
            cursor.execute("UPDATE Usuarios SET contrasena_hash = ? WHERE id_usuario = ?", (nueva_contrasena_hash, id_usuario))
            return True
        except Exception as e:
            print("Error al actualizar contraseña:", e)
            return False

