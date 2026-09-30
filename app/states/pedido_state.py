import reflex as rx
from datetime import date
from pydantic import BaseModel
from typing import Optional

from app.database import SessionLocal
from app.services.stock_service import StockService
from app.services.pedido_service import PedidoService
from app.states.auth_state import AppState


class PedidoSchema(BaseModel):
    id_reserva: int
    fecha: str
    hora: str
    correo: str
    menu_resumen: str
    platos_lista: list[str]
    estado: str
    estado_bit: int


class PedidoState(rx.State):
    pedidos: list[PedidoSchema] = []
    search_text: str = ""
    filtro_estado: str = "todos"
    
    # Métricas
    total_hoy: int = 0
    pendientes_hoy: int = 0
    recogidos_hoy: int = 0

    # Modal para detalle del menú
    show_modal_detalle: bool = False
    pedido_seleccionado: Optional[PedidoSchema] = None

    def set_search_text(self, value: str):
        self.search_text = value

    def set_filtro_estado(self, value: str):
        self.filtro_estado = value

    def set_show_modal_detalle(self, value: bool):
        self.show_modal_detalle = value

    @rx.event
    async def cargar_pedidos(self):
        """Carga la lista de comandas y sus platos correspondientes."""
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in:
            self.pedidos = []
            return rx.redirect("/")
        if not (app_state.is_admin or app_state.is_cocina):
            self.pedidos = []
            app_state.agregar_notificacion("Acceso denegado: Se requieren permisos de cocina o administrador.")
            return rx.redirect("/home")

        with SessionLocal() as db:
            items = PedidoService.get_pedidos_comedor(
                db,
                search_text=self.search_text,
                estado_filtro=self.filtro_estado
            )

            lista = []
            c_total = 0
            c_pendientes = 0
            c_recogidos = 0

            for r in items:
                # Obtener la lista de platos asociados
                nombres_platos = PedidoService.get_platos_por_reserva(r)
                resumen_txt = ", ".join(nombres_platos)

                f_str = r.fecha_reserva.strftime("%Y-%m-%d") if r.fecha_reserva else ""
                h_str = r.fecha_reserva.strftime("%H:%M") if r.fecha_reserva else ""
                email_usr = r.usuario.email if r.usuario else "Usuario Desconocido"

                # Métricas
                c_total += 1
                if r.estado_bit == 1 or r.estado == "recogida":
                    c_recogidos += 1
                elif r.estado in ["confirmada", "pendiente"]:
                    c_pendientes += 1

                lista.append(
                    PedidoSchema(
                        id_reserva=r.id_reserva,
                        fecha=f_str,
                        hora=h_str,
                        correo=email_usr,
                        menu_resumen=resumen_txt,
                        platos_lista=nombres_platos,
                        estado=r.estado or "confirmada",
                        estado_bit=r.estado_bit or 0,
                    )
                )

            self.pedidos = lista
            self.total_hoy = c_total
            self.pendientes_hoy = c_pendientes
            self.recogidos_hoy = c_recogidos

    @rx.event
    def ver_detalle_menu(self, pedido: PedidoSchema):
        self.pedido_seleccionado = pedido
        self.show_modal_detalle = True

    @rx.event
    async def marcar_recogido(self, id_reserva: int):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not (app_state.is_admin or app_state.is_cocina):
            return rx.window_alert("No tienes permisos para realizar esta acción.")

        with SessionLocal() as db:
            PedidoService.actualizar_estado_pedido(db, id_reserva, "recogida")
            # Descontar automáticamente del inventario al entregar
            StockService.descontar_stock_por_reserva(db, id_reserva)
        return PedidoState.cargar_pedidos

    @rx.event
    async def marcar_cancelado(self, id_reserva: int):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not (app_state.is_admin or app_state.is_cocina):
            return rx.window_alert("No tienes permisos para realizar esta acción.")

        with SessionLocal() as db:
            PedidoService.actualizar_estado_pedido(db, id_reserva, "cancelada")
        return PedidoState.cargar_pedidos