import reflex as rx
from pydantic import BaseModel
from typing import List, Optional, Union

from app.database import SessionLocal
from app.services.pago_service import PagoService
from app.states.auth_state import AppState
from app.models import Estudiante, Profesor


class PagoSchema(BaseModel):
    id_pago: int
    id_usuario: int
    id_reserva: Optional[int] = None
    monto: float
    metodo: str
    fecha_pago: str
    estado: str
    correo: str


class PagoState(rx.State):

    # ====================================================
    # ESTADO GENERAL Y ADMIN
    # ====================================================
    pagos: List[PagoSchema] = []
    search_text: str = ""
    filtro_metodo: str = "todos"
    is_loading: bool = False

    # Métricas agregadas Admin (KPIs)
    kpi_ingresos: float = 0.0
    kpi_operaciones: int = 0
    kpi_tui_bono: int = 0
    kpi_visitantes: int = 0

    # ====================================================
    # ESTADO MONEDERO USUARIOS (ESTUDIANTE / PROFESOR)
    # ====================================================
    saldo_actual: float = 0.00
    numero_tui: str = "TUI-UNILEON"
    monto_recarga: str = "10"
    metodo_recarga: str = "tarjeta"

    # ====================================================
    # SETTERS
    # ====================================================
    def set_search_text(self, value: str):
        self.search_text = value

    def set_monto_recarga(self, value: str):
        self.monto_recarga = value

    def set_metodo_recarga(self, value: str):
        self.metodo_recarga = value

    def set_filtro_metodo(self, value: Union[str, list[str]]):
        if isinstance(value, list):
            self.filtro_metodo = value[0] if value else "todos"
        else:
            self.filtro_metodo = value

    # ====================================================
    # CARGA DE DATOS (CON SINCRONIZACIÓN DE SIDEBAR)
    # ====================================================
    @rx.event
    async def load_pagos(self):
        self.is_loading = True
        app_state = await self.get_state(AppState)
        
        with SessionLocal() as db:
            # 1. Cargar saldo y TUI del usuario
            if app_state.user_id:
                est = db.query(Estudiante).filter(Estudiante.id_usuario == app_state.user_id).first()
                if est:
                    self.saldo_actual = float(est.saldo or 0.0)
                    self.numero_tui = getattr(est, "tui_numero", None) or f"TUI-{app_state.user_id:06d}"
                else:
                    prof = db.query(Profesor).filter(Profesor.id_usuario == app_state.user_id).first()
                    if prof:
                        self.saldo_actual = float(prof.saldo or 0.0)
                        self.numero_tui = getattr(prof, "tui_numero", None) or f"TUI-{app_state.user_id:06d}"

                # 🎯 Actualizamos el saldo del Sidebar
                app_state.user_saldo = self.saldo_actual

            # 2. Cargar historial de pagos
            resultados = PagoService.get_all(db, self.search_text, self.filtro_metodo)
            
            # Si no es admin, filtra solo las propias del usuario
            if not app_state.is_admin and app_state.user_id:
                resultados = [p for p in resultados if p.id_usuario == app_state.user_id]

            self.pagos = [
                PagoSchema(
                    id_pago=p.id_pago,
                    id_usuario=p.id_usuario or 0,
                    id_reserva=p.id_reserva,
                    monto=float(p.monto or 0.0),
                    metodo=(p.metodo or "tarjeta").lower(),
                    fecha_pago=p.fecha_pago.strftime("%Y-%m-%d %H:%M") if hasattr(p.fecha_pago, "strftime") else str(p.fecha_pago),
                    estado=(p.estado or "completado").lower(),
                    correo=p.usuario.email if (p.usuario and p.id_usuario != 0) else (p.correo or "Visitante"),
                )
                for p in resultados
            ]

            # KPIs
            kpis = PagoService.get_kpis(db)
            self.kpi_ingresos = kpis["total_ingresos"]
            self.kpi_operaciones = kpis["total_operaciones"]
            self.kpi_tui_bono = kpis["tui_bonos"]
            self.kpi_visitantes = kpis["visitantes"]

        self.is_loading = False

    # ====================================================
    # ACCIONES
    # ====================================================
    @rx.event
    async def realizar_recarga(self):
        try:
            monto_val = float(self.monto_recarga)
            if monto_val <= 0:
                return rx.window_alert("Por favor, introduce un importe válido mayor que 0.")

            app_state = await self.get_state(AppState)
            if not app_state.user_id:
                return rx.window_alert("Sesión no válida.")

            with SessionLocal() as db:
                exito = PagoService.recargar_saldo_usuario(
                    db, app_state.user_id, monto_val, self.metodo_recarga
                )

                if exito:
                    # 🛠️ Obtener saldo exacto tras commit
                    nuevo_saldo = 0.0
                    est = db.query(Estudiante).filter(Estudiante.id_usuario == app_state.user_id).first()
                    if est:
                        nuevo_saldo = float(est.saldo or 0.0)
                    else:
                        prof = db.query(Profesor).filter(Profesor.id_usuario == app_state.user_id).first()
                        if prof:
                            nuevo_saldo = float(prof.saldo or 0.0)

                    # 🛠️ Sincronizar Sidebar y Vista Monedero
                    app_state.user_saldo = nuevo_saldo
                    self.saldo_actual = nuevo_saldo

            if exito:
                msg = f"🎉 ¡Recarga de {monto_val:.2f} € realizada con éxito!"
                app_state.agregar_notificacion(msg)

                self.monto_recarga = "10"

                return [
                    PagoState.load_pagos,
                    rx.window_alert(f"¡Recarga completada! Tu nuevo saldo es: {app_state.user_saldo:.2f} €")
                ]

        except ValueError:
            return rx.window_alert("El importe introducido no es un número válido.")

    @rx.event
    async def cambiar_estado_pago(self, id_pago: int, nuevo_estado: str):
        with SessionLocal() as db:
            PagoService.cambiar_estado(db, id_pago, nuevo_estado)

        app_state = await self.get_state(AppState)
        app_state.agregar_notificacion(
            f"El pago #{id_pago} ha cambiado a estado {nuevo_estado.upper()}."
        )

        return PagoState.load_pagos