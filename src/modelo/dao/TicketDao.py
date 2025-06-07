from src.modelo.conexion.Conexion import Conexion
from src.modelo.dao.PagoDao import PagoDao

class TicketDao:
    def getCursor(self):
        return Conexion().getCursor()

    def obtener_datos_ticket(self, id_reserva):
        cursor = self.getCursor()

        # Intentar obtener datos del usuario registrado
        cursor.execute("""
            SELECT r.id_reserva, u.nombre, u.email, r.fecha_reserva
            FROM Reservas r
            JOIN Usuarios u ON r.id_usuario = u.id_usuario
            WHERE r.id_reserva = ?
        """, (id_reserva,))
        datos = cursor.fetchone()

        # Si no hay datos o el correo es NULL, buscar en la tabla Pagos (visitante)
        if not datos or not datos[2]:
            cursor.execute("""
                SELECT r.id_reserva, 'Visitante', p.correo, r.fecha_reserva
                FROM Reservas r
                JOIN Pagos p ON r.id_reserva = p.id_reserva
                WHERE r.id_reserva = ? AND r.id_usuario = 0
                ORDER BY p.fecha_pago DESC LIMIT 1
            """, (id_reserva,))
            datos_pagos = cursor.fetchone()

            if datos_pagos:
                # Si el correo en datos es None, reemplazar con el correo de Pagos
                if datos and datos[2] is None:
                    datos = (datos[0], datos[1], datos_pagos[2], datos[3])
                else:
                    datos = datos_pagos

        if datos:
            pago_dao = PagoDao()
            total = pago_dao.total_pagado_por_reserva(id_reserva)
            return datos + (total,)

        return None

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