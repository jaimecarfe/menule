from src.modelo.conexion.Conexion import Conexion
from datetime import datetime
from src.modelo.vo.ReservaVo import ReservaVo

class ReservaDao:
    def getCursor(self):
        return Conexion().getCursor()

    def insert(self, reservaVO):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                INSERT INTO Reservas (id_usuario, id_menu, fecha_reserva, estado)
                VALUES (?, ?, ?, ?)
            """, (
                reservaVO.id_usuario,
                reservaVO.id_menu,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                reservaVO.estado
            ))
            return cursor.lastrowid
        except Exception as e:
            print("Error al crear reserva:", e)
            return None

    def obtener_ultima_reserva_id(self, id_usuario):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT id_reserva FROM Reservas 
                WHERE id_usuario = ? 
                ORDER BY fecha_reserva DESC LIMIT 1
            """, (id_usuario,))
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print("Error al obtener última reserva:", e)
            return None