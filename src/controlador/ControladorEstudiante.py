# src/controlador/ControladorEstudiante.py
from src.modelo.Sesion import Sesion
from src.modelo.logica.LogicaReserva import LogicaReserva
from src.modelo.logica.LogicaMenu import LogicaMenu
from src.modelo.logica.LogicaUsuario import LogicaUsuario
from src.modelo.logica.LogicaIncidencia import LogicaIncidencia

class ControladorEstudiante:
    def __init__(self, reserva_service=None, menu_service=None, usuario_service=None, incidencia_service=None):
        # Desacoplamos los controladores entre sí y eliminamos el cuello de botella de BussinessObject
        self.reserva_service = reserva_service or LogicaReserva()
        self.menu_service = menu_service or LogicaMenu()
        self.usuario_service = usuario_service or LogicaUsuario()
        self.incidencia_service = incidencia_service or LogicaIncidencia()

    # === GESTIÓN DE MENÚS ===
    def obtener_menus_disponibles(self):
        return self.menu_service.obtener_menus_disponibles()

    def obtener_platos_por_fecha(self, fecha):
        if not fecha:
            return []
        return self.menu_service.obtener_menu_por_fecha(fecha)

    # === GESTIÓN DE RESERVAS ===
    # Centralizamos todas las peticiones de reserva directo a la lógica correspondiente
    def hacer_reserva(self, id_usuario: int, fecha: str):
        return self.reserva_service.crear_reserva_por_fecha(id_usuario, fecha)

    def reservar_menu(self, id_usuario, fecha, primero, segundo, postre):
        """Punto único de entrada para la reserva estructurada de menús del estudiante."""
        return self.reserva_service.crear_reserva_completa(id_usuario, fecha, primero, segundo, postre)

    def hacer_reserva_completa(self, id_usuario, fecha, primero, segundo, postre):
        # Redirigimos el método antiguo al formato unificado para mantener retrocompatibilidad
        return self.reservar_menu(id_usuario, fecha, primero, segundo, postre)

    def crear_reserva(self, reserva_vo):
        return self.reserva_service.crear_reserva(reserva_vo)

    def obtener_ultima_reserva_id(self, id_usuario):
        return self.reserva_service.obtener_ultima_reserva_id(id_usuario)

    def obtener_reservas_estudiante(self, id_usuario):
        return self.reserva_service.obtener_reservas_estudiante(id_usuario)

    # === GESTIÓN DE INCIDENCIAS ===
    def reportar_incidencia(self, incidencia_vo):
        return self.incidencia_service.reportar_incidencia(incidencia_vo)

    # === GESTIÓN DE USUARIO Y SALDO ===
    def obtener_saldo(self, id_usuario):
        return self.usuario_service.obtener_saldo(id_usuario)

    def actualizar_saldo(self, id_usuario, nuevo_saldo):
        return self.usuario_service.actualizar_saldo(id_usuario, nuevo_saldo)

    def dar_de_baja(self):
        usuario = Sesion().get_usuario()
        if usuario and hasattr(usuario, 'idUser'):
            return self.usuario_service.dar_de_baja_y_cerrar_sesion(usuario.idUser)
        return {"success": False, "message": "No hay una sesión activa de estudiante."}