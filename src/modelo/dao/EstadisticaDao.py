from src.modelo.conexion.Conexion import Conexion

class EstadisticaDao:
    def obtener_pagos(self):
        conn = Conexion()
        cursor = conn.getCursor()

        cursor.execute("SELECT SUM(saldo) FROM Estudiantes")
        total_estudiantes = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(saldo) FROM Profesores")
        total_profesores = cursor.fetchone()[0] or 0

        return [
            ("Estudiantes", total_estudiantes),
            ("Profesores", total_profesores)
        ]
    def obtener_incidencias(self):
        conn = Conexion()
        cursor = conn.getCursor()
        cursor.execute("SELECT fecha_reporte, COUNT(*) FROM Incidencias GROUP BY fecha_reporte")
        datos = cursor.fetchall()
        return datos

    def obtener_menus(self):
        conn = Conexion()
        cursor = conn.getCursor()
        cursor.execute("SELECT fecha, COUNT(*) FROM Menus GROUP BY fecha")
        datos = cursor.fetchall()
        return datos

    def obtener_reservas(self):
        conn = Conexion()
        cursor = conn.getCursor()
        cursor.execute("SELECT fecha_reserva, COUNT(*) FROM Reservas GROUP BY fecha_reserva")
        datos = cursor.fetchall()
        return datos
    
    def obtener_total_pagos_por_rol(self):
        conn= Conexion()
        query = """
        SELECT tipo, SUM(monto) as total_gastado,
                COUNT(pagos.id_pago) AS cantidad_pagos
        FROM pagos 
        JOIN usuarios ON pagos.id_usuario = usuarios.id_usuario
        GROUP BY tipo
        """
        cursor = conn.getCursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados  # Lista de tuplas (tipo, total_gastado)
    

    def obtener_total_incidencias_por_rol(self):
        conn = Conexion()
        query = """
        SELECT tipo, COUNT(incidencias.id_incidencia) AS cantidad_incidencias
        FROM incidencias 
        JOIN usuarios ON incidencias.id_usuario = usuarios.id_usuario
        GROUP BY tipo
        """
        cursor = conn.getCursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

