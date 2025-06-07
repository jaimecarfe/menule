from src.modelo.logica.LogicaUsuario import LogicaUsuario
from src.modelo.logica.LogicaReserva import LogicaReserva
from src.modelo.logica.LogicaIncidencia import LogicaIncidencia
from src.modelo.logica.LogicaPago import LogicaPago
from src.modelo.logica.LogicaTicket import LogicaTicket
from src.modelo.logica.LogicaMenu import LogicaMenu
from src.modelo.logica.LogicaEstadistica import LogicaEstadistica
from src.modelo.logica.LogicaConfiguracion import LogicaConfiguracion
from src.modelo.logica.LogicaIngrediente import LogicaIngrediente

class BussinessObject:
    def __init__(self):
        self.usuario_service = LogicaUsuario()
        self.reserva_service = LogicaReserva()
        self.incidencia_service = LogicaIncidencia()
        self.pago_service = LogicaPago()
        self.ticket_service = LogicaTicket()
        self.menu_service = LogicaMenu()
        self.estadistica_service = LogicaEstadistica()
        self.configuracion_service = LogicaConfiguracion()
        self.ingrediente_service = LogicaIngrediente()