# src/modelo/dao/PagoDao.py
from src.modelo.conexion.Conexion import Conexion
from datetime import datetime
from src.modelo.vo.PagoVo import PagoVo

class PagoDao:
    def __init__(self):
        self.conexion = Conexion()

    def getCursor(self):
        return self.conexion.getCursor()
    
    def insertar_pago(self, pago_vo):
        cursor = self.getCursor()
        connection = None
        if hasattr(cursor, '_connection'):
            connection = cursor._connection
        elif hasattr(cursor, 'connection'):
            connection = cursor.connection

        try:
            # 1. Extraer los campos base dependiendo de si pago_vo es dict o propiedad
            if isinstance(pago_vo, dict):
                id_usuario = pago_vo.get('id_usuario', 0)
                id_reserva = pago_vo.get('id_reserva', None)
                monto = pago_vo.get('monto', 0.0)
                metodo = pago_vo.get('metodo', 'tarjeta')
                fecha_raw = pago_vo.get('fecha_pago', datetime.now())
                correo = pago_vo.get('correo', None)
            else:
                id_usuario = getattr(pago_vo, 'id_usuario', 0)
                id_reserva = getattr(pago_vo, 'id_reserva', None)
                monto = getattr(pago_vo, 'monto', 0.0)
                metodo = getattr(pago_vo, 'metodo', 'tarjeta')
                fecha_raw = getattr(pago_vo, 'fecha_pago', datetime.now())
                correo = getattr(pago_vo, 'correo', None)

            # --- DESENTRAÑAR ID_USUARIO SI ES UN DICT O UN OBJETO ---
            if isinstance(id_usuario, dict):
                id_usuario = id_usuario.get('id_usuario', id_usuario.get('idUser', id_usuario.get('id', 0)))
            elif hasattr(id_usuario, 'id_usuario'):
                id_usuario = id_usuario.id_usuario
            elif hasattr(id_usuario, 'idUser'):
                id_usuario = id_usuario.idUser

            # --- DESENTRAÑAR ID_RESERVA SI ES UN DICT O UN OBJETO ---
            if isinstance(id_reserva, dict):
                id_reserva = id_reserva.get('id_reserva', id_reserva.get('id', None))
            elif hasattr(id_reserva, 'id_reserva'):
                id_reserva = id_reserva.id_reserva

            # --- FORZAR CONVERSIÓN SEGURA A PRIMITIVOS ---
            try:
                id_usuario = int(id_usuario) if id_usuario is not None else 0
            except Exception:
                id_usuario = 0

            try:
                id_reserva = int(id_reserva) if id_reserva is not None else None
            except Exception:
                id_reserva = None

            try:
                monto = float(monto)
            except Exception:
                monto = 0.0

            # Forzar formateo de fecha limpio
            if isinstance(fecha_raw, (datetime, datetime.date)):
                fecha_str = fecha_raw.strftime('%Y-%m-%d %H:%M:%S')
            else:
                fecha_str = str(fecha_raw)

            if isinstance(correo, dict):
                correo = correo.get('correo', correo.get('email', str(correo)))
            elif correo is not None:
                correo = str(correo)

            # --- INSERCIÓN EN BASE DE DATOS ---
            if id_usuario != 0:
                cursor.execute("""
                    INSERT INTO Pagos (id_usuario, id_reserva, monto, metodo, fecha_pago)
                    VALUES (?, ?, ?, ?, ?)
                """, (id_usuario, id_reserva, monto, metodo, fecha_str))
            else:
                cursor.execute("""
                    INSERT INTO Pagos (id_usuario, id_reserva, monto, metodo, fecha_pago, correo)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (0, id_reserva, monto, metodo, fecha_str, correo))

            cursor.execute("SELECT LAST_INSERT_ID()")
            last_id = cursor.fetchone()[0]

            if connection:
                try: connection.commit()
                except Exception: pass

            return last_id

        except Exception as e:
            print("Error al insertar pago:", e)
            if connection:
                try: connection.rollback()
                except Exception: pass
            return None
        finally:
            try: cursor.close()
            except Exception: pass

    def obtener_total_pagado(self, id_reserva):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT SUM(monto) FROM Pagos WHERE id_reserva = ?
            """, (id_reserva,))
            total = cursor.fetchone()[0]
            return total if total else 0
        except Exception as e:
            print("Error al obtener total pagado por reserva:", e)
            return 0
        finally:
            try: cursor.close()
            except Exception: pass
        
    def obtener_todos_pagos(self):
        cursor = self.getCursor()
        try:
            cursor.execute("SELECT id_pago, id_usuario, id_reserva, monto, metodo, fecha_pago FROM Pagos")
            pagos = cursor.fetchall()
            return [PagoVo(*pago) for pago in pagos]
        except Exception as e:
            print("Error al obtener todos los pagos:", e)
            return []
        finally:
            try: cursor.close()
            except Exception: pass
        
    def obtener_por_usuario(self, id_usuario):
        cursor = self.getCursor()
        try:
            cursor.execute("SELECT id_pago, id_usuario, id_reserva, monto, metodo, fecha_pago FROM Pagos WHERE id_usuario = ?", (id_usuario,))
            pagos = cursor.fetchall()
            return [PagoVo(*pago) for pago in pagos]
        except Exception as e:
            print("Error al obtener pagos por usuario:", e)
            return []
        finally:
            try: cursor.close()
            except Exception: pass