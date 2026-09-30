import re
import asyncio
import reflex as rx

from app.database import SessionLocal
from app.services.register_service import RegisterService


class RegisterState(rx.State):
    # Campos formulario
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    tipo: str = "estudiante"

    dni: str = ""
    telefono: str = ""

    # Campos visuales
    grado: str = ""
    especialidad: str = ""

    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""

    # Setters
    def set_nombre(self, value: str): self.nombre = value
    def set_apellido(self, value: str): self.apellido = value
    def set_email(self, value: str): self.email = value
    def set_password(self, value: str): self.password = value
    def set_confirm_password(self, value: str): self.confirm_password = value
    def set_tipo(self, value: str): self.tipo = value
    def set_dni(self, value: str): self.dni = value
    def set_telefono(self, value: str): self.telefono = value
    def set_grado(self, value: str): self.grado = value
    def set_especialidad(self, value: str): self.especialidad = value

    @rx.var
    def show_grado(self) -> bool:
        return self.tipo in ["estudiante", "profesor"]

    @rx.var
    def show_especialidad(self) -> bool:
        return self.tipo == "personal_comedor"

    def _validar_dni(self, dni: str) -> bool:
        dni = dni.strip().upper()
        if not re.fullmatch(r"\d{8}[A-Z]", dni):
            return False
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        numero = int(dni[:8])
        letra = dni[8]
        return letras[numero % 23] == letra

    def _validar_correo_por_rol(self, correo: str, rol: str) -> bool:
        c = correo.strip().lower()
        if rol == "estudiante":
            return c.endswith("@estudiantes.unileon.es") or c.endswith("@unileon.es")
        if rol == "profesor":
            return c.endswith("@unileon.es")
        if rol == "personal_comedor":
            return c.endswith("@comedor.unileon.es")
        return False

    @rx.event
    async def register(self):
        self.is_loading = True
        self.error_message = ""
        self.success_message = ""

        try:
            nombre = self.nombre.strip()
            apellido = self.apellido.strip()
            email = self.email.strip().lower()
            dni = self.dni.strip().upper()
            telefono = self.telefono.strip()

            if not nombre or not apellido or not email or not self.password or not dni or not telefono:
                self.error_message = "Completa todos los campos obligatorios."
                self.is_loading = False
                return

            if len(self.password) < 6:
                self.error_message = "La contraseña debe tener al menos 6 caracteres."
                self.is_loading = False
                return

            if self.password != self.confirm_password:
                self.error_message = "Las contraseñas no coinciden."
                self.is_loading = False
                return

            if self.tipo not in ["estudiante", "profesor", "personal_comedor"]:
                self.error_message = "Rol no válido para autorregistro."
                self.is_loading = False
                return

            if not self._validar_dni(dni):
                self.error_message = "DNI inválido. Debe tener 8 números y letra válida."
                self.is_loading = False
                return

            if not telefono.isdigit() or len(telefono) < 9:
                self.error_message = "Teléfono inválido. Debe tener al menos 9 dígitos."
                self.is_loading = False
                return

            if not self._validar_correo_por_rol(email, self.tipo):
                self.error_message = f"El correo no es válido para el rol {self.tipo}."
                self.is_loading = False
                return

            if self.tipo in ["estudiante", "profesor"] and not self.grado.strip():
                self.error_message = "El grado académico es obligatorio para este rol."
                self.is_loading = False
                return

            if self.tipo == "personal_comedor" and not self.especialidad.strip():
                self.error_message = "La especialidad es obligatoria para personal de comedor."
                self.is_loading = False
                return

            with SessionLocal() as db:
                if RegisterService.email_exists(db, email):
                    self.error_message = "Ya existe un usuario con ese correo."
                    self.is_loading = False
                    return

                if RegisterService.dni_exists(db, dni):
                    self.error_message = "Ya existe un usuario con ese DNI."
                    self.is_loading = False
                    return

                RegisterService.register_user(
                    db=db,
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    password=self.password,
                    dni=dni,
                    telefono=telefono,
                    tipo=self.tipo,
                )

            self.success_message = "Cuenta creada correctamente. Redirigiendo al login..."

            # Limpiar campos
            self.nombre = ""
            self.apellido = ""
            self.email = ""
            self.password = ""
            self.confirm_password = ""
            self.tipo = "estudiante"
            self.dni = ""
            self.telefono = ""
            self.grado = ""
            self.especialidad = ""

            self.is_loading = False
            
            await asyncio.sleep(2)
            return rx.redirect("/")

        except Exception as e:
            print("Error en registro:", e)
            self.error_message = "No se pudo crear la cuenta por un error interno."
            self.is_loading = False

    @rx.var
    def email_help_text(self) -> str:
        if self.tipo == "estudiante":
            return "Usar correo institucional: @estudiantes.unileon.es o @unileon.es"
        elif self.tipo == "profesor":
            return "Usar correo docente: @unileon.es"
        elif self.tipo == "personal_comedor":
            return "Usar correo del servicio: @comedor.unileon.es"
        return ""