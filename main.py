from PyQt5.QtWidgets import QApplication
from src.vista.Login import Login
from src.vista.Registro import Registro
from src.vista.estudiante.MenuEstudiante import MenuEstudiante
from src.vista.administrador.AdminPanel import AdminPanel
from src.vista.profesor.MenuProfesor import MenuProfesor
from src.vista.personal_comedor.MenuComedor import MenuComedor
from src.vista.visitante.MenuVisitante import MenuVisitante

from src.modelo.BussinessObject import BussinessObject
from src.controlador.ControladorPrincipal import ControladorPrincipal

class App:
    def __init__(self):
        self.app = QApplication([])
        self.modelo = BussinessObject()
        self.login_window = Login()
        self.controlador = ControladorPrincipal(self.login_window, self.modelo)
        self.login_window.controlador = self.controlador
        self.login_window.abrir_registro = self.abrir_registro
        self.controlador.on_login_exitoso = self.mostrar_menu_por_rol

    def abrir_registro(self):
        self.login_window.hide()
        self.registro_window = Registro(volver_a=self.login_window)
        self.registro_window.controlador = self.controlador
        self.registro_window.show()

    def mostrar_menu_por_rol(self, usuario):
        self.login_window.close()
        if usuario.rol == "estudiante":
            ventana = MenuEstudiante(usuario)
        elif usuario.rol == "profesor":
            ventana = MenuProfesor(usuario)
        elif usuario.rol == "personal_comedor":
            ventana = MenuComedor(usuario)
        elif usuario.rol == "visitante":
            ventana = MenuVisitante(usuario)
        elif usuario.rol == "administrador":
            ventana = AdminPanel(usuario)
        else:
            print(f"⚠️ Rol no soportado: {usuario.rol}")
            return
        ventana.show()

    def run(self):
        self.login_window.show()
        self.app.exec()

if __name__ == "__main__":
    app_instance = App()
    app_instance.run()
