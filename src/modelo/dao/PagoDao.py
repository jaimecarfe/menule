from src.modelo.conexion.Conexion import Conexion
from datetime import datetime
from src.modelo.vo.PagoVo import PagoVo
from datetime import datetime

class PagoDao:
    def __init__(self):
        self.conexion = Conexion()

    def insertar_pago(self, pago_vo):
        cursor = self.conexion.getCursor()
        try:
            if not isinstance(pago_vo.fecha_pago, str):
                fecha_str = pago_vo.fecha_pago.strftime('%Y-%m-%d %H:%M:%S')
            else:
                fecha_str = pago_vo.fecha_pago

            if pago_vo.id_usuario is not None and pago_vo.id_usuario != 0:

                cursor.execute("""
                    INSERT INTO Pagos (id_usuario, id_reserva, monto, metodo, fecha_pago)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    pago_vo.id_usuario,
                    pago_vo.id_reserva,
                    pago_vo.monto,
                    pago_vo.metodo,
                    fecha_str
                ))
            else:  # Visitante
                cursor.execute("""
                    INSERT INTO Pagos (id_usuario, id_reserva, monto, metodo, fecha_pago, correo)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    0,
                    pago_vo.id_reserva,
                    pago_vo.monto,
                    pago_vo.metodo,
                    fecha_str,
                    pago_vo.correo
                ))
            cursor.execute("SELECT LAST_INSERT_ID()")
            pago_id = cursor.fetchone()[0]
            cursor.close()
            return pago_id
        except Exception as e:
            print("Error al insertar pago:", e)
            try:
                cursor.close()
            except Exception:
                pass
            return None

    def total_pagado_por_reserva(self, id_reserva):
        cursor = self.conexion.getCursor()
        try:
            cursor.execute("""
                SELECT SUM(monto) FROM Pagos WHERE id_reserva = ?
            """, (id_reserva,))
            total = cursor.fetchone()[0]
            cursor.close()
            return total if total else 0
        except Exception as e:
            print("Error al obtener total pagado por reserva:", e)
            try:
                cursor.close()
            except Exception:
                pass
            return 0
        
    def obtener_todos_pagos(self):
        cursor = self.conexion.getCursor()
        try:
            cursor.execute("SELECT * FROM Pagos")
            pagos = cursor.fetchall()
            cursor.close()
            return [PagoVo(*pago) for pago in pagos]
        except Exception as e:
            print("Error al obtener todos los pagos:", e)
            try:
                cursor.close()
            except Exception:
                pass
            return []
        
    def obtener_por_usuario(self, id_usuario):
        cursor = self.conexion.getCursor()
        try:
            cursor.execute("SELECT * FROM Pagos WHERE id_usuario = ?", (id_usuario,))
            pagos = cursor.fetchall()
            cursor.close()
            return [PagoVo(*pago) for pago in pagos]
        except Exception as e:
            print("Error al obtener pagos por usuario:", e)
            try:
                cursor.close()
            except Exception:
                pass
            return []