from PyQt5.QtWidgets import QMainWindow

class MenuProfesor(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Menú del Profesor")
        self.usuario = usuario
        self.init_ui()

    def init_ui(self):
        # Aquí puedes agregar los elementos de la interfaz gráfica
        pass
    
