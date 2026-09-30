import reflex as rx
from typing import List, Dict, Any, Union
from app.database import SessionLocal
from app.services.estadistica_service import EstadisticaService
from app.states.auth_state import AppState


class EstadisticaState(rx.State):
    tipo_vista: str = "Pagos"  # 'Pagos' o 'Incidencias'
    
    # Datos estructurados para Recharts y Tablas
    datos_pagos_rol: List[Dict[str, Any]] = []
    datos_incidencias_rol: List[Dict[str, Any]] = []
    datos_diarios: List[Dict[str, Any]] = []

    # Métricas Globales rápidas
    total_recaudado_rol: float = 0.0
    total_incidencias_rol: int = 0

    # ==================== SETTERS ====================
    def set_tipo_vista(self, value: Union[str, List[str]]):
        if isinstance(value, list):
            self.tipo_vista = value[0] if value else "Pagos"
        else:
            self.tipo_vista = value

    # ==================== CARGA DE DATOS ====================
    @rx.event
    async def load_estadisticas(self):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in:
            self.datos_pagos_rol = []
            self.datos_incidencias_rol = []
            self.datos_diarios = []
            return rx.redirect("/")
        if not app_state.is_admin:
            self.datos_pagos_rol = []
            self.datos_incidencias_rol = []
            self.datos_diarios = []
            app_state.agregar_notificacion("Acceso denegado: Se requieren permisos de administrador.")
            return rx.redirect("/home")

        with SessionLocal() as db:
            # 1. Carga por rol
            self.datos_pagos_rol = EstadisticaService.obtener_pagos_por_rol(db)
            self.datos_incidencias_rol = EstadisticaService.obtener_incidencias_por_rol(db)
            
            # 2. Carga diaria de la Vista SQL
            self.datos_diarios = EstadisticaService.obtener_estadisticas_diarias(db)

            # 3. Totales calculados
            self.total_recaudado_rol = sum(d["total_pagado"] for d in self.datos_pagos_rol)
            self.total_incidencias_rol = sum(d["cantidad_incidencias"] for d in self.datos_incidencias_rol)