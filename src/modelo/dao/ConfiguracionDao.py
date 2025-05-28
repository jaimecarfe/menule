from src.modelo.conexion.Conexion import Conexion

class ConfiguracionDao:
    def obtener_configuraciones(self):
        """
        Devuelve todas las configuraciones del sistema en forma de diccionario.
        """
        try:
            conn = Conexion().conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT clave, valor FROM configuraciones")
            filas = cursor.fetchall()
            return {clave: valor for clave, valor in filas}
        except Exception as e:
            print(f"Error al obtener configuraciones: {e}")
            return {}

    def guardar_configuracion(self, clave, valor):
        """
        Guarda una configuración nueva o actualiza una existente.
        """
        try:
            conn = Conexion().conectar()
            cursor = conn.cursor()
            cursor.execute(
                "REPLACE INTO configuraciones (clave, valor) VALUES (?, ?)",
                (clave, valor)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
            return False
