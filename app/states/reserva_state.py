import reflex as rx
from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime

from app.database import SessionLocal
from sqlalchemy import cast, String
from app.services.reserva_service import ReservaService
from app.states.auth_state import AppState
from app.models import Reserva, Plato


class ReservaSchema(BaseModel):
    id_reserva: int
    id_usuario: int
    id_menu: int
    fecha_reserva: str
    estado: str
    estado_bit: Optional[int] = None
    correo_usuario: str = "Visitante"
    detalle_menu: str = "Sin detalles"
    platos_lista: List[str] = []  # Lista de nombres de platos elegidos


class ReservaState(rx.State):

    # DATOS
    reservas: List[ReservaSchema] = []
    search_text: str = ""
    is_loading: bool = False
    modo_vista: str = "admin"

    # Control del modal de detalle
    show_modal_detalle: bool = False
    reserva_seleccionada: Optional[ReservaSchema] = None

    # SETTERS
    def set_search_text(self, value: str):
        self.search_text = value

    def set_show_modal_detalle(self, value: bool):
        self.show_modal_detalle = value

    def set_modo_vista(self, value: Union[str, list[str]]):
        if isinstance(value, list):
            self.modo_vista = value[0] if value else "admin"
        else:
            self.modo_vista = value

    @rx.event
    def abrir_detalle(self, res: ReservaSchema):
        self.reserva_seleccionada = res
        self.show_modal_detalle = True

    @rx.event
    def cerrar_detalle(self):
        self.show_modal_detalle = False

    # CARGAR RESERVAS Y SUS PLATOS ESPECÍFICOS
    @rx.event
    async def load_reservas(self):
        self.is_loading = True
        app_state = await self.get_state(AppState)
        
        if not app_state.is_logged_in:
            self.reservas = []
            self.is_loading = False
            return rx.redirect("/")

        current_user_id = app_state.user_id
        if not current_user_id and getattr(app_state, "usuario_actual", None):
            current_user_id = getattr(app_state.usuario_actual, "id_usuario", None)

        with SessionLocal() as db:
            if app_state.is_admin or app_state.is_cocina:
                resultados = ReservaService.get_all(db, self.search_text)
            elif (app_state.is_estudiante or app_state.is_profesor) and current_user_id:
                query = db.query(Reserva).filter(Reserva.id_usuario == current_user_id)
                if self.search_text.strip():
                    patron = f"%{self.search_text.strip()}%"
                    query = query.filter(cast(Reserva.id_reserva, String).ilike(patron))
                resultados = query.order_by(Reserva.fecha_reserva.desc()).all()
            else:
                resultados = []

            self.reservas = [
                ReservaSchema(
                    id_reserva=r.id_reserva,
                    id_usuario=r.id_usuario or 0,
                    id_menu=r.id_menu,
                    fecha_reserva=r.fecha_reserva.strftime("%Y-%m-%d %H:%M") if hasattr(r.fecha_reserva, "strftime") else str(r.fecha_reserva),
                    estado=r.estado or "pendiente",
                    estado_bit=r.estado_bit,
                    correo_usuario=r.usuario.email if (r.usuario and r.id_usuario != 0) else "Visitante",
                    detalle_menu=f"Menú #{r.id_menu}",
                    # 🛠️ Extrae SOLO los platos guardados específicamente en esa reserva
                    platos_lista=[p.nombre for p in r.platos] if r.platos else ["Sin platos asociados"]
                )
                for r in resultados
            ]
        self.is_loading = False

    # REALIZAR RESERVA GUARDANDO LOS 3 PLATOS ELEGIDOS
    @rx.event
    async def realizar_reserva(self, id_menu: int, ids_platos: List[int]):
        """
        id_menu: ID del menú del día
        ids_platos: Lista con los IDs de los 3 platos elegidos (1º, 2º y Postre)
        """
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not app_state.user_id:
            return rx.window_alert("Debes iniciar sesión para realizar una reserva.")

        exito_pago = app_state.descontar_saldo_menu()
        if not exito_pago:
            return rx.window_alert("No tienes suficiente saldo en tu Monedero TUI.")

        with SessionLocal() as db:
            # Obtener los 3 platos de la BD
            platos_objetos = []
            if ids_platos:
                platos_objetos = db.query(Plato).filter(Plato.id_plato.in_(ids_platos)).all()

            nueva_reserva = Reserva(
                id_usuario=app_state.user_id,
                id_menu=id_menu,
                fecha_reserva=datetime.now(),
                estado="confirmada",
                estado_bit=False,
                platos=platos_objetos  # 👈 Asigna únicamente los 3 elegidos
            )
            db.add(nueva_reserva)
            db.commit()

        app_state.agregar_notificacion("¡Reserva realizada e importe descontado correctamente!")
        return ReservaState.load_reservas

    @rx.event
    async def marcar_recogida(self, id_reserva: int):
        with SessionLocal() as db:
            ReservaService.actualizar_estado(db, id_reserva, estado="recogida", estado_bit=1)
        
        plato_state = await self.get_state(AppState)
        plato_state.agregar_notificacion(f"Reserva #{id_reserva} marcada como RECOGIDA.")
        return ReservaState.load_reservas

    @rx.event
    async def marcar_cancelada(self, id_reserva: int):
        with SessionLocal() as db:
            ReservaService.actualizar_estado(db, id_reserva, estado="cancelada", estado_bit=0)
        
        plato_state = await self.get_state(AppState)
        plato_state.agregar_notificacion(f"Reserva #{id_reserva} ha sido CANCELADA.")
        return ReservaState.load_reservas