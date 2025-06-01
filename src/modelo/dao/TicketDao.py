def obtener_datos_ticket(self, id_reserva):
    cursor = self.getCursor()
    cursor.execute("""
        SELECT r.id_reserva, u.nombre, u.email, r.fecha, r.total
        FROM Reservas r
        JOIN Usuarios u ON r.id_usuario = u.id_usuario
        WHERE r.id_reserva = ?
    """, (id_reserva,))
    return cursor.fetchone()
