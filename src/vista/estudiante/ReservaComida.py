from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QComboBox
from src.modelo.dao.ReservaDao import ReservaDao
from src.vista.comun.GenerarTicket import GenerarTicket

class ReservaComida(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Reservar Comida")

        self.dao = ReservaDao()

        layout = QVBoxLayout()

        self.combo_menu = QComboBox()
        self.menus_disponibles = self.dao.obtener_menus_disponibles()
        for menu in self.menus_disponibles:
            self.combo_menu.addItem(f"{menu['fecha']} - {menu['tipo']}", userData=menu['id_menu'])
        layout.addWidget(self.combo_menu)

        self.btn_reservar = QPushButton("Confirmar Reserva")
        self.btn_reservar.clicked.connect(self.realizar_reserva)
        layout.addWidget(self.btn_reservar)

        self.btn_ticket = QPushButton("Generar Ticket")
        self.btn_ticket.clicked.connect(self.abrir_ticket)
        layout.addWidget(self.btn_ticket)

        self.setLayout(layout)

    def realizar_reserva(self):
        id_menu = self.combo_menu.currentData()
        total_simulado = 10.0  # Por ahora, lo fijamos

        exito = self.dao.crear_reserva(self.usuario.idUser, id_menu, total_simulado)
        if exito:
            QMessageBox.information(self, "Reserva hecha", "Reserva registrada con éxito.")
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar la reserva.")

    def abrir_ticket(self):
        id_reserva = self.dao.obtener_ultima_reserva_id(self.usuario.idUser)
        if id_reserva:
            self.ticket_window = GenerarTicket(id_reserva)
            self.ticket_window.show()
        else:
            QMessageBox.warning(self, "Sin reserva", "No se encontró ninguna reserva activa.")


    def crear_reserva(self, id_usuario, id_menu, total):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                INSERT INTO Reservas (id_usuario, id_menu, fecha_reserva, estado)
                VALUES (?, ?, NOW(), 'confirmada')
            """, (id_usuario, id_menu))
            return True
        except Exception as e:
            print("Error al crear reserva:", e)
            return False

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
            print("Error al obtener reserva:", e)
            return None

    def obtener_menus_disponibles(self):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT id_menu, fecha, tipo FROM Menus
                WHERE disponible = TRUE
                ORDER BY fecha DESC
            """)
            rows = cursor.fetchall()
            return [{"id_menu": row[0], "fecha": row[1], "tipo": row[2]} for row in rows]
        except Exception as e:
            print("Error obteniendo menús:", e)
            return []
