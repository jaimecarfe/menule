import reflex as rx
from pydantic import BaseModel

from app.database import SessionLocal
from app.services.plato_service import PlatoService
from app.states.auth_state import AppState

LISTA_ALERGENOS = [
    "Gluten", "Crustáceos", "Huevos", "Pescado", 
    "Cacahuetes", "Soja", "Lácteos", "Frutos de cáscara", 
    "Apio", "Mostaza", "Sésamo", "Sulfitos", 
    "Altramuces", "Moluscos"
]


class PlatoSchema(BaseModel):
    id_plato: int
    nombre: str
    tipo: str
    alergenos: str
    activo: bool
    num_menus: int = 0


class PlatoState(rx.State):

    # ====================================================
    # DATOS
    # ====================================================
    platos: list[PlatoSchema] = []
    search_text: str = ""
    is_loading: bool = False

    # Notificaciones globales del sistema para el layout
    notificaciones: list[str] = []

    # ====================================================
    # MODAL Y FORMULARIO
    # ====================================================
    show_modal: bool = False
    show_warning_modal: bool = False
    editando: int = 0

    form_nombre: str = ""
    form_tipo: str = "primero"
    form_activo: bool = True
    
    form_alergenos_selected: dict[str, bool] = {a: False for a in LISTA_ALERGENOS}
    form_otros_active: bool = False
    form_otros_texto: str = ""

    affected_menus_count: int = 0

    # ====================================================
    # SETTERS & ACCIONES NOTIFICACIONES
    # ====================================================
    def set_search_text(self, value: str):
        self.search_text = value

    def set_form_nombre(self, value: str):
        self.form_nombre = value

    def set_form_tipo(self, value: str):
        self.form_tipo = value

    def set_form_activo(self, value: bool):
        self.form_activo = value

    def set_show_modal(self, value: bool):
        self.show_modal = value

    def set_show_warning_modal(self, value: bool):
        self.show_warning_modal = value

    def set_form_otros_active(self, value: bool):
        self.form_otros_active = value

    def set_form_otros_texto(self, value: str):
        self.form_otros_texto = value

    @rx.event
    def toggle_alergeno(self, alergeno: str, checked: bool):
        self.form_alergenos_selected[alergeno] = checked

    # 👇 ESTE MÉTODO ES EL QUE PERMITE A OTROS ESTADOS (COMO MENU_STATE)
    # AÑADIR NOTIFICACIONES SIN QUE LANCE EL VARATTRIBUTERROR
    @rx.event
    def agregar_notificacion(self, mensaje: str):
        """Añade una notificación de forma segura para Reflex."""
        self.notificaciones.append(mensaje)

    @rx.event
    def limpiar_notificaciones(self):
        self.notificaciones = []

    # ====================================================
    # CARGAR DATOS
    # ====================================================
    @rx.event
    async def load_platos(self):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in:
            self.platos = []
            return rx.redirect("/")
        if not (app_state.is_admin or app_state.is_cocina):
            self.platos = []
            app_state.agregar_notificacion("Acceso denegado: Se requieren permisos de cocina o administrador.")
            return rx.redirect("/home")

        self.is_loading = True
        with SessionLocal() as db:
            if self.search_text.strip():
                resultados = PlatoService.search(db, self.search_text)
            else:
                resultados = PlatoService.get_all(db)

        self.platos = [
            PlatoSchema(
                id_plato=p.id_plato,
                nombre=p.nombre,
                tipo=p.tipo,
                alergenos=p.alergenos or "Ninguno",
                activo=bool(p.activo),
                num_menus=len(p.menus),
            )
            for p in resultados
        ]
        self.is_loading = False

    # ====================================================
    # ACCIONES MODAL
    # ====================================================
    @rx.event
    def nuevo_plato(self):
        self.editando = 0
        self.form_nombre = ""
        self.form_tipo = "primero"
        self.form_activo = True
        self.form_alergenos_selected = {a: False for a in LISTA_ALERGENOS}
        self.form_otros_active = False
        self.form_otros_texto = ""
        self.show_modal = True

    @rx.event
    def editar_plato(self, id_plato: int):
        with SessionLocal() as db:
            plato = PlatoService.get_by_id(db, id_plato)

        if plato is None:
            return rx.window_alert("No existe ese plato.")

        self.editando = plato.id_plato
        self.form_nombre = plato.nombre
        self.form_tipo = plato.tipo
        self.form_activo = bool(plato.activo)

        actuales = [a.strip() for a in (plato.alergenos or "").split(",") if a.strip()]
        self.form_alergenos_selected = {
            a: (a in actuales) for a in LISTA_ALERGENOS
        }

        otros_lista = [a for a in actuales if a not in LISTA_ALERGENOS and a != "Ninguno"]
        if otros_lista:
            self.form_otros_active = True
            self.form_otros_texto = ", ".join(otros_lista)
        else:
            self.form_otros_active = False
            self.form_otros_texto = ""

        self.show_modal = True

    # ====================================================
    # COMPROBACIÓN Y GUARDADO DE ESTADO
    # ====================================================
    @rx.event
    def intentar_guardar(self):
        if not self.form_nombre.strip():
            return rx.window_alert("El nombre del plato es obligatorio.")

        # Si estamos editando y cambiando el plato a INACTIVO
        if self.editando > 0 and not self.form_activo:
            with SessionLocal() as db:
                plato = PlatoService.get_by_id(db, self.editando)
                if plato and len(plato.menus) > 0:
                    self.affected_menus_count = len(plato.menus)
                    self.show_warning_modal = True
                    return

        return self.ejecutar_guardado()

    @rx.event
    def confirmar_desactivacion(self):
        self.show_warning_modal = False
        alerta = f"El plato '{self.form_nombre}' ha sido desactivado pero se utiliza en {self.affected_menus_count} menú(s). Requiere sustitución."
        self.notificaciones.append(alerta)
        return self.ejecutar_guardado()

    @rx.event
    async def ejecutar_guardado(self):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not (app_state.is_admin or app_state.is_cocina):
            return rx.window_alert("No tienes permisos para realizar esta acción.")

        seleccionados = [a for a, act in self.form_alergenos_selected.items() if act]
        if self.form_otros_active and self.form_otros_texto.strip():
            seleccionados.append(self.form_otros_texto.strip())

        alergenos_str = ", ".join(seleccionados) if seleccionados else "Ninguno"

        with SessionLocal() as db:
            if self.editando == 0:
                PlatoService.create(
                    db=db,
                    nombre=self.form_nombre,
                    tipo=self.form_tipo,
                    alergenos=alergenos_str,
                    activo=self.form_activo,
                )
                mensaje = "Plato creado correctamente."
            else:
                PlatoService.update(
                    db=db,
                    id_plato=self.editando,
                    nombre=self.form_nombre,
                    tipo=self.form_tipo,
                    alergenos=alergenos_str,
                    activo=self.form_activo,
                )
                mensaje = "Plato actualizado correctamente."

        self.show_modal = False
        return [
            PlatoState.load_platos,
            rx.window_alert(mensaje)
        ]

    @rx.event
    async def eliminar(self, id_plato: int):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not (app_state.is_admin or app_state.is_cocina):
            return rx.window_alert("No tienes permisos para realizar esta acción.")

        with SessionLocal() as db:
            PlatoService.delete(db, id_plato)

        return [
            PlatoState.load_platos,
            rx.window_alert("Plato eliminado correctamente.")
        ]