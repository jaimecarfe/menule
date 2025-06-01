from src.modelo.conexion.Conexion import Conexion
from datetime import datetime

class ReservaDao:
    def getCursor(self):
        return Conexion().getCursor()

    def crear_reserva(self, id_usuario, total):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                INSERT INTO Reservas (id_usuario, fecha, total, estado)
                VALUES (?, ?, ?, ?)
            """, (id_usuario, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), total, "confirmada"))
            return True
        except Exception as e:
            print("Error al crear reserva:", e)
            return False

    def obtener_ultima_reserva_id(self, id_usuario):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT id_reserva FROM Reservas 
                WHERE id_usuario = ? 
                ORDER BY fecha DESC LIMIT 1
            """, (id_usuario,))
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print("Error al obtener última reserva:", e)
            return None
