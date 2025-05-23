from PyQt5.QtWidgets import QMainWindow

class MenuComedor(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Menú del Personal de Comedor")
        self.usuario = usuario
        self.init_ui()

    def init_ui(self):
        # Aquí puedes agregar los elementos de la interfaz gráfica
        pass