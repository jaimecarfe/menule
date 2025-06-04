from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QHeaderView
from PyQt5.QtCore import Qt
from src.modelo.conexion.Conexion import Conexion
from PyQt5 import uic


#Form, Window = uic.loadUiType("./src/vista/ui/ProcesarPedidos.ui")

class ProcesarPedidos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Procesar Pedidos")
        self.setMinimumSize(800, 500)

        self.conn = Conexion().conexion

        # Layout principal
        self.layout = QVBoxLayout()

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "ID Reserva", "Correo", "Menú (3 platos)", "Acciones"])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.tabla)

        # Botón actualizar
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.clicked.connect(self.cargar_datos)
        self.layout.addWidget(self.btn_actualizar)

        # Asignar layout
        self.setLayout(self.layout)

        # Cargar datos al iniciar
        self.cargar_datos()

    def cargar_datos(self):
        cursor = self.conn.cursor()
        self.tabla.setRowCount(0)
        cursor.execute("""
            SELECT r.id_reserva, r.fecha_reserva, u.email,
                GROUP_CONCAT(p.nombre SEPARATOR ', ') AS platos,
                r.estado_bit
            FROM Reservas r
            JOIN Usuarios u ON r.id_usuario = u.id_usuario
            JOIN ReservaPlatos rp ON r.id_reserva = rp.id_reserva
            JOIN Platos p ON rp.id_plato = p.id_plato
            WHERE r.estado IN ('confirmada', 'pendiente')
            GROUP BY r.id_reserva
            ORDER BY r.fecha_reserva DESC
        """)
        rows = cursor.fetchall()

        for i, (id_reserva, fecha, email, platos, estado_bit) in enumerate(rows):
            self.tabla.insertRow(i)
            self.tabla.setItem(i, 0, QTableWidgetItem(str(fecha)))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(id_reserva)))
            self.tabla.setItem(i, 2, QTableWidgetItem(email))

            # Celda de menú con botón emergente
            item_menu = QTableWidgetItem(platos)
            item_menu.setToolTip("Haz clic para ver detalles")
            self.tabla.setItem(i, 3, item_menu)

            # Botones de acción
            widget = QWidget()
            hbox = QHBoxLayout()
            btn_recogida = QPushButton("Recogida")
            btn_cancelar = QPushButton("Cancelar")

            # Marcar visualmente si está activo
            if estado_bit == 1:
                btn_recogida.setStyleSheet("background-color: lightgreen;")
            elif estado_bit == 0:
                btn_cancelar.setStyleSheet("background-color: lightcoral;")

            # Conectar acciones
            btn_recogida.clicked.connect(lambda _, r=id_reserva, b1=btn_recogida, b2=btn_cancelar: self.actualizar_estado(r, 1, b1, b2))
            btn_cancelar.clicked.connect(lambda _, r=id_reserva, b1=btn_recogida, b2=btn_cancelar: self.actualizar_estado(r, 0, b1, b2))

            hbox.addWidget(btn_recogida)
            hbox.addWidget(btn_cancelar)
            hbox.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(hbox)
            self.tabla.setCellWidget(i, 4, widget)

        # Ajustes de visibilidad
        self.tabla.resizeColumnsToContents()
        self.tabla.resizeRowsToContents()
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Conectar evento de clic en menú
        self.tabla.cellClicked.connect(self.mostrar_detalle_menu)

    def actualizar_estado(self, id_reserva, bit, boton_recogida, boton_cancelar):
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE Reservas SET estado_bit = ? WHERE id_reserva = ?", (bit, id_reserva))
            #self.conn.commit()

            if bit == 1:
                boton_recogida.setStyleSheet("background-color: lightgreen;")
                boton_cancelar.setStyleSheet("")
            else:
                boton_cancelar.setStyleSheet("background-color: lightcoral;")
                boton_recogida.setStyleSheet("")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar la reserva:\n{e}")


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
    
    def mostrar_detalle_menu(self, row, column):
        if column == 3:  # Menú (3 platos)
            item = self.tabla.item(row, column)
            if item:
                texto = item.text()
                platos = [p.strip() for p in texto.split(",")]
                mensaje = "\n".join(platos)
                QMessageBox.information(self, "Detalle del menú", mensaje)

