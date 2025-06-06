from src.modelo.conexion.Conexion import Conexion
from datetime import datetime
from src.modelo.vo.PagoVo import PagoVo

class PagoDao:
    def getCursor(self):
        return Conexion().getCursor()

    def total_pagado_por_reserva(self, id_reserva):
        cursor = self.getCursor()
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0)
            FROM Pagos
            WHERE id_reserva = ?
        """, (id_reserva,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0

    def insertar_pago(self, id_usuario, monto, metodo, id_reserva=None, descuento=0, estado='completado', transaccion_id=None):
        cursor = self.getCursor()
        fecha_pago = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO Pagos (id_usuario, id_reserva, monto, metodo, fecha_pago, descuento, estado, transaccion_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            id_usuario,
            id_reserva,
            monto,
            metodo,
            fecha_pago,
            descuento,
            estado,
            transaccion_id
        ))
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        return last_id
    '''
    def obtener_por_usuario(self, id_usuario):
        cursor = self.getCursor()
        cursor.execute("""
            SELECT id_pago, id_reserva, monto, metodo, fecha_pago, descuento, estado, transaccion_id
            FROM Pagos
            WHERE id_usuario = ?
            ORDER BY fecha_pago DESC
        """, (id_usuario,))
        pagos = cursor.fetchall()
        return pagos if pagos else []
    '''
    def obtener_todos_pagos(self):
        cursor = self.getCursor()
        cursor.execute("""
            SELECT id_pago, id_usuario, id_reserva, monto, metodo, fecha_pago, descuento, estado, transaccion_id
            FROM Pagos
            ORDER BY fecha_pago DESC
        """)
        pagos = []
        for row in cursor.fetchall():
            id_pago, id_usuario, id_reserva, monto, metodo, fecha_pago, descuento, estado, transaccion_id = row
            pago = PagoVo(
                id_pago=id_pago,
                id_usuario=id_usuario,
                id_reserva=id_reserva,
                monto=monto,
                metodo=metodo,
                fecha_pago=fecha_pago,
                descuento=descuento,
                estado=estado,
                transaccion_id=transaccion_id
            )
            pagos.append(pago)
        return pagos


