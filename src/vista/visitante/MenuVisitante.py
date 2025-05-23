from PyQt5.QtWidgets import QMainWindow

class MenuVisitante(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Menú del Visitante")
        self.usuario = usuario
        self.init_ui()

    def init_ui(self):
        # Aquí puedes agregar los elementos de la interfaz gráfica
        pass