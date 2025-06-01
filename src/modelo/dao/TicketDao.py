from src.modelo.conexion.Conexion import Conexion

class TicketDao:
    def getCursor(self):
        return Conexion().getCursor()

    def obtener_datos_ticket(self, id_reserva):
        cursor = self.getCursor()
        cursor.execute("""
            SELECT r.id_reserva, u.nombre, u.email, r.fecha_reserva
            FROM Reservas r
            JOIN Usuarios u ON r.id_usuario = u.id_usuario
            WHERE r.id_reserva = ?
        """, (id_reserva,))
        return cursor.fetchone()
    
    def insert(self, ticketVO):
        cursor = self.getCursor()
        cursor.execute("""
            INSERT INTO Tickets (codigo, id_reserva, fecha_emision, estado)
            VALUES (?, ?, ?, ?)
        """, (ticketVO.codigo, ticketVO.id_reserva, ticketVO.fecha_emision, ticketVO.estado))
        Conexion().commit()
        return cursor.lastrowid
    
    def marcar_usado(self, codigo):
        cursor = self.getCursor()
        cursor.execute("""
            UPDATE Tickets
            SET estado = 'usado'
            WHERE codigo = ?
        """, (codigo,))
        Conexion().commit()
        return cursor.rowcount > 0
    