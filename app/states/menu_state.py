import reflex as rx
from datetime import date, datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel

from app.database import SessionLocal
from app.services.menu_service import MenuService
from app.models import Plato, Reserva, Pago, Estudiante, Profesor
from app.states.auth_state import AppState


class MenuSchema(BaseModel):
    id_menu: int
    fecha: str
    tipo: str
    max_reservas: int
    disponible: bool
    num_platos: int = 0


class PlatoSimpleSchema(BaseModel):
    id_plato: int
    nombre: str
    tipo: str
    alergenos: str = "Ninguno"


class MenuState(rx.State):

    # ======================
    # DATOS Y GESTIÓN
    # ======================
    menus: list[MenuSchema] = []
    platos_disponibles: list[PlatoSimpleSchema] = []

    search_text: str = ""
    is_loading: bool = False
    total_reservas_hoy: int = 0

    # ======================
    # FORMULARIO / SELECCIÓN DE PLATOS (ADMIN Y COMEDOR)
    # ======================
    show_modal_nuevo_menu: bool = False
    show_modal_editar_menu: bool = False
    show_warning_desactivar: bool = False

    editing_id_menu: Optional[int] = None
    form_fecha: str = str(date.today())
    form_tipo: str = "almuerzo"
    form_max_reservas: int = 150
    form_disponible: bool = True

    id_primero_1: str = ""
    id_primero_2: str = ""
    id_primero_3: str = ""

    id_segundo_1: str = ""
    id_segundo_2: str = ""
    id_segundo_3: str = ""

    id_postre_1: str = ""
    id_postre_2: str = ""
    id_postre_3: str = ""

    # ======================
    # VISTA ESTUDIANTE / PROFESOR
    # ======================
    has_menu_hoy: bool = False
    id_menu_hoy: int = 0
    tipo_menu_hoy: str = ""
    fecha_menu_hoy: str = ""

    platos_primeros: list[PlatoSimpleSchema] = []
    platos_segundos: list[PlatoSimpleSchema] = []
    platos_postres: list[PlatoSimpleSchema] = []

    plato_1_sel: str = ""
    plato_2_sel: str = ""
    postre_sel: str = ""

    # ======================
    # SETTERS FORMULARIO
    # ======================
    def set_search_text(self, value: str): self.search_text = value
    def set_form_fecha(self, value: str): self.form_fecha = value
    def set_form_tipo(self, value: str): self.form_tipo = value
    def set_form_disponible(self, value: bool): self.form_disponible = value
    def set_show_modal_nuevo_menu(self, value: bool): self.show_modal_nuevo_menu = value
    def set_show_modal_editar_menu(self, value: bool): self.show_modal_editar_menu = value
    def set_show_warning_desactivar(self, value: bool): self.show_warning_desactivar = value

    def set_form_max_reservas(self, value: str):
        try:
            self.form_max_reservas = int(value)
        except Exception:
            self.form_max_reservas = 0

    def set_id_primero_1(self, v: str): self.id_primero_1 = v
    def set_id_primero_2(self, v: str): self.id_primero_2 = v
    def set_id_primero_3(self, v: str): self.id_primero_3 = v

    def set_id_segundo_1(self, v: str): self.id_segundo_1 = v
    def set_id_segundo_2(self, v: str): self.id_segundo_2 = v
    def set_id_segundo_3(self, v: str): self.id_segundo_3 = v

    def set_id_postre_1(self, v: str): self.id_postre_1 = v
    def set_id_postre_2(self, v: str): self.id_postre_2 = v
    def set_id_postre_3(self, v: str): self.id_postre_3 = v

    def set_plato_1_sel(self, value: str): self.plato_1_sel = value
    def set_plato_2_sel(self, value: str): self.plato_2_sel = value
    def set_postre_sel(self, value: str): self.postre_sel = value

    # ======================
    # CARGAR DATOS
    # ======================
    @rx.event
    def load_platos(self):
        """Carga el catálogo completo de platos con alérgenos."""
        with SessionLocal() as db:
            platos_db = db.query(Plato).all()
            self.platos_disponibles = [
                PlatoSimpleSchema(
                    id_plato=p.id_plato,
                    nombre=p.nombre,
                    tipo=getattr(p, "tipo", "primero"),
                    alergenos=getattr(p, "alergenos", "") or "Ninguno"
                )
                for p in platos_db
            ]

    @rx.event
    def load_menus(self):
        """Carga los menús para administración o personal de comedor."""
        self.is_loading = True
        with SessionLocal() as db:
            if self.search_text.strip():
                results = MenuService.search(db, self.search_text)
            else:
                results = MenuService.get_all(db)

        self.menus = [
            MenuSchema(
                id_menu=m.id_menu,
                fecha=str(m.fecha),
                tipo=m.tipo,
                max_reservas=m.max_reservas or 0,
                disponible=bool(m.disponible),
                num_platos=len(m.platos),
            )
            for m in results
        ]
        self.is_loading = False

    @rx.event
    def load_resumen_comedor(self):
        """Carga métricas específicas para el personal de comedor."""
        with SessionLocal() as db:
            self.total_reservas_hoy = MenuService.count_reservas_dia(db, date.today())

    @rx.event
    def load_menu_del_dia(self):
        """Carga el menú disponible de hoy."""
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

    # ======================
    # RESERVA DE MENÚ (CORREGIDO)
    # ======================
    @rx.event
    async def realizar_reserva(self):
        if not self.plato_1_sel or not self.plato_2_sel or not self.postre_sel:
            return rx.window_alert("Por favor, selecciona 1º Plato, 2º Plato y Postre.")

        app_state = await self.get_state(AppState)
        
        es_estudiante = app_state.is_estudiante
        es_profesor = app_state.is_profesor

        precio_menu = Decimal("5.50") if es_estudiante else Decimal("6.50")

        if Decimal(str(app_state.user_saldo)) < precio_menu:
            return rx.window_alert("Saldo TUI insuficiente. Por favor, recarga tu monedero.")

        with SessionLocal() as db:
            try:
                # 🛠️ Buscar los objetos Plato correspondientes a los 3 nombres seleccionados
                nombres_elegidos = [self.plato_1_sel, self.plato_2_sel, self.postre_sel]
                objetos_platos = db.query(Plato).filter(Plato.nombre.in_(nombres_elegidos)).all()

                nueva_reserva = Reserva(
                    id_usuario=app_state.user_id,
                    id_menu=self.id_menu_hoy,
                    fecha_reserva=datetime.now(),
                    estado="confirmada",
                    estado_bit=True,
                    platos=objetos_platos  # 👈 Guardamos los 3 platos elegidos en la tabla intermedia ReservaPlatos
                )
                db.add(nueva_reserva)
                db.flush()

                nuevo_pago = Pago(
                    id_usuario=app_state.user_id,
                    id_reserva=nueva_reserva.id_reserva,
                    monto=precio_menu,
                    metodo="tui",
                    fecha_pago=datetime.now(),
                    estado="completado"
                )
                db.add(nuevo_pago)

                nuevo_saldo_float = float(app_state.user_saldo) - float(precio_menu)
                
                if es_estudiante:
                    est_db = db.query(Estudiante).filter(Estudiante.id_usuario == app_state.user_id).first()
                    if est_db:
                        est_db.saldo = Decimal(str(nuevo_saldo_float))
                elif es_profesor:
                    prof_db = db.query(Profesor).filter(Profesor.id_usuario == app_state.user_id).first()
                    if prof_db:
                        prof_db.saldo = Decimal(str(nuevo_saldo_float))

                db.commit()

                app_state.user_saldo = nuevo_saldo_float

                msg_exito = f"🎉 ¡Reserva confirmada con éxito! Se han descontado {precio_menu:.2f}€ de tu TUI."
                self.plato_1_sel = ""
                self.plato_2_sel = ""
                self.postre_sel = ""

                return [
                    AppState.agregar_notificacion(msg_exito),
                    rx.window_alert(f"¡Reserva realizada con éxito! Nuevo saldo: {nuevo_saldo_float:.2f} €"),
                ]
            except Exception as e:
                db.rollback()
                print("Error al procesar reserva:", e)
                return rx.window_alert(f"Error al procesar la reserva: {str(e)}")

    # ======================
    # MODALES
    # ======================
    def _limpiar_formulario_admin(self):
        self.editing_id_menu = None
        self.form_fecha = str(date.today())
        self.form_tipo = "almuerzo"
        self.form_max_reservas = 150
        self.form_disponible = True

        self.id_primero_1 = ""
        self.id_primero_2 = ""
        self.id_primero_3 = ""

        self.id_segundo_1 = ""
        self.id_segundo_2 = ""
        self.id_segundo_3 = ""

        self.id_postre_1 = ""
        self.id_postre_2 = ""
        self.id_postre_3 = ""

    @rx.event
    def abrir_modal_nuevo_menu(self):
        self._limpiar_formulario_admin()
        self.show_modal_nuevo_menu = True
        return MenuState.load_platos

    @rx.event
    def abrir_modal_editar_menu(self, menu: MenuSchema):
        self._limpiar_formulario_admin()
        self.editing_id_menu = menu.id_menu
        self.form_fecha = menu.fecha
        self.form_tipo = menu.tipo
        self.form_max_reservas = menu.max_reservas
        self.form_disponible = menu.disponible

        self.load_platos()

        with SessionLocal() as db:
            m = MenuService.get_by_id(db, menu.id_menu)
            if m:
                p_list = [p for p in m.platos if str(p.tipo).lower() in ["primero", "1", "1º plato"]]
                s_list = [p for p in m.platos if str(p.tipo).lower() in ["segundo", "2", "2º plato"]]
                po_list = [p for p in m.platos if str(p.tipo).lower() in ["postre", "3"]]

                if len(p_list) > 0: self.id_primero_1 = str(p_list[0].id_plato)
                if len(p_list) > 1: self.id_primero_2 = str(p_list[1].id_plato)
                if len(p_list) > 2: self.id_primero_3 = str(p_list[2].id_plato)

                if len(s_list) > 0: self.id_segundo_1 = str(s_list[0].id_plato)
                if len(s_list) > 1: self.id_segundo_2 = str(s_list[1].id_plato)
                if len(s_list) > 2: self.id_segundo_3 = str(s_list[2].id_plato)

                if len(po_list) > 0: self.id_postre_1 = str(po_list[0].id_plato)
                if len(po_list) > 1: self.id_postre_2 = str(po_list[1].id_plato)
                if len(po_list) > 2: self.id_postre_3 = str(po_list[2].id_plato)

        self.show_modal_editar_menu = True

    def _obtener_ids_platos_seleccionados(self) -> list[int]:
        ids_raw = [
            self.id_primero_1, self.id_primero_2, self.id_primero_3,
            self.id_segundo_1, self.id_segundo_2, self.id_segundo_3,
            self.id_postre_1, self.id_postre_2, self.id_postre_3
        ]
        selected = set()
        for pid in ids_raw:
            if pid and pid.isdigit():
                selected.add(int(pid))
        return list(selected)

    @rx.event
    async def crear_menu(self):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not (app_state.is_admin or app_state.is_cocina):
            return rx.window_alert("No tienes permisos para realizar esta acción.")

        plato_ids = self._obtener_ids_platos_seleccionados()

        with SessionLocal() as db:
            nuevo_menu = MenuService.create(
                db=db,
                fecha=date.fromisoformat(self.form_fecha),
                tipo=self.form_tipo,
                max_reservas=self.form_max_reservas,
                disponible=self.form_disponible,
            )
            if plato_ids:
                platos = db.query(Plato).filter(Plato.id_plato.in_(plato_ids)).all()
                nuevo_menu.platos = platos
                db.commit()

        self.show_modal_nuevo_menu = False
        msg = f"ℹ️ Nuevo menú de {self.form_tipo.capitalize()} publicado para la fecha {self.form_fecha}."

        return [
            MenuState.load_menus,
            MenuState.load_resumen_comedor,
            AppState.agregar_notificacion(msg),
            rx.window_alert("Menú creado correctamente.")
        ]

    @rx.event
    def intentar_guardar_edicion(self):
        if self.editing_id_menu is None:
            return

        if not self.form_disponible:
            self.show_warning_desactivar = True
            return

        return self.ejecutar_guardado_edicion()

    @rx.event
    def confirmar_desactivacion_menu(self):
        self.show_warning_desactivar = False
        msg = f"⚠️ El menú ({self.form_tipo.capitalize()}) del {self.form_fecha} ha sido desactivado."

        return [
            MenuState.ejecutar_guardado_edicion,
            AppState.agregar_notificacion(msg)
        ]

    @rx.event
    async def ejecutar_guardado_edicion(self):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not (app_state.is_admin or app_state.is_cocina):
            return rx.window_alert("No tienes permisos para realizar esta acción.")

        plato_ids = self._obtener_ids_platos_seleccionados()

        with SessionLocal() as db:
            menu = MenuService.update(
                db=db,
                id_menu=self.editing_id_menu,
                fecha=date.fromisoformat(self.form_fecha),
                tipo=self.form_tipo,
                max_reservas=self.form_max_reservas,
                disponible=self.form_disponible,
            )
            if menu:
                platos = db.query(Plato).filter(Plato.id_plato.in_(plato_ids)).all()
                menu.platos = platos
                db.commit()

        self.show_modal_editar_menu = False
        return [
            MenuState.load_menus,
            rx.window_alert("Menú actualizado correctamente.")
        ]

    @rx.event
    async def eliminar_menu(self, id_menu: int):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not (app_state.is_admin or app_state.is_cocina):
            return rx.window_alert("No tienes permisos para realizar esta acción.")

        with SessionLocal() as db:
            MenuService.delete(db, id_menu)

        return [
            MenuState.load_menus,
            rx.window_alert("Menú eliminado.")
        ]