from typing import Optional
from pydantic import BaseModel
import reflex as rx

from app.database import SessionLocal
from app.services.stock_service import StockService
from app.states.auth_state import AppState


class IngredienteSchema(BaseModel):
    id_ingrediente: int
    nombre: str
    unidad_medida: str
    stock_actual: float
    stock_minimo: float
    es_critico: bool
    alergeno: bool
    tipo_alergeno: str


class StockState(rx.State):
    ingredientes: list[IngredienteSchema] = []
    search_text: str = ""
    filtro_critico: bool = False

    # Métricas
    total_ingredientes: int = 0
    stock_critico_count: int = 0

    # Modal para pedir/reabastecer stock
    show_modal_pedido: bool = False
    ingrediente_seleccionado: Optional[IngredienteSchema] = None
    cantidad_a_pedir: float = 10.0

    # Modal y campos para AÑADIR NUEVO INGREDIENTE
    show_modal_nuevo_ingrediente: bool = False
    nuevo_nombre: str = ""
    nuevo_stock_actual: float = 20.0
    nueva_unidad: str = "Kg"
    nuevo_stock_minimo: float = 10.0
    nuevo_alergeno: bool = False
    nuevo_tipo_alergeno: str = "Ninguno"

    @rx.event
    def set_search_text(self, value: str):
        self.search_text = value
        return StockState.cargar_stock

    @rx.event
    def set_cantidad_a_pedir(self, value: str):
        try:
            self.cantidad_a_pedir = float(value)
        except ValueError:
            self.cantidad_a_pedir = 0.0

    @rx.event
    def set_show_modal_pedido(self, value: bool):
        self.show_modal_pedido = value

    @rx.event
    def set_show_modal_nuevo_ingrediente(self, value: bool):
        self.show_modal_nuevo_ingrediente = value

    @rx.event
    def set_nuevo_nombre(self, value: str):
        self.nuevo_nombre = value

    @rx.event
    def set_nueva_unidad(self, value: str):
        self.nueva_unidad = value

    @rx.event
    def set_nuevo_stock_actual(self, value: str):
        try:
            self.nuevo_stock_actual = float(value) if value else 0.0
        except ValueError:
            self.nuevo_stock_actual = 0.0

    @rx.event
    def set_nuevo_stock_minimo(self, value: str):
        try:
            self.nuevo_stock_minimo = float(value) if value else 0.0
        except ValueError:
            self.nuevo_stock_minimo = 0.0

    @rx.event
    def set_nuevo_tipo_alergeno(self, value: str):
        self.nuevo_tipo_alergeno = value
        self.nuevo_alergeno = value != "Ninguno"

    @rx.event
    def abrir_modal_nuevo(self):
        self.nuevo_nombre = ""
        self.nuevo_stock_actual = 20.0
        self.nueva_unidad = "Kg"
        self.nuevo_stock_minimo = 10.0
        self.nuevo_tipo_alergeno = "Ninguno"
        self.nuevo_alergeno = False
        self.show_modal_nuevo_ingrediente = True

    @rx.event
    async def crear_nuevo_ingrediente(self):
        """Guarda el ingrediente en la BD y recarga la tabla en pantalla."""
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not (app_state.is_admin or app_state.is_cocina):
            return rx.window_alert("No tienes permisos para realizar esta acción.")

        if self.nuevo_nombre.strip():
            with SessionLocal() as db:
                if hasattr(StockService, "crear_ingrediente"):
                    StockService.crear_ingrediente(
                        db,
                        nombre=self.nuevo_nombre.strip(),
                        unidad_medida=self.nueva_unidad.strip(),
                        stock_actual=self.nuevo_stock_actual,
                        stock_minimo=self.nuevo_stock_minimo,
                        alergeno=self.nuevo_alergeno,
                        tipo_alergeno=self.nuevo_tipo_alergeno,
                    )
        self.show_modal_nuevo_ingrediente = False
        return StockState.cargar_stock

    @rx.event
    async def cargar_stock(self):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in:
            self.ingredientes = []
            return rx.redirect("/")
        if not (app_state.is_admin or app_state.is_cocina):
            self.ingredientes = []
            app_state.agregar_notificacion("Acceso denegado: Se requieren permisos de cocina o administrador.")
            return rx.redirect("/home")

        with SessionLocal() as db:
            items = StockService.get_ingredientes(db, self.search_text)

            lista = []
            criticos = 0

            for i in items:
                actual = float(i.stock_actual or 0)
                minimo = float(i.stock_minimo or 0)
                es_critico = actual <= minimo

                if es_critico:
                    criticos += 1

                if self.filtro_critico and not es_critico:
                    continue

                lista.append(
                    IngredienteSchema(
                        id_ingrediente=i.id_ingrediente,
                        nombre=i.nombre,
                        unidad_medida=i.unidad_medida or "Kg",
                        stock_actual=actual,
                        stock_minimo=minimo,
                        es_critico=es_critico,
                        alergeno=i.alergeno or False,
                        tipo_alergeno=i.tipo_alergeno or "Ninguno",
                    )
                )

            self.ingredientes = lista
            self.total_ingredientes = len(items)
            self.stock_critico_count = criticos

    @rx.event
    def toggle_filtro_critico(self):
        self.filtro_critico = not self.filtro_critico
        return StockState.cargar_stock

    @rx.event
    def abrir_modal_reabastecer(self, ing: IngredienteSchema):
        self.ingrediente_seleccionado = ing
        self.cantidad_a_pedir = 10.0
        self.show_modal_pedido = True

    @rx.event
    async def confirmar_pedido_stock(self):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not (app_state.is_admin or app_state.is_cocina):
            return rx.window_alert("No tienes permisos para realizar esta acción.")

        if self.ingrediente_seleccionado and self.cantidad_a_pedir > 0:
            with SessionLocal() as db:
                StockService.reabastecer_stock(
                    db,
                    self.ingrediente_seleccionado.id_ingrediente,
                    self.cantidad_a_pedir,
                )
        self.show_modal_pedido = False
        return StockState.cargar_stock