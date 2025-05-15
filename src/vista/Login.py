from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

# Cargar la interfaz generada desde el archivo .ui
Form, Window = uic.loadUiType("./src/vista/ui/VistaLogging.ui")

class Login(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets
        self._controlador = None
        # Conectar el botón a la función
        self.pushButton_aceptar.clicked.connect(self.on_button_click)
        self.setWindowOpacity(1.0)
        self.setWindowTitle("MenULE - Iniciar Sesión")
        self.resize(432, 505)


    def on_button_click(self):
        print("Botón presionado")
        texto_area = self.lineEdit_usuario.text()
        print("El texto es: ")
        print(texto_area)
        self._controlador.login(texto_area)

    @property
    def controlador(self):
        return self._controlador
    @controlador.setter
    def controlador(self, controlador):
        self._controlador = controlador

#pyrcc6 recursos.qrc -o recursos_rc.py