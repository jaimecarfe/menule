from PyQt5.QtWidgets import QApplication
from src.vista.WelcomePanel import WelcomePanel
from src.vista.Login import Login
from src.vista.Registro import Registro
from src.vista.estudiante.MenuEstudiante import MenuEstudiante
from src.vista.administrador.AdminPanel import AdminPanel
from src.vista.profesor.MenuProfesor import MenuProfesor
from src.vista.personal_comedor.MenuComedor import MenuComedor
from src.vista.visitante.MenuVisitante import MenuVisitante

from src.modelo.BussinessObject import BussinessObject
from src.controlador.ControladorPrincipal import ControladorPrincipal
from src.modelo.dao.UserDao import UserDao
from src.modelo.vo.UserVo import UserVo
import bcrypt
from datetime import date

class App:
    def __init__(self):
        self.app = QApplication([])
        self.modelo = BussinessObject()
        self.crear_admin_por_defecto()

        # Mostrar WelcomePanel como pantalla inicial
        self.welcome_window = WelcomePanel()
        self.welcome_window.btnContinuar.clicked.connect(self.abrir_login)
        self.welcome_window.show()

    def crear_admin_por_defecto(self):
        admin_email = "admin@menule.com"
        admin_contra = "admin123"

        user_dao = UserDao()
        if not user_dao.find_by_correo(admin_email):
            hash_pw = bcrypt.hashpw(admin_contra.encode(), bcrypt.gensalt()).decode()
            admin = UserVo(
                idUser=None,
                nombre="Admin",
                apellido="MenULE",
                correo=admin_email,
                contrasena=hash_pw,
                rol="administrador",
                saldo=0.0,
                tui=None,
                dni="00000000A",
                telefono="000000000",
                fecha_alta=date.today(),
                activo=True
            )
            user_dao.insert(admin)

    def abrir_login(self):
        self.welcome_window.close()
        self.login_window = Login()
        self.controlador = ControladorPrincipal(self.login_window, self.modelo)
        self.login_window.controlador = self.controlador
        self.login_window.abrir_registro = self.abrir_registro
        self.controlador.on_login_exitoso = self.mostrar_menu_por_rol
        self.login_window.show()

    def abrir_registro(self):
        self.login_window.hide()
        self.registro_window = Registro(volver_a=self.login_window)
        self.registro_window.controlador = self.controlador
        self.registro_window.show()

    def mostrar_menu_por_rol(self, usuario):
        self.login_window.close()
        if usuario.rol == "estudiante":
            self.ventana_actual = MenuEstudiante(usuario)
        elif usuario.rol == "profesor":
            self.ventana_actual = MenuProfesor(usuario)
        elif usuario.rol == "personal_comedor":
            self.ventana_actual = MenuComedor(usuario)
        elif usuario.rol == "visitante":
            self.ventana_actual = MenuVisitante(usuario)
        elif usuario.rol == "administrador":
            self.ventana_actual = AdminPanel(usuario)
            self.ventana_actual.callback_cerrar_sesion = self.abrir_login
        else:
            print(f"Rol no soportado: {usuario.rol}")
            return
        self.ventana_actual.show()

    def run(self):
        self.app.exec()

if __name__ == "__main__":
    app_instance = App()
    app_instance.run()
