import reflex as rx
from typing import List

from app.config.navigation import NAV_ITEMS, NavigationItem
from app.database import SessionLocal
from app.services.auth_service import AuthService
from app.services.user_service import UserService


class AppState(rx.State):
    # =====================================
    # LOGIN
    # =====================================
    email: str = ""
    password: str = ""

    is_logged_in: bool = False
    is_loading: bool = False
    error_message: str = ""

    # =====================================
    # USUARIO ACTUAL Y MONEDERO
    # =====================================
    user_id: int = 0
    user_name: str = ""
    user_email: str = ""
    user_role: str = ""
    user_dni: str = ""
    user_saldo: float = 0.00
    user_tui_num: str = ""
    notificaciones: List[str] = []

    users: list = []

    # =====================================
    # VARS COMPUTADOS PARA LA UI
    # =====================================
    @rx.var
    def user_saldo_str(self) -> str:
        return f"{self.user_saldo:.2f} €"

    # =====================================
    # LOGIN EVENT
    # =====================================
    @rx.event
    def login(self):
        self.is_loading = True
        self.error_message = ""

        try:
            with SessionLocal() as db:
                user = AuthService.login(
                    db,
                    self.email,
                    self.password,
                )

                if user is None:
                    self.error_message = "Correo o contraseña incorrectos."
                    self.is_loading = False
                    return

                self.is_logged_in = True
                self.user_id = user.id_usuario
                self.user_name = f"{user.nombre} {user.apellido}"
                self.user_email = user.email
                self.user_role = str(user.tipo).lower() if user.tipo else ""
                self.user_dni = user.dni or f"ID-{user.id_usuario}"

                # Obtención blindada de datos (soporta objeto único o lista)
                est_info = getattr(user, "estudiante_info", None)
                prof_info = getattr(user, "profesor_info", None)

                if isinstance(est_info, list) and len(est_info) > 0:
                    est_info = est_info[0]
                if isinstance(prof_info, list) and len(prof_info) > 0:
                    prof_info = prof_info[0]

                if self.is_estudiante and est_info:
                    self.user_saldo = float(getattr(est_info, "saldo", 0.0) or 0.0)
                    self.user_tui_num = getattr(est_info, "tui_numero", "") or "Sin TUI"
                elif self.is_profesor and prof_info:
                    self.user_saldo = float(getattr(prof_info, "saldo", 0.0) or 0.0)
                    self.user_tui_num = getattr(prof_info, "tui_numero", "") or "Sin TUI"
                else:
                    self.user_saldo = 0.0
                    self.user_tui_num = self.user_dni

            self.is_loading = False
            return rx.redirect("/home")

        except Exception as e:
            print("Error en login:", e)
            self.error_message = "Ha ocurrido un error al iniciar sesión."
            self.is_loading = False

    # =====================================
    # LOGIN VISITANTE
    # =====================================
    @rx.event
    def login_visitante(self):
        self.email = ""
        self.password = ""
        self.error_message = ""
        self.is_loading = False

        self.is_logged_in = True
        self.user_id = 0
        self.user_name = "Visitante"
        self.user_email = ""
        self.user_role = "visitante"
        self.user_dni = ""
        self.user_saldo = 0.0
        self.user_tui_num = ""

        return rx.redirect("/home")

    # =====================================
    # LOGOUT
    # =====================================
    @rx.event
    def logout(self):
        self.email = ""
        self.password = ""

        self.is_logged_in = False
        self.is_loading = False
        self.error_message = ""

        self.user_id = 0
        self.user_name = ""
        self.user_email = ""
        self.user_role = ""
        self.user_dni = ""
        self.user_saldo = 0.0
        self.user_tui_num = ""

        self.notificaciones = []

        return rx.redirect("/")

    # =====================================
    # SETTERS
    # =====================================
    def set_email(self, value: str):
        self.email = value

    def set_password(self, value: str):
        self.password = value

    # =====================================
    # ROLES
    # =====================================
    @rx.var
    def is_admin(self) -> bool:
        return self.user_role == "administrador"

    @rx.var
    def is_estudiante(self) -> bool:
        return self.user_role == "estudiante"

    @rx.var
    def is_profesor(self) -> bool:
        return self.user_role == "profesor"

    @rx.var
    def is_cocina(self) -> bool:
        return self.user_role == "personal_comedor"

    @rx.var
    def is_visitante(self) -> bool:
        return self.user_role == "visitante"

    # =====================================
    # NAVEGACIÓN DINÁMICA
    # =====================================
    @rx.var
    def navigation_items(self) -> List[NavigationItem]:
        return NAV_ITEMS.get(self.user_role, [])

    # =====================================
    # CARGAR USUARIOS
    # =====================================
    @rx.event
    def load_users(self):
        with SessionLocal() as db:
            self.users = UserService.get_all_users(db)

    # =====================================
    # INICIALES Y NOMBRE COMPLETO DINÁMICOS
    # =====================================
    @rx.var
    def user_full_name(self) -> str:
        if not self.user_name:
            return "Usuario MenULE"
        return self.user_name

    @rx.var
    def user_initials(self) -> str:
        name = self.user_name.strip() if self.user_name else ""
        if not name:
            return "U"

        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        return parts[0][0].upper()

    # =====================================
    # NOTIFICACIONES
    # =====================================
    def agregar_notificacion(self, mensaje: str):
        self.notificaciones.append(mensaje)

    def limpiar_notificaciones(self):
        self.notificaciones = []

    # =====================================
    # DESCONTAR SALDO PERSISTENTE EN BD
    # =====================================
    @rx.event
    def descontar_saldo_menu(self) -> bool:
        """Descuenta el precio exacto según rol (5.50€ Estudiante / 6.50€ Profesor) y guarda en BD."""
        if not self.is_logged_in or self.user_id == 0:
            return False

        # Tarifa exacta por rol
        precio = 5.50 if self.is_estudiante else (6.50 if self.is_profesor else 7.50)

        if self.user_saldo < precio:
            return False

        try:
            with SessionLocal() as db:
                if self.is_estudiante:
                    from app.models import Estudiante
                    est = db.query(Estudiante).filter(Estudiante.id_usuario == self.user_id).first()
                    if est:
                        nuevo_saldo = float(est.saldo or 0.0) - precio
                        est.saldo = nuevo_saldo
                        db.commit()
                        db.refresh(est)
                        self.user_saldo = float(est.saldo)
                elif self.is_profesor:
                    from app.models import Profesor
                    prof = db.query(Profesor).filter(Profesor.id_usuario == self.user_id).first()
                    if prof:
                        nuevo_saldo = float(prof.saldo or 0.0) - precio
                        prof.saldo = nuevo_saldo
                        db.commit()
                        db.refresh(prof)
                        self.user_saldo = float(prof.saldo)

            return True
        except Exception as e:
            print("Error al descontar saldo de la BD:", e)
            return False