import reflex as rx
from pydantic import BaseModel
from typing import Optional
from app.models import Usuario as UsuarioORM
from app.database import SessionLocal
from app.services.register_service import RegisterService
from app.services.user_service import UserService
from app.states.auth_state import AppState


class UsuarioSchema(BaseModel):
    id_usuario: int
    dni: Optional[str] = ""
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = ""
    tipo: str


class UserState(rx.State):
    users: list[UsuarioSchema] = []
    search_text: str = ""

    # Control de Modales
    show_modal_nuevo: bool = False
    show_modal_editar: bool = False

    # Campos de Formulario (Crear / Editar)
    current_id: int = 0
    form_dni: str = ""
    form_nombre: str = ""
    form_apellido: str = ""
    form_email: str = ""
    form_telefono: str = ""
    form_tipo: str = "estudiante"
    form_password: str = ""

    # --- SETTERS ---
    def set_search_text(self, val: str):
        self.search_text = val
        self.search_users()

    def set_show_modal_nuevo(self, val: bool):
        self.show_modal_nuevo = val

    def set_show_modal_editar(self, val: bool):
        self.show_modal_editar = val

    def set_form_dni(self, val: str):
        self.form_dni = val

    def set_form_nombre(self, val: str):
        self.form_nombre = val

    def set_form_apellido(self, val: str):
        self.form_apellido = val

    def set_form_email(self, val: str):
        self.form_email = val

    def set_form_telefono(self, val: str):
        self.form_telefono = val

    def set_form_tipo(self, val: str):
        self.form_tipo = val

    def set_form_password(self, val: str):
        self.form_password = val

    # --- CONTROL DE ACCESO ADMIN ---
    @rx.event
    async def check_admin_access(self):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in:
            return rx.redirect("/")
        if not app_state.is_admin:
            app_state.agregar_notificacion("Acceso denegado: Se requieren permisos de administrador.")
            return rx.redirect("/home")

    # --- LECTURA ---
    @rx.event
    async def load_users(self):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in:
            self.users = []
            return rx.redirect("/")
        if not app_state.is_admin:
            self.users = []
            app_state.agregar_notificacion("Acceso denegado: Se requieren permisos de administrador.")
            return rx.redirect("/home")

        db = SessionLocal()
        try:
            query_results = UserService.get_all_users(db)
            self.users = [
                UsuarioSchema(
                    id_usuario=u.id_usuario,
                    dni=u.dni or "",
                    nombre=u.nombre,
                    apellido=u.apellido,
                    email=u.email,
                    telefono=u.telefono or "",
                    tipo=u.tipo,
                )
                for u in query_results
            ]
        finally:
            db.close()

    @rx.event
    async def search_users(self):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not app_state.is_admin:
            self.users = []
            return

        db = SessionLocal()
        try:
            results = UserService.search_users(db, self.search_text.strip()) if self.search_text.strip() else UserService.get_all_users(db)
            self.users = [
                UsuarioSchema(
                    id_usuario=u.id_usuario,
                    dni=u.dni or "",
                    nombre=u.nombre,
                    apellido=u.apellido,
                    email=u.email,
                    telefono=u.telefono or "",
                    tipo=u.tipo,
                )
                for u in results
            ]
        finally:
            db.close()

    # --- CREAR USUARIO EN MYSQL (DESDE PANEL ADMIN) ---
    def abrir_modal_nuevo(self):
        self.form_dni = ""
        self.form_nombre = ""
        self.form_apellido = ""
        self.form_email = ""
        self.form_telefono = ""
        self.form_tipo = "estudiante"
        self.form_password = ""
        self.show_modal_nuevo = True

    @rx.event
    async def crear_usuario(self):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not app_state.is_admin:
            return rx.window_alert("No tienes permisos para realizar esta acción.")

        if not self.form_nombre or not self.form_email or not self.form_password:
            return rx.window_alert("Nombre, Email y Contraseña son obligatorios.")

        db = SessionLocal()
        try:
            pwd_hashed = RegisterService.hash_password(self.form_password)

            nuevo = UsuarioORM(
                dni=self.form_dni or None,
                nombre=self.form_nombre,
                apellido=self.form_apellido,
                email=self.form_email,
                contrasena_hash=pwd_hashed,
                telefono=self.form_telefono or None,
                tipo=self.form_tipo,
                credencial_activa=True,
            )
            db.add(nuevo)
            db.commit()
            self.show_modal_nuevo = False
            return [
                UserState.load_users,
                rx.window_alert("Usuario creado exitosamente.")
            ]
        except Exception as e:
            db.rollback()
            return rx.window_alert(f"Error al crear usuario: {str(e)}")
        finally:
            db.close()

    # --- EDITAR USUARIO EN MYSQL ---
    def abrir_modal_editar(self, u: UsuarioSchema):
        self.current_id = u.id_usuario
        self.form_dni = u.dni or ""
        self.form_nombre = u.nombre
        self.form_apellido = u.apellido
        self.form_email = u.email
        self.form_telefono = u.telefono or ""
        self.form_tipo = u.tipo
        self.form_password = ""
        self.show_modal_editar = True

    @rx.event
    async def guardar_edicion_usuario(self):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not app_state.is_admin:
            return rx.window_alert("No tienes permisos para realizar esta acción.")

        db = SessionLocal()
        try:
            u = (
                db.query(UsuarioORM)
                .filter(UsuarioORM.id_usuario == self.current_id)
                .first()
            )
            if u:
                u.dni = self.form_dni
                u.nombre = self.form_nombre
                u.apellido = self.form_apellido
                u.email = self.form_email
                u.telefono = self.form_telefono
                u.tipo = self.form_tipo
                
                if self.form_password.strip():
                    u.contrasena_hash = RegisterService.hash_password(self.form_password)

                db.commit()
                self.show_modal_editar = False
                return [
                    UserState.load_users,
                    rx.window_alert("Usuario actualizado correctamente.")
                ]
        except Exception as e:
            db.rollback()
            return rx.window_alert(f"Error al actualizar: {str(e)}")
        finally:
            db.close()

    # --- ELIMINAR USUARIO EN MYSQL ---
    @rx.event
    async def eliminar_usuario(self, id_usuario: int):
        app_state = await self.get_state(AppState)
        if not app_state.is_logged_in or not app_state.is_admin:
            return rx.window_alert("No tienes permisos para realizar esta acción.")

        db = SessionLocal()
        try:
            u = db.query(UsuarioORM).filter(UsuarioORM.id_usuario == id_usuario).first()
            if u:
                db.delete(u)
                db.commit()
                return [
                    UserState.load_users,
                    rx.window_alert(f"Usuario #{id_usuario} eliminado con éxito.")
                ]
        except Exception as e:
            db.rollback()
            return rx.window_alert(f"No se pudo eliminar el usuario: {str(e)}")
        finally:
            db.close()