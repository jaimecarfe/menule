from PyQt5.QtWidgets import QMainWindow

class MenuEstudiante(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Menú del Estudiante")
        self.usuario = usuario
        self.init_ui()

    def init_ui(self):
        # Aquí puedes agregar los elementos de la interfaz gráfica
        pass