from src.modelo.dao.UserDao import UserDao
from src.modelo.dao.EstudianteDao import EstudianteDao
from src.modelo.dao.ProfesorDao import ProfesorDao
from src.modelo.dao.PersonalComedorDao import PersonalComedorDao
from src.modelo.dao.EstadisticaDao import EstadisticaDao
from src.modelo.dao.ConfiguracionDao import ConfiguracionDao
from src.modelo.dao.ReservaDao import ReservaDao
from src.modelo.dao.TicketDao import TicketDao
from src.modelo.dao.MenuDao import MenuDao
from src.modelo.dao.PagoDao import PagoDao
from src.modelo.dao.IncidenciaDao import IncidenciaDao



"""
from src.modelo.dao.PlatoDao import PlatoDao
from src.modelo.dao.IncidenciaDao import IncidenciaDao
from src.modelo.dao.IngredienteDao import IngredienteDao
"""


from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UserVo import UserVo
from src.modelo.vo.EstudianteVo import EstudianteVo
from src.modelo.vo.ProfesorVo import ProfesorVo
from src.modelo.vo.PersonalComedorVo import PersonalComedorVo
from src.modelo.vo.EstadisticaVo import EstadisticaVo
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.vo.TicketVo import TicketVo
from src.modelo.vo.PagoVo import PagoVo
from src.modelo.vo.IncidenciaVo import IncidenciaVo

"""
from src.modelo.vo.IncidenciaVo import IncidenciaVo
"""


import bcrypt
from datetime import date


