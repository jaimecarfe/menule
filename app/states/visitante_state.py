import reflex as rx
from datetime import date, datetime
from typing import List
from app.database import SessionLocal
from app.services.menu_service import MenuService
from app.services.reserva_service import ReservaService
from app.states.menu_state import PlatoSimpleSchema


class VisitanteState(rx.State):
    has_menu_hoy: bool = False
    id_menu_hoy: int = 0
    tipo_menu_hoy: str = ""
    fecha_menu_hoy: str = ""

    # Listas de platos dinámicas
    platos_primeros: List[PlatoSimpleSchema] = []
    platos_segundos: List[PlatoSimpleSchema] = []
    platos_postres: List[PlatoSimpleSchema] = []

    # Platos seleccionados (almacenamos el nombre del plato al seleccionar la tarjeta)
    plato_1_sel: str = ""
    plato_2_sel: str = ""
    postre_sel: str = ""

    # Modales y formulario
    precio_tarifa: float = 7.50
    show_modal_pago: bool = False
    show_modal_correo: bool = False
    email_visitante: str = ""
    error_correo: str = ""
    reserva_exito_id: int = 0
    is_loading: bool = False

    # Setters de selección de platos
    def set_plato_1_sel(self, valor: str):
        self.plato_1_sel = valor

    def set_plato_2_sel(self, valor: str):
        self.plato_2_sel = valor

    def set_postre_sel(self, valor: str):
        self.postre_sel = valor

    def set_email_visitante(self, valor: str):
        self.email_visitante = valor
        if self.error_correo:
            self.error_correo = ""

    @rx.event
    def cargar_menu_del_dia(self):
        """Carga el menú disponible de hoy para los visitantes."""
        self.is_loading = True
        with SessionLocal() as db:
            menu = MenuService.get_menu_del_dia(db, date.today())
            if menu:
                self.has_menu_hoy = True
                self.id_menu_hoy = menu.id_menu
                self.tipo_menu_hoy = menu.tipo.capitalize()
                self.fecha_menu_hoy = menu.fecha.strftime("%d/%m/%Y")

                self.platos_primeros = [
                    PlatoSimpleSchema(
                        id_plato=p.id_plato,
                        nombre=p.nombre,
                        tipo=str(p.tipo),
                        alergenos=p.alergenos or "Ninguno"
                    )
                    for p in menu.platos if str(p.tipo).lower() in ["primero", "1", "1º plato"] and getattr(p, "activo", True)
                ]
                self.platos_segundos = [
                    PlatoSimpleSchema(
                        id_plato=p.id_plato,
                        nombre=p.nombre,
                        tipo=str(p.tipo),
                        alergenos=p.alergenos or "Ninguno"
                    )
                    for p in menu.platos if str(p.tipo).lower() in ["segundo", "2", "2º plato"] and getattr(p, "activo", True)
                ]
                self.platos_postres = [
                    PlatoSimpleSchema(
                        id_plato=p.id_plato,
                        nombre=p.nombre,
                        tipo=str(p.tipo),
                        alergenos=p.alergenos or "Ninguno"
                    )
                    for p in menu.platos if str(p.tipo).lower() in ["postre", "3"] and getattr(p, "activo", True)
                ]
            else:
                self.has_menu_hoy = False
        self.is_loading = False

    def abrir_modal_pago(self):
        if not self.plato_1_sel or not self.plato_2_sel or not self.postre_sel:
            return rx.window_alert("Por favor, selecciona 1º Plato, 2º Plato y Postre.")
        self.show_modal_pago = True

    def cerrar_modal_pago(self):
        self.show_modal_pago = False

    def proceder_al_correo(self):
        self.show_modal_pago = False
        self.show_modal_correo = True

    @rx.event
    def validar_y_finalizar_reserva(self):
        correo = self.email_visitante.strip()
        if "@" not in correo or "." not in correo:
            self.error_correo = "Introduce un correo electrónico válido."
            return

        self.error_correo = ""

        with SessionLocal() as db:
            # Buscar los IDs de los 3 platos seleccionados a través de la BD
            from app.models import Plato
            nombres_elegidos = [self.plato_1_sel, self.plato_2_sel, self.postre_sel]
            platos_db = db.query(Plato).filter(Plato.nombre.in_(nombres_elegidos)).all()
            platos_ids = [p.id_plato for p in platos_db]

            self.reserva_exito_id = ReservaService.crear_reserva_visitante(
                db=db,
                id_menu=self.id_menu_hoy,
                platos_ids=platos_ids,
                email_visitante=correo
            )

        self.show_modal_correo = False
        
        # Limpiar selección
        self.plato_1_sel = ""
        self.plato_2_sel = ""
        self.postre_sel = ""
        self.email_visitante = ""

        return rx.window_alert(f"¡Reserva #{self.reserva_exito_id} confirmada! Se ha enviado el comprobante a {correo}.")