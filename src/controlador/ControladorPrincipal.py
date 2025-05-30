from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UserVo import UserVo
from src.modelo.BussinessObject import BussinessObject

class ControladorPrincipal:
    def __init__(self, vista, modelo: BussinessObject):
        self._vista = vista
        self._modelo = modelo
        self._usuario_actual = None
        self.on_login_exitoso = None

    def login(self, correo, contrasena):
        loginVO = LoginVO(correo, contrasena)
        usuario = self._modelo.comprobarLogin(loginVO)
        if usuario:
            self._usuario_actual = usuario
            if self.on_login_exitoso:
                self.on_login_exitoso(usuario)
            return usuario

    def insertar_usuario(self, userVO: UserVo):
        id_nuevo = self._modelo.registrarUsuario(userVO)
        if id_nuevo:
            print(f"Usuario registrado con ID: {id_nuevo}")
            return True
        else:
            return False

    def get_usuario_actual(self):
        return self._usuario_actual
    
    def obtener_usuario_por_correo(self, correo: str) -> UserVo | None:
        return self._modelo.obtenerUsuarioPorCorreo(correo)