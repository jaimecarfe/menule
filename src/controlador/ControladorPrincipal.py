from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UserVo import UserVo
from src.modelo.BussinessObject import BussinessObject
from src.modelo.Sesion import Sesion

class ControladorPrincipal:
    def __init__(self, vista):
        self._vista = vista
        self._modelo = BussinessObject()
        self.on_login_exitoso = None

    def login(self, correo, contrasena):
        loginVO = LoginVO(correo, contrasena)
        usuario = self._modelo.usuario_service.comprobar_login(loginVO)
        if usuario:
            Sesion().set_usuario(usuario)
            if self.on_login_exitoso:
                self.on_login_exitoso(usuario)
            return usuario
        return None

    def insertar_usuario(self, userVO: UserVo):
        id_nuevo = self._modelo.usuario_service.registrar_usuario(userVO)
        if id_nuevo:
            print(f"Usuario registrado con ID: {id_nuevo}")
            return True
        else:
            return False

    def get_usuario_actual(self):
        return Sesion().get_usuario()
    
    def obtener_usuario_por_correo(self, correo: str) -> UserVo | None:
        return self._modelo.usuario_service.obtener_usuario_por_correo(correo)
    
    def buscar_usuario_por_dni(self, dni: str) -> UserVo | None:
        return self._modelo.usuario_service.buscar_por_dni(dni)
