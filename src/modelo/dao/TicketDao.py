from src.modelo.conexion.Conexion import Conexion
from src.modelo.dao.PagoDao import PagoDao

class TicketDao:
    def getCursor(self):
        return Conexion().getCursor()

    def obtener_datos_ticket(self, id_reserva):
        cursor = self.getCursor()

        # --- BLINDAJE ANTI-DICCIONARIOS (Crasheo setObject dict de Java) ---
        if isinstance(id_reserva, dict):
            id_reserva = id_reserva.get('id_reserva', id_reserva.get('id', 0))
        elif hasattr(id_reserva, 'id_reserva'):
            id_reserva = id_reserva.id_reserva

        # Forzamos conversión estricta a un entero primitivo de Python que Java entienda
        id_reserva_limpio = int(id_reserva)

        try:
            # 1. Intentar obtener datos del usuario registrado
            cursor.execute("""
                SELECT r.id_reserva, u.nombre, u.email, r.fecha_reserva
                FROM Reservas r
                JOIN Usuarios u ON r.id_usuario = u.id_usuario
                WHERE r.id_reserva = ?
            """, (id_reserva_limpio,))
            datos = cursor.fetchone()

            # Si no hay datos o el correo es NULL, buscar en la tabla Pagos (visitante)
            if not datos or not datos[2]:
                cursor.execute("""
                    SELECT r.id_reserva, 'Visitante', p.correo, r.fecha_reserva
                    FROM Reservas r
                    JOIN Pagos p ON r.id_reserva = p.id_reserva
                    WHERE r.id_reserva = ? AND r.id_usuario = 0
                    ORDER BY p.fecha_pago DESC LIMIT 1
                """, (id_reserva_limpio,))
                datos_pagos = cursor.fetchone()

                if datos_pagos:
                    # Si el correo en datos es None, reemplazar con el correo de Pagos
                    if datos and datos[2] is None:
                        datos = (datos[0], datos[1], datos_pagos[2], datos[3])
                    else:
                        datos = datos_pagos

            if datos:
                pago_dao = PagoDao()
                # CORRECCIÓN: Cambiamos total_pagado_por_reserva por obtener_total_pagado para coincidir con tu PagoDao real
                total = pago_dao.obtener_total_pagado(id_reserva_limpio)
                return datos + (total,)

            return None
            
        except Exception as e:
            print("Error en TicketDao al obtener datos del ticket:", e)
            return None
        finally:
            try: cursor.close()
            except Exception: pass

    def insert(self, ticketVO):
        cursor = self.getCursor()
        connection = None
        if hasattr(cursor, '_connection'):
            connection = cursor._connection
        elif hasattr(cursor, 'connection'):
            connection = cursor.connection

        try:
            # Sanitizar id_reserva interno si fuera necesario
            id_reserva = ticketVO.id_reserva
            if isinstance(id_reserva, dict):
                id_reserva = id_reserva.get('id_reserva', id_reserva.get('id', 0))
            id_reserva_limpio = int(id_reserva)

            cursor.execute("""
                INSERT INTO Tickets (codigo, id_reserva, fecha_emision, estado)
                VALUES (?, ?, ?, ?)
            """, (ticketVO.codigo, id_reserva_limpio, ticketVO.fecha_emision, ticketVO.estado))
            
            # Commit protegido contra autocommit=true
            if connection:
                try: connection.commit()
                except Exception: pass

            cursor.execute("SELECT LAST_INSERT_ID()")
            last_id = cursor.fetchone()[0]
            return last_id
            
        except Exception as e:
            print("Error al insertar ticket:", e)
            return None
        finally:
            try: cursor.close()
            except Exception: pass

    def marcar_usado(self, codigo):
        cursor = self.getCursor()
        connection = None
        if hasattr(cursor, '_connection'):
            connection = cursor._connection
        elif hasattr(cursor, 'connection'):
            connection = cursor.connection

        try:
            cursor.execute("""
                UPDATE Tickets
                SET estado = 'usado'
                WHERE codigo = ?
            """, (str(codigo),))
            
            # Commit protegido contra autocommit=true
            if connection:
                try: connection.commit()
                except Exception: pass

            return True
        except Exception as e:
            print("Error al marcar ticket como usado:", e)
            return False
        finally:
            try: cursor.close()
            except Exception: pass