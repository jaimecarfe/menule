from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from src.modelo.conexion.Conexion import Conexion

class ProcesarPedidos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Procesar Pedidos")
        self.setMinimumSize(700, 400)
        self.conn = Conexion().conexion
        self.layout = QVBoxLayout()
        self.tabla = QTableWidget()
        self.layout.addWidget(self.tabla)

        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "ID Reserva", "Correo", "Menú (3 platos)", "Acciones"])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.clicked.connect(self.cargar_datos)
        self.layout.addWidget(self.btn_actualizar)

        self.setLayout(self.layout)
        self.cargar_datos()

    def cargar_datos(self):
        cursor = self.conn.cursor()
        self.tabla.setRowCount(0)
        cursor.execute("""
            SELECT r.id_reserva, r.fecha_reserva, u.email,
                   GROUP_CONCAT(p.nombre SEPARATOR ', ') AS platos,
                   r.estado
            FROM Reservas r
            JOIN Usuarios u ON r.id_usuario = u.id_usuario
            JOIN ReservaPlatos rp ON r.id_reserva = rp.id_reserva
            JOIN Platos p ON rp.id_plato = p.id_plato
            WHERE r.estado IN ('confirmada', 'pendiente')
            GROUP BY r.id_reserva
            ORDER BY r.fecha_reserva DESC
        """)
        rows = cursor.fetchall()
        for i, (id_reserva, fecha, email, platos, estado) in enumerate(rows):
            self.tabla.insertRow(i)
            self.tabla.setItem(i, 0, QTableWidgetItem(str(fecha)))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(id_reserva)))
            self.tabla.setItem(i, 2, QTableWidgetItem(email))
            self.tabla.setItem(i, 3, QTableWidgetItem(platos))

            widget = QWidget()
            hbox = QHBoxLayout()
            btn_completar = QPushButton("Recogida")
            btn_cancelar = QPushButton("Cancelar")
            hbox.addWidget(btn_completar)
            hbox.addWidget(btn_cancelar)
            hbox.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(hbox)

            btn_completar.clicked.connect(lambda _, r=id_reserva: self.actualizar_estado(r, "recogida"))
            btn_cancelar.clicked.connect(lambda _, r=id_reserva: self.actualizar_estado(r, "cancelada"))

            self.tabla.setCellWidget(i, 4, widget)

    def actualizar_estado(self, id_reserva, nuevo_estado):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE Reservas SET estado = %s WHERE id_reserva = %s", (nuevo_estado, id_reserva))
        self.conn.commit()
        QMessageBox.information(self, "Reserva actualizada", f"Reserva {id_reserva} marcada como {nuevo_estado}.")
        self.cargar_datos()


    def cargar_reservas_pendientes(self):
        reservas = self._modelo.obtener_reservas_pendientes()
        self.tabla.setRowCount(len(reservas))

        for i, reserva in enumerate(reservas):
            self.tabla.setItem(i, 0, QTableWidgetItem(reserva['fecha']))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(reserva['id_reserva'])))
            self.tabla.setItem(i, 2, QTableWidgetItem(reserva['correo']))
            self.tabla.setItem(i, 3, QTableWidgetItem(reserva['menu']))

    # En BussinessObject
    def obtener_reservas_pendientes(self):
        return self._reservaDao.obtener_reservas_con_detalle(estado='pendiente')

    # En ReservaDao
    def obtener_reservas_con_detalle(self, estado='pendiente'):
        cursor = self.getCursor()
        cursor.execute("""
            SELECT r.id_reserva, r.fecha_reserva, u.email,
                GROUP_CONCAT(p.nombre SEPARATOR ', ') as menu
            FROM Reservas r
            JOIN Usuarios u ON r.id_usuario = u.id_usuario
            JOIN ReservaPlatos rp ON r.id_reserva = rp.id_reserva
            JOIN Platos p ON rp.id_plato = p.id_plato
            WHERE r.estado = ?
            GROUP BY r.id_reserva
            ORDER BY r.fecha_reserva DESC
        """, (estado,))
        rows = cursor.fetchall()
        return [
            {
                'id_reserva': row[0],
                'fecha': row[1].strftime('%Y-%m-%d'),
                'correo': row[2],
                'menu': row[3]
            }
            for row in rows
        ]
