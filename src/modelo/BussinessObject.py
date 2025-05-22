from src.modelo.dao.UserDao import UserDao
from src.modelo.dao.ReservaDao import ReservaDao
from src.modelo.dao.MenuDao import MenuDao
from src.modelo.dao.PlatoDao import PlatoDao
from src.modelo.dao.TicketDao import TicketDao
from src.modelo.dao.PagoDao import PagoDao
from src.modelo.dao.IncidenciaDao import IncidenciaDao
from src.modelo.dao.IngredienteDao import IngredienteDao
from src.modelo.dao.EstadisticaDao import EstadisticaDao

from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UserVo import UserVo
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.vo.IncidenciaVo import IncidenciaVo
from src.modelo.vo.TicketVo import TicketVo
from src.modelo.vo.PagoVo import PagoVo

import bcrypt

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
        return user_dao.insert(user)

    def actualizarSaldo(self, idUser: int, nuevo_saldo: float) -> bool:
        return UserDao().update_saldo(idUser, nuevo_saldo)

    def obtenerUsuarioPorCorreo(self, correo: str) -> UserVo | None:
        return UserDao().find_by_correo(correo)

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

    # --- Estadísticas ---
    def obtenerEstadisticasDiarias(self):
        return EstadisticaDao().obtener_diarias()