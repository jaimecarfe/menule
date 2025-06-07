from src.modelo.dao.ReservaDao import ReservaDao
from src.modelo.dao.UserDao import UserDao
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.dao.MenuDao import MenuDao
from datetime import datetime


class LogicaReserva:
    def __init__(self):
        self.reserva_dao = ReservaDao()
        self.user_dao = UserDao()

    def crear_reserva(self, reservaVO: ReservaVo) -> int | None:
        return self.reserva_dao.insert(reservaVO)

    def crear_reserva_completa(self, id_usuario, fecha, primero, segundo, postre):
        return self.reserva_dao.crear_reserva_completa_por_fecha(id_usuario, fecha, primero, segundo, postre)

    def crear_reserva_anonima(self, fecha, primero, segundo, postre):
        return self.reserva_dao.crear_reserva_anonima(fecha, primero, segundo, postre)

    def obtener_ultima_reserva_id(self, id_usuario):
        return self.reserva_dao.obtener_ultima_reserva_id(id_usuario)

    def listar_reservas(self):
        return self.reserva_dao.listar_reservas()

    def obtener_reservas_estudiante(self, id_usuario):
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
        menu_dao = MenuDao()
        id_menu = menu_dao.obtener_id_menu_por_fecha(fecha)
        if not id_menu:
            return None

        reserva = ReservaVo(
            id_reserva=None,
            id_usuario=id_usuario,
            id_menu=id_menu,
            fecha_reserva=datetime.now(),
            estado="confirmada"
        )
        return self.reserva_dao.insert(reserva)

    def obtener_reservas_con_detalle(self, estados=('confirmada', 'pendiente')):
        return self.reserva_dao.obtener_reservas_con_detalle(estados)

    def actualizar_estado_reserva(self, id_reserva, bit):
        return self.reserva_dao.actualizar_estado_reserva(id_reserva, bit)

