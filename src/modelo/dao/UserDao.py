import sqlite3
from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UserVo import UserVo

class UserDao(Conexion):
    SQL_INSERT = """
        INSERT INTO Usuarios(dni, nombre, apellido, email, contrasena_hash, telefono, fecha_alta, credencial_activa, tipo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    SQL_SELECT = "SELECT id_usuario, dni, nombre, apellido, email, contrasena_hash, telefono, fecha_alta, credencial_activa, tipo FROM Usuarios WHERE credencial_activa = TRUE"
    SQL_FIND_BY_CORREO = "SELECT id_usuario, dni, nombre, apellido, email, contrasena_hash, telefono, fecha_alta, credencial_activa, tipo FROM Usuarios WHERE email = ? AND credencial_activa = 1"

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
                saldo=0.0,
                tui=None,
                dni=dni,
                telefono=telefono,
                fecha_alta=fecha_alta,
                activo=bool(activo)
            )
            usuarios.append(usuario)
        return usuarios
    
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
                saldo=0.0,
                tui=None,
                dni=dni,
                telefono=telefono,
                fecha_alta=fecha_alta,
                activo=bool(activo)
            )
        return None

    def update_saldo(self, id_usuario, nuevo_saldo):
        cursor = self.getCursor()
        try:
            # Obtener el rol del usuario
            cursor.execute("SELECT tipo FROM Usuarios WHERE id_usuario = ?", (id_usuario,))
            row = cursor.fetchone()
            if not row:
                print("Usuario no encontrado.")
                return False
            rol = row[0]

            # Actualizar saldo en la tabla correspondiente según el rol
            if rol == "estudiante":
                cursor.execute("UPDATE Estudiantes SET saldo = ? WHERE id_usuario = ?", (nuevo_saldo, id_usuario))
            elif rol == "profesor":
                cursor.execute("UPDATE Profesores SET saldo = ? WHERE id_usuario = ?", (nuevo_saldo, id_usuario))
            else:
                print("El rol no tiene saldo asociado.")
                return False
            return True
        except Exception as e:
            print("Error actualizando saldo:", e)
            return False        

    def eliminar_usuario_logico(self, user_id):
        """
        Marca un usuario como inactivo (eliminación lógica).
        No permite dar de baja a un administrador.
        :param user_id: ID del usuario a desactivar
        :return: True si se realizó la operación, "admin" si es administrador, False si falló
        """
        try:
            cursor = self.getCursor()
            cursor.execute("SELECT tipo FROM Usuarios WHERE id_usuario = ?", (user_id,))
            row = cursor.fetchone()
            if row and row[0] == "administrador":
                return "admin"
            cursor.execute("UPDATE Usuarios SET credencial_activa = 0 WHERE id_usuario = ?", (user_id,))
            return True
        except Exception as e:
            print(f"Error al dar de baja usuario: {e}")
            return False

    def eliminar_usuario_fisico(self, user_id):
        """
        Elimina completamente al usuario de la base de datos, excepto si es administrador.
        Devuelve:
            True si lo elimina,
            "admin" si es administrador,
            "integridad" si hay error de integridad referencial,
            False para otros errores.
        """
        try:
            cursor = self.getCursor()
            cursor.execute("SELECT tipo FROM Usuarios WHERE id_usuario = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                return False

            rol = row[0]
            if rol == "administrador":
                return "admin"

            # Elimina primero de la tabla correspondiente según el rol
            if rol == "profesor":
                cursor.execute("DELETE FROM Profesores WHERE id_usuario = ?", (user_id,))
            elif rol == "personal_comedor":
                cursor.execute("DELETE FROM PersonalComedor WHERE id_usuario = ?", (user_id,))
            elif rol == "estudiante":
                cursor.execute("DELETE FROM Estudiantes WHERE id_usuario = ?", (user_id,))

            try:
                cursor.execute("DELETE FROM Usuarios WHERE id_usuario = ?", (user_id,))
            except sqlite3.IntegrityError as ie:
                print(f"Error de integridad al eliminar usuario: {ie}")
                return "integridad"
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            if "Integrity" in str(e):
                return "integridad"
            return False
        
    def listarUsuarios(self):
        cursor = self.getCursor()
        cursor.execute("SELECT id_usuario, dni, nombre, apellido, email, contrasena_hash, telefono, fecha_alta, credencial_activa, tipo FROM Usuarios")
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
                saldo=0.0,
                tui=None,
                dni=dni,
                telefono=telefono,
                fecha_alta=fecha_alta,
                activo=bool(activo)
            )
            usuarios.append(usuario)
        return usuarios

    def actualizar_contrasena(self, id_usuario, nueva_contrasena_hash):
        cursor = self.getCursor()
        try:
            cursor.execute("UPDATE Usuarios SET contrasena_hash = ? WHERE id_usuario = ?", (nueva_contrasena_hash, id_usuario))
            return True
        except Exception as e:
            print("Error al actualizar contraseña:", e)
            return False
    
    def actualizar_campo_usuario(self, id_usuario, campo, valor):
        campos_permitidos = ["dni","nombre", "apellido", "email", "tipo", "credencial_activa"]
        if campo not in campos_permitidos:
            raise ValueError(f"Campo no permitido: {campo}")
        if isinstance(valor, str):
            valor_sql = f"'{valor}'"
        elif isinstance(valor, bool):
            valor_sql = "1" if valor else "0"
        else:
            valor_sql = str(valor)
        sql = f"UPDATE Usuarios SET {campo} = {valor_sql} WHERE id_usuario = {id_usuario}"
        conexion = Conexion()
        cursor = conexion.getCursor()
        cursor.execute(sql)
        cursor.close()
        conexion.closeConnection()

    def buscar_por_dni(self, dni):
        cursor = self.getCursor()
        cursor.execute("SELECT * FROM Usuarios WHERE dni = ?", (dni,))
        return cursor.fetchone()
    

    def get_by_id(self, id_usuario):
        cursor = self.getCursor()
        cursor.execute("SELECT id_usuario, nombre, apellido, email, tipo FROM Usuarios WHERE id_usuario = ?", (id_usuario,))
        fila = cursor.fetchone()
        cursor.close()

        if fila:
            from src.modelo.vo.UserVo import UserVo
            return UserVo(
                idUser=fila[0],
                nombre=fila[1],
                apellido=fila[2],
                correo=fila[3],
                contrasena="",
                rol=fila[4]
            )
        else:
            return None

    def obtener_saldo(self, id_usuario):
        cursor = self.getCursor()
        try:
            # Obtener el rol del usuario
            cursor.execute("SELECT tipo FROM Usuarios WHERE id_usuario = ?", (id_usuario,))
            row = cursor.fetchone()
            if not row:
                print("Usuario no encontrado.")
                return None
            rol = row[0]

            # Filtrar por rol y obtener saldo
            if rol == "estudiante":
                cursor.execute("SELECT saldo FROM Estudiantes WHERE id_usuario = ?", (id_usuario,))
            elif rol == "profesor":
                cursor.execute("SELECT saldo FROM Profesores WHERE id_usuario = ?", (id_usuario,))
            else:
                print("El rol no tiene saldo asociado.")
                return None

            fila = cursor.fetchone()
            if fila:
                return fila[0]
            return None
        except Exception as e:
            print("Error obteniendo saldo:", e)
            return None