class BussinessObject:
    def __init__(self):
        self.user_dao = UserDao()
        self.estadistica_dao = EstadisticaDao()
        self.estudiante_dao = EstudianteDao()
        self.profesor_dao = ProfesorDao()
        self.personal_comedor_dao = PersonalComedorDao()
        self.reserva_dao = ReservaDao()
        self.ticket_dao = TicketDao()
        self.incidencia_dao = IncidenciaDao()


    # --- Usuarios ---
    def comprobarLogin(self, loginVO: LoginVO) -> UserVo | None:
        user_dao = UserDao()
        user = user_dao.find_by_correo(loginVO.correo)
        if user and bcrypt.checkpw(loginVO.contrasena.encode(), user.contrasena.encode()):
            return user
        return None

    def registrarUsuario(self, user: UserVo) -> int | None:
        user_dao = UserDao()
        hashed_pw = bcrypt.hashpw(user.contrasena.encode(), bcrypt.gensalt())
        user.contrasena = hashed_pw.decode()
        user.fecha_alta = date.today()
        id_user = user_dao.insert(user)

        if id_user:
            user.idUser = id_user
            if user.rol == "estudiante":
                estudiante_dao = self.estudiante_dao
                estudiante_vo = EstudianteVo(id_usuario=id_user, grado_academico=user.grado_academico, tui_numero=user.tui, saldo=user.saldo)
                estudiante_dao.insert(estudiante_vo)
            elif user.rol == "profesor":
                profesor_dao = self.profesor_dao
                profesor_vo = ProfesorVo(id_usuario=id_user, grado_academico=user.grado_academico, tui_numero= user.tui, saldo=user.saldo)
                profesor_dao.insert(profesor_vo)
            elif user.rol == "personal_comedor":
                comedor_dao = self.personal_comedor_dao
                comedor_vo = PersonalComedorVo(id_usuario=id_user, fecha_contratacion=user.fecha_alta, especialidad=user.especialidad)
                comedor_dao.insert(comedor_vo)
            return id_user
        return None

    def actualizarSaldo(self, idUser: int, nuevo_saldo: float) -> bool:
        return self.user_dao.update_saldo(idUser, nuevo_saldo)
    
    def obtener_saldo(self, id_usuario):
        return self.estudiante_dao.obtener_saldo(id_usuario)

    def obtenerUsuarioPorCorreo(self, correo: str) -> UserVo | None:
        return self.user_dao.find_by_correo(correo)
    
    def listarUsuarios(self) -> list[UserVo]:
        return self.user_dao.select()
    
    def eliminarUsuario(self, id_usuario: int) -> bool:
        return self.user_dao.eliminar_usuario_fisico(id_usuario)    

    def listarUsuarios(self):
        return self.user_dao.listarUsuarios()
    
    def darDeBajaUsuario(self, id_usuario: int) -> bool:
        return self.user_dao.eliminar_usuario_logico(id_usuario)
    
    def actualizarUsuario(self, id_usuario: int, campo: str, nuevo_valor) -> bool:
        return self.user_dao.actualizar_campo_usuario(id_usuario, campo, nuevo_valor)

    def find_user_by_email(self, email: str) -> UserVo | None:
        return self.user_dao.find_by_correo(email)
    
    def buscar_por_dni(self, dni: str) -> UserVo | None:
        return self.user_dao.buscar_por_dni(dni)
    
    def actualizarSaldoEstudiante(self, id_usuario, nuevo_saldo):
        return self.estudiante_dao.actualizar_saldo(id_usuario, nuevo_saldo)
    
    def actualizarSaldoProfesor(self, id_usuario, nuevo_saldo):
        return self.profesor_dao.actualizar_saldo(id_usuario, nuevo_saldo)

    def crearReservaCompleta(self, id_usuario, fecha, primero, segundo, postre):
        return self.reserva_dao.crear_reserva_completa_por_fecha(id_usuario, fecha, primero, segundo, postre)

    def crearReservaAnonima(self, fecha, primero, segundo, postre):
        return self.reserva_dao.crear_reserva_anonima(fecha, primero, segundo, postre)
    
    def insertar_reserva(self, reserva_vo):
        return self._reservaDao.insert(reserva_vo)

    
    # --- Estadísticas ---
    def obtenerEstadisticas(self, tipo):
        dao = self.estadistica_dao
        if tipo == 'Pagos':
            datos = dao.obtener_pagos()
        elif tipo == 'Incidencias':
            datos = dao.obtener_incidencias()
        elif tipo == 'Menús':
            datos = dao.obtener_menus()
        elif tipo == 'Reservas':
            datos = dao.obtener_reservas()
        else:
            datos = []
        
        return EstadisticaVo(tipo, datos)

    # --- Configuraciones ---
    def obtenerConfiguraciones(self):
        return ConfiguracionDao().obtener_configuraciones()
    
    def guardarConfiguracion(self, clave: str, valor: str) -> bool:
        return ConfiguracionDao().guardar_configuracion(clave, valor)
    
    # --- Reservas ---
    def crearReserva(self, reservaVO: ReservaVo) -> int | None:
        return self.reserva_dao.insert(reservaVO)

    def obtenerUltimaReservaId(self, id_usuario):
        return self.reserva_dao.obtener_ultima_reserva_id(id_usuario)    


    # --- Tickets ---
    def generarTicket(self, ticketVO: TicketVo) -> int | None:
        return self.ticket_dao.insert(ticketVO)

    def validarTicket(self, codigo: str) -> bool:
        return self.ticket_dao.marcar_usado(codigo)
    
    # --- Menús ---
    def obtenerMenusDisponibles(self):
        return MenuDao().listar_disponibles()

    # --- Pagos ---
    def registrarPago(self, pagoVO: PagoVo) -> int | None:
        return PagoDao().insertar_pago(pagoVO)

    def obtenerPagosPorUsuario(self, id_usuario: int):
        return PagoDao().obtener_por_usuario(id_usuario)
    
    
    """

    # --- Platos ---
    def obtenerPlatosPorMenu(self, id_menu: int):
        return PlatoDao().buscar_por_menu(id_menu)
    """
    # --- Incidencias ---
    def reportarIncidencia(self, incidenciaVO: IncidenciaVo) -> int | None:
        return IncidenciaDao().insertar_incidencia(incidenciaVO)

    def listarIncidencias(self):
        return IncidenciaDao().listar_todas()

    def resolverIncidencia(self, id_incidencia: int, solucion: str) -> bool:
        return IncidenciaDao().resolver(id_incidencia, solucion)
    """
    # --- Ingredientes ---
    def consultarStockIngredientes(self):
        return IngredienteDao().listar()

    """

    def get_reservas_completas(self):
        reservas = self.reserva_dao.get_all()
        resultado = []
        for r in reservas:
            usuario = self.user_dao.get_by_id(r.id_usuario)
            platos = self.reserva_dao.obtener_platos_de_reserva(r.id_reserva)
            resultado.append({
                "id_reserva": r.id_reserva,
                "correo": usuario.correo,
                "fecha": r.fecha_reserva,
                "estado": r.estado,
                "platos": platos
            })
        return resultado
