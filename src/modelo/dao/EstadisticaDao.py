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