import reflex as rx
from pydantic import BaseModel
from typing import List, Optional, Dict, Union
from app.database import SessionLocal
from app.services.incidencia_service import IncidenciaService
from app.states.auth_state import AppState


class IncidenciaSchema(BaseModel):
    id_incidencia: int
    titulo: str
    descripcion: str
    numero_seguimiento: str
    fecha_reporte: str
    estado: str
    prioridad: str
    correo_usuario: str
    solucion: Optional[str] = ""
    respuesta: Optional[str] = ""


class IncidenciaState(rx.State):
    incidencias: List[IncidenciaSchema] = []
    search_text: str = ""
    filtro_estado: str = "todos"
    is_loading: bool = False

    # KPIs
    kpi_total: int = 0
    kpi_abiertas: int = 0
    kpi_en_proceso: int = 0
    kpi_resueltas: int = 0
    kpi_por_rol: Dict[str, int] = {}

    # Modal "Responder Incidencia" (Admin)
    modal_abierto: bool = False
    incidencia_seleccionada: Optional[IncidenciaSchema] = None
    texto_respuesta: str = ""

    # Modal "Reportar Nueva Incidencia" (Estudiante/Profesor)
    modal_crear_abierto: bool = False
    nuevo_titulo: str = ""
    nueva_descripcion: str = ""
    nuevo_destino: str = "administracion"  # <--- 'administracion' por defecto o 'cocina'

    # ==================== SETTERS ====================
    def set_search_text(self, value: str):
        self.search_text = value

    def set_filtro_estado(self, value: Union[str, List[str]]):
        if isinstance(value, list):
            self.filtro_estado = value[0] if value else "todos"
        else:
            self.filtro_estado = value

    def set_texto_respuesta(self, value: str):
        self.texto_respuesta = value

    def set_nuevo_titulo(self, value: str):
        self.nuevo_titulo = value

    def set_nueva_descripcion(self, value: str):
        self.nueva_descripcion = value

    def set_nuevo_destino(self, value: str):
        self.nuevo_destino = value

    # ==================== MODALES ====================
    def abrir_modal_respuesta(self, inc: IncidenciaSchema):
        self.incidencia_seleccionada = inc
        self.texto_respuesta = inc.solucion or ""
        self.modal_abierto = True

    def cerrar_modal(self):
        self.modal_abierto = False
        self.incidencia_seleccionada = None
        self.texto_respuesta = ""

    def abrir_modal_crear(self):
        self.nuevo_titulo = ""
        self.nueva_descripcion = ""
        self.nuevo_destino = "administracion"
        self.modal_crear_abierto = True

    def cerrar_modal_crear(self):
        self.modal_crear_abierto = False
        self.nuevo_titulo = ""
        self.nueva_descripcion = ""
        self.nuevo_destino = "administracion"

    # ==================== CARGA DE DATOS ====================
    @rx.event
    async def load_incidencias(self):
        self.is_loading = True
        app = await self.get_state(AppState)

        rol_usuario = app.user_role or "estudiante"
        user_id = app.user_id

        with SessionLocal() as db:
            resultados = IncidenciaService.get_all(
                db, 
                search_text=self.search_text, 
                estado_filtro=self.filtro_estado,
                user_role=rol_usuario,
                user_id=user_id
            )
            
            self.incidencias = [
                IncidenciaSchema(
                    id_incidencia=i.id_incidencia,
                    titulo=i.titulo,
                    descripcion=i.descripcion,
                    numero_seguimiento=i.numero_seguimiento or "S/N",
                    fecha_reporte=i.fecha_reporte.strftime("%Y-%m-%d %H:%M") if hasattr(i.fecha_reporte, "strftime") else str(i.fecha_reporte),
                    estado=i.estado or "abierta",
                    prioridad=i.prioridad or "media",
                    correo_usuario=i.usuario.email if i.usuario else "Desconocido",
                    solucion=i.solucion or "",
                    respuesta=i.solucion or ""
                )
                for i in resultados
            ]

            kpis = IncidenciaService.get_kpis(db, user_role=rol_usuario, user_id=user_id)
            self.kpi_total = kpis["total"]
            self.kpi_abiertas = kpis["abiertas"]
            self.kpi_en_proceso = kpis["en_proceso"]
            self.kpi_resueltas = kpis["resueltas"]

        self.is_loading = False

    # ==================== ACCIONES ====================
    @rx.event
    async def crear_incidencia(self):
        if not self.nuevo_titulo.strip() or not self.nueva_descripcion.strip():
            return

        app_state = await self.get_state(AppState)
        user_id = app_state.user_id

        if not user_id:
            return

        with SessionLocal() as db:
            IncidenciaService.crear(
                db,
                id_usuario=user_id,
                titulo=self.nuevo_titulo.strip(),
                descripcion=self.nueva_descripcion.strip(),
                destino=self.nuevo_destino
            )

        app_state.agregar_notificacion("Incidencia enviada correctamente.")
        self.cerrar_modal_crear()
        return IncidenciaState.load_incidencias

    @rx.event
    async def enviar_respuesta(self):
        if not self.incidencia_seleccionada or not self.texto_respuesta.strip():
            return

        app_state = await self.get_state(AppState)
        admin_id = app_state.user_id

        with SessionLocal() as db:
            IncidenciaService.responder(
                db,
                self.incidencia_seleccionada.id_incidencia,
                self.texto_respuesta.strip(),
                admin_id
            )

        app_state.agregar_notificacion(
            f"Incidencia #{self.incidencia_seleccionada.id_incidencia} respondida y resuelta."
        )

        self.cerrar_modal()
        return IncidenciaState.load_incidencias

    @rx.event
    async def cambiar_estado_rapido(self, id_incidencia: int, nuevo_estado: str):
        with SessionLocal() as db:
            IncidenciaService.cambiar_estado(db, id_incidencia, nuevo_estado)

        app_state = await self.get_state(AppState)
        app_state.agregar_notificacion(
            f"Incidencia #{id_incidencia} cambió a {nuevo_estado.upper()}."
        )

        return IncidenciaState.load_incidencias