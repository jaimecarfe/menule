# src/modelo/logica/LogicaReserva.py
from src.modelo.dao.ReservaDao import ReservaDao
from src.modelo.dao.UserDao import UserDao
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.dao.MenuDao import MenuDao
from datetime import datetime

class LogicaReserva:
    def __init__(self, reserva_dao=None, user_dao=None):
        # Permitimos inyección de dependencias para facilitar pruebas unitarias
        self.reserva_dao = reserva_dao or ReservaDao()
        self.user_dao = user_dao or UserDao()

    def crear_reserva(self, reservaVO: ReservaVo) -> dict:
        """Valida una reserva simple en base al Value Object recibido."""
        if not reservaVO or not reservaVO.id_usuario or not reservaVO.id_menu:
            return {"success": False, "message": "Datos de reserva incompletos o inválidos."}
            
        id_reserva = self.reserva_dao.insert(reservaVO)
        if id_reserva:
            return {"success": True, "id_reserva": id_reserva, "message": "Reserva simple creada con éxito."}
        return {"success": False, "message": "Error interno al insertar la reserva básica."}

    def crear_reserva_completa(self, id_usuario, fecha, primero, segundo, postre):
        """Regla de Negocio: Valida parámetros y fechas antes de agendar un menú completo."""
        try:
            # Validar que la fecha no sea pasada
            fecha_limite = datetime.strptime(fecha, "%Y-%m-%d").date()
            if fecha_limite < datetime.today().date():
                return {"success": False, "message": "No se permiten reservas para fechas pasadas."}
        except ValueError:
            return {"success": False, "message": "Formato de fecha inválido. Use AAAA-MM-DD."}

        if not primero or not segundo or not postre:
            return {"success": False, "message": "Debe seleccionar un primer plato, segundo plato y postre."}

        id_reserva = self.reserva_dao.crear_reserva_completa_por_fecha(
            id_usuario, fecha, primero, segundo, postre
        )
        
        if id_reserva:
            return {"success": True, "id_reserva": id_reserva, "message": "Reserva de menú procesada correctamente."}
        return {"success": False, "message": "No se pudo procesar la reserva. Verifique que el menú exista para esa fecha."}

    def crear_reserva_anonima(self, fecha, primero, segundo, postre):
        """Regla de Negocio: Valida parámetros para comensales anónimos/visitantes."""
        try:
            fecha_limite = datetime.strptime(fecha, "%Y-%m-%d").date()
            if fecha_limite < datetime.today().date():
                return {"success": False, "message": "No se permiten reservas anónimas en fechas pasadas."}
        except ValueError:
            return {"success": False, "message": "Formato de fecha inválido."}

        id_reserva = self.reserva_dao.crear_reserva_anonima(fecha, primero, segundo, postre)
        if id_reserva:
            return {"success": True, "id_reserva": id_reserva, "message": "Reserva anónima generada con éxito."}
        return {"success": False, "message": "Error al procesar la reserva anónima."}

    def obtener_ultima_reserva_id(self, id_usuario):
        return self.reserva_dao.obtener_ultima_reserva_id(id_usuario)

    def listar_reservas(self):
        return self.reserva_dao.listar_reservas()

    def obtener_reservas_estudiante(self, id_usuario):
        if not id_usuario or id_usuario <= 0:
            return []
        return self.reserva_dao.obtener_por_usuario(id_usuario)

    def get_reservas_completas(self):
        reservas = self.reserva_dao.get_all()
        resultado = []
        for r in reservas:
            usuario = self.user_dao.get_by_id(r.id_usuario)
            platos = self.reserva_dao.obtener_platos_de_reserva(r.id_reserva)
            resultado.append({
                "id_reserva": r.id_reserva,
                "correo": usuario.correo if usuario else "Desconocido",
                "fecha": r.fecha_reserva,
                "estado": r.estado,
                "platos": platos
            })
        return resultado
    
    def obtener_reservas_confirmadas(self):
        return self.reserva_dao.obtener_reservas_confirmadas()
    
    def crear_reserva_por_fecha(self, id_usuario, fecha):
        """Regla de Negocio: Busca el menú del día y automatiza una reserva estándar confirmada."""
        try:
            fecha_limite = datetime.strptime(fecha, "%Y-%m-%d").date()
            if fecha_limite < datetime.today().date():
                return {"success": False, "message": "No puedes reservar un menú de un día pasado."}
        except ValueError:
            return {"success": False, "message": "Formato de fecha inválido."}

        menu_dao = MenuDao()
        id_menu = menu_dao.obtener_id_menu_por_fecha(fecha)
        if not id_menu:
            return {"success": False, "message": f"No se encontró ningún menú programado para la fecha: {fecha}."}

        reserva = ReservaVo(
            id_reserva=None,
            id_usuario=id_usuario,
            id_menu=id_menu,
            fecha_reserva=datetime.now(),
            estado="confirmada"
        )
        
        id_reserva = self.reserva_dao.insert(reserva)
        if id_reserva:
            return {"success": True, "id_reserva": id_reserva, "message": "Reserva por fecha generada de manera exitosa."}
        return {"success": False, "message": "Error interno al confirmar la reserva automatizada."}

    def obtener_reservas_con_detalle(self, estados=('confirmada', 'pendiente')):
        return self.reserva_dao.obtener_reservas_con_detalle(estados)

    def actualizar_estado_reserva(self, id_reserva, bit):
        if not id_reserva or id_reserva <= 0:
            return False
        return self.reserva_dao.actualizar_estado_reserva(id_reserva, bit)