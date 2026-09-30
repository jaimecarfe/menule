import reflex as rx
from app.database import SessionLocal
from app.services.perfil_service import PerfilService
from app.states.auth_state import AppState


class PerfilState(rx.State):
    modal_contrasena_abierto: bool = False
    pass_actual: str = ""
    pass_nueva: str = ""
    pass_repetir: str = ""
    error_msg: str = ""
    success_msg: str = ""

    def abrir_modal_contrasena(self):
        self.pass_actual = ""
        self.pass_nueva = ""
        self.pass_repetir = ""
        self.error_msg = ""
        self.success_msg = ""
        self.modal_contrasena_abierto = True

    def cerrar_modal_contrasena(self):
        self.modal_contrasena_abierto = False
        self.error_msg = ""
        self.success_msg = ""

    def set_pass_actual(self, value: str):
        self.pass_actual = value

    def set_pass_nueva(self, value: str):
        self.pass_nueva = value

    def set_pass_repetir(self, value: str):
        self.pass_repetir = value

    @rx.event
    async def cambiar_contrasena(self):
        self.error_msg = ""
        self.success_msg = ""

        if not self.pass_actual or not self.pass_nueva or not self.pass_repetir:
            self.error_msg = "Por favor, completa todos los campos."
            return

        if self.pass_nueva != self.pass_repetir:
            self.error_msg = "Las nuevas contraseñas no coinciden."
            return

        if len(self.pass_nueva) < 4:
            self.error_msg = "La nueva contraseña debe tener al menos 4 caracteres."
            return

        app = await self.get_state(AppState)
        user_id = app.user_id

        with SessionLocal() as db:
            ok, msg = PerfilService.cambiar_contrasena(
                db, user_id, self.pass_actual, self.pass_nueva
            )

        if ok:
            self.success_msg = msg
            self.pass_actual = ""
            self.pass_nueva = ""
            self.pass_repetir = ""
            app.agregar_notificacion("Contraseña actualizada con éxito.")
        else:
            self.error_msg = msg