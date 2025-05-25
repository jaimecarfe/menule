from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UserVo import UserVo
from src.modelo.BussinessObject import BussinessObject

class ControladorPrincipal:
    def __init__(self, vista, modelo: BussinessObject):
        self._vista = vista
        self._modelo = modelo  # instancia de BussinessObject
        self._usuario_actual = None
        self.on_login_exitoso = None  # Callback para redirigir según rol

    def login(self, correo, contrasena):
        loginVO = LoginVO(correo, contrasena)
        usuario = self._modelo.comprobarLogin(loginVO)
        if usuario:
            print(f"Login correcto: {usuario.nombre} ({usuario.rol})")
            self._usuario_actual = usuario
            if self.on_login_exitoso:
                self.on_login_exitoso(usuario)
            return True
        else:
            print("Credenciales incorrectas")
            return False

    def insertar_usuario(self, userVO: UserVo):
        if not self._modelo.obtenerUsuarioPorCorreo(userVO.correo):
            return self._modelo.registrarUsuario(userVO)
        else:
            print("Correo ya registrado")
            return None

    def get_usuario_actual(self):
        return self._usuario_actual