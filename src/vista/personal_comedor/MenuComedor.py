from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from src.controlador.ControladorComedor import ControladorComedor
from src.controlador.ControladorEstudiante import ControladorEstudiante
from src.modelo.BussinessObject import BussinessObject


class MenuComedor(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Menú del Personal de Comedor")
        self.usuario = usuario
        self.init_ui()

    def init_ui(self):
        # Aquí puedes agregar los elementos de la interfaz gráfica
        pass

    def cargar_reservas(self):
        reservas = self.controlador.obtener_reservas()
        self.tabla.setRowCount(0)
        for r in reservas:
            row_position = self.tabla.rowCount()
            self.tabla.insertRow(row_position)
            self.tabla.setItem(row_position, 0, QTableWidgetItem(str(r["id_reserva"])))
            self.tabla.setItem(row_position, 1, QTableWidgetItem(r["correo"]))
            self.tabla.setItem(row_position, 2, QTableWidgetItem(r["fecha"]))
            self.tabla.setItem(row_position, 3, QTableWidgetItem(", ".join(r["platos"])))
            self.tabla.setItem(row_position, 4, QTableWidgetItem(r["estado"]))
