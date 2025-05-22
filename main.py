from PyQt5.QtWidgets import QApplication
from src.vista.Login import Login
from src.vista.Registro import Registro
from vista.estudiante.MenuEstudiante import MenuEstudiante
from src.vista.administrador.AdminPanel import AdminPanel
from src.modelo.BussinessObject import BussinessObject
from src.controlador.ControladorPrincipal import ControladorPrincipal
from src.vista.profesor.MenuProfesor import MenuProfesor
from src.vista.personal_comedor.MenuComedor import MenuComedor
from src.vista.visitante.MenuVisitante import MenuVisitante
from src.vista.estudiante.MenuEstudiante import MenuEstudiante

def mostrar_menu_por_rol(usuario):
    if usuario.rol == "estudiante":
        menu = MenuEstudiante(usuario)
        menu.show()
    elif usuario.rol == "profesor":
        print("Mostrar menú de profesor")
        # menu = MenuProfesor(usuario)
        # menu.show()
    elif usuario.rol == "personal_comedor":
        print("Mostrar menú del personal de comedor")
        # menu = MenuComedor(usuario)
        # menu.show()
    elif usuario.rol == "visitante":
        print("Mostrar menú del visitante")
        # menu = MenuVisitante(usuario)
        # menu.show()
    elif usuario.rol == "administrador":
        panel = AdminPanel(usuario)
        panel.show()
    else:
        print(f"⚠️ Rol no soportado: {usuario.rol}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    modelo = BussinessObject()

    # Ventana de Login
    login_window = Login()
    controlador = ControladorPrincipal(login_window, modelo)
    login_window.controlador = controlador

    def on_login_exitoso(usuario):
        login_window.close()
        mostrar_menu_por_rol(usuario)

    controlador.on_login_exitoso = on_login_exitoso

    def abrir_registro():
        login_window.close()
        registro = Registro()
        registro.show()

    login_window.abrir_registro = abrir_registro

    login_window.show()
    sys.exit(app.exec())