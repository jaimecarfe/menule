from src.modelo.dao.UserDao import UserDao
from src.modelo.dao.EstudianteDao import EstudianteDao
from src.modelo.dao.ProfesorDao import ProfesorDao
from src.modelo.dao.PersonalComedorDao import PersonalComedorDao
from src.modelo.dao.EstadisticaDao import EstadisticaDao
"""
from src.modelo.dao.ReservaDao import ReservaDao
from src.modelo.dao.MenuDao import MenuDao
from src.modelo.dao.PlatoDao import PlatoDao
from src.modelo.dao.TicketDao import TicketDao
from src.modelo.dao.PagoDao import PagoDao
from src.modelo.dao.IncidenciaDao import IncidenciaDao
from src.modelo.dao.IngredienteDao import IngredienteDao
"""
from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UserVo import UserVo
from src.modelo.vo.EstudianteVo import EstudianteVo
from src.modelo.vo.ProfesorVo import ProfesorVo
from src.modelo.vo.PersonalComedorVo import PersonalComedorVo
from src.modelo.vo.EstadisticaVo import EstadisticaVo
"""
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.vo.IncidenciaVo import IncidenciaVo
from src.modelo.vo.TicketVo import TicketVo
from src.modelo.vo.PagoVo import PagoVo
"""

import bcrypt
from datetime import date

class BussinessObject:
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
                estudiante_dao = EstudianteDao()
                estudiante_vo = EstudianteVo(id_usuario=id_user, grado_academico=user.grado_academico, tui_numero=user.tui, saldo=user.saldo)
                estudiante_dao.insert(estudiante_vo)
            elif user.rol == "profesor":
                profesor_dao = ProfesorDao()
                profesor_vo = ProfesorVo(id_usuario=id_user, grado_academico=user.grado_academico, saldo=user.saldo)
                profesor_dao.insert(profesor_vo)
            elif user.rol == "personal_comedor":
                comedor_dao = PersonalComedorDao()
                comedor_vo = PersonalComedorVo(id_usuario=id_user, fecha_contratacion=user.fecha_alta, especialidad=user.especialidad)
                comedor_dao.insert(comedor_vo)
            return id_user
        return None

    def actualizarSaldo(self, idUser: int, nuevo_saldo: float) -> bool:
        return UserDao().update_saldo(idUser, nuevo_saldo)

    def obtenerUsuarioPorCorreo(self, correo: str) -> UserVo | None:
        return UserDao().find_by_correo(correo)
    
    def listarUsuarios(self) -> list[UserVo]:
        return UserDao().select()
    
    def eliminarUsuario(self, id_usuario: int) -> bool:
        return UserDao().delete(id_usuario)    

    # --- Estadísticas ---
    def obtenerEstadisticas(self, tipo):
        dao = EstadisticaDao()
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
"""
    # --- Reservas ---
    def crearReserva(self, reservaVO: ReservaVo) -> int | None:
        return ReservaDao().insert(reservaVO)

    def cancelarReserva(self, id_reserva: int, motivo: str) -> bool:
        return ReservaDao().cancelar(id_reserva, motivo)

    def obtenerReservasPorUsuario(self, id_usuario: int) -> list:
        return ReservaDao().obtener_por_usuario(id_usuario)

    # --- Menús ---
    def obtenerMenusDisponibles(self):
        return MenuDao().listar_disponibles()

    # --- Platos ---
    def obtenerPlatosPorMenu(self, id_menu: int):
        return PlatoDao().buscar_por_menu(id_menu)

    # --- Tickets ---
    def generarTicket(self, ticketVO: TicketVo) -> int | None:
        return TicketDao().insert(ticketVO)

    def validarTicket(self, codigo: str) -> bool:
        return TicketDao().marcar_usado(codigo)

    # --- Pagos ---
    def registrarPago(self, pagoVO: PagoVo) -> int | None:
        return PagoDao().insert(pagoVO)

    def obtenerPagosPorUsuario(self, id_usuario: int):
        return PagoDao().obtener_por_usuario(id_usuario)

    # --- Incidencias ---
    def reportarIncidencia(self, incidenciaVO: IncidenciaVo) -> int | None:
        return IncidenciaDao().insert(incidenciaVO)

    def listarIncidencias(self):
        return IncidenciaDao().listar_todas()

    def resolverIncidencia(self, id_incidencia: int, solucion: str) -> bool:
        return IncidenciaDao().resolver(id_incidencia, solucion)

    # --- Ingredientes ---
    def consultarStockIngredientes(self):
        return IngredienteDao().listar()

"""