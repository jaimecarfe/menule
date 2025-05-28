from src.modelo.conexion.Conexion import Conexion

class ConfiguracionDao:
    def obtener_configuraciones(self):
        try:
            conexion = Conexion()
            cursor = conexion.getCursor()
            cursor.execute("SELECT clave, valor FROM configuraciones")
            filas = cursor.fetchall()
            return {clave: valor for clave, valor in filas}
        except Exception as e:
            print(f"Error al obtener configuraciones: {e}")
            return {}

    def guardar_configuracion(self, clave, valor):
        try:
            conexion = Conexion()
            cursor = conexion.getCursor()
            cursor.execute(
                "REPLACE INTO configuraciones (clave, valor) VALUES (?, ?)",
                (clave, valor)
            )
            return True
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
            return False
