from src.modelo.dao.UserDao import UserDao
from src.modelo.dao.EstudianteDao import EstudianteDao
from src.modelo.dao.ProfesorDao import ProfesorDao
from src.modelo.dao.PersonalComedorDao import PersonalComedorDao
from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UserVo import UserVo
from src.modelo.vo.EstudianteVo import EstudianteVo
from src.modelo.vo.ProfesorVo import ProfesorVo
from src.modelo.vo.PersonalComedorVo import PersonalComedorVo
from src.modelo.Sesion import Sesion
from datetime import date
import bcrypt

class LogicaUsuario:
    def __init__(self):
        self.user_dao = UserDao()
        self.estudiante_dao = EstudianteDao()
        self.profesor_dao = ProfesorDao()
        self.personal_comedor_dao = PersonalComedorDao()

    def comprobar_login(self, loginVO: LoginVO) -> UserVo | None:
        user = self.user_dao.find_by_correo(loginVO.correo)
        if user and bcrypt.checkpw(loginVO.contrasena.encode(), user.contrasena.encode()):
            return user
        return None

    def registrar_usuario(self, user: UserVo) -> int | None:
        hashed_pw = bcrypt.hashpw(user.contrasena.encode(), bcrypt.gensalt())
        user.contrasena = hashed_pw.decode()
        user.fecha_alta = date.today()
        id_user = self.user_dao.insert(user)

        if id_user:
            user.idUser = id_user
            if user.rol == "estudiante":
                estudiante_vo = EstudianteVo(id_usuario=id_user, grado_academico=user.grado_academico,
                                             tui_numero=user.tui, saldo=user.saldo)
                self.estudiante_dao.insert(estudiante_vo)
            elif user.rol == "profesor":
                profesor_vo = ProfesorVo(id_usuario=id_user, grado_academico=user.grado_academico,
                                         tui_numero=user.tui, saldo=user.saldo)
                self.profesor_dao.insert(profesor_vo)
            elif user.rol == "personal_comedor":
                comedor_vo = PersonalComedorVo(id_usuario=id_user, fecha_contratacion=user.fecha_alta,
                                               especialidad=user.especialidad)
                self.personal_comedor_dao.insert(comedor_vo)
            return id_user
        return None

    def obtener_usuario_por_correo(self, correo: str) -> UserVo | None:
        return self.user_dao.find_by_correo(correo)

    def buscar_por_dni(self, dni: str) -> UserVo | None:
        return self.user_dao.buscar_por_dni(dni)

    def actualizar_saldo(self, id_usuario: int, nuevo_saldo: float) -> bool:
        return self.user_dao.update_saldo(id_usuario, nuevo_saldo)

    def obtener_saldo(self, id_usuario: int):
        return self.user_dao.obtener_saldo(id_usuario)

    def eliminar_usuario_fisico(self, id_usuario: int) -> bool | str:
        return self.user_dao.eliminar_usuario_fisico(id_usuario)

    def dar_de_baja_usuario(self, id_usuario: int) -> bool | str:
            return self.user_dao.eliminar_usuario_logico(id_usuario)

    def dar_de_baja_y_cerrar_sesion(self, id_usuario: int) -> bool | str:
        resultado = self.dar_de_baja_usuario(id_usuario)
        from src.modelo.Sesion import Sesion
        Sesion().cerrar_sesion()
        return resultado

    def actualizar_usuario(self, id_usuario: int, campo: str, nuevo_valor) -> bool:
        return self.user_dao.actualizar_campo_usuario(id_usuario, campo, nuevo_valor)

    def listar_usuarios(self) -> list[UserVo]:
        return self.user_dao.listarUsuarios()

    def obtener_usuario_por_id(self, id_usuario: int) -> UserVo | None:
        return self.user_dao.get_by_id(id_usuario)

