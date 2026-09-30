import reflex as rx
from app.states.register_state import RegisterState


def form_field(
    label: str,
    placeholder: str,
    value: rx.Var[str],
    on_change,
    type_: str = "text",
    icon: str = "",
) -> rx.Component:
    return rx.vstack(
        rx.text(label, weight="medium", size="2", color="#374151"),
        rx.input(
            rx.input.slot(rx.icon(icon, size=16, color="#9CA3AF")) if icon else None,
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            type=type_,
            width="100%",
            size="3",
            radius="large",
        ),
        spacing="1",
        width="100%",
        align="start",
    )


def registro_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.image(
                        src="/logo_menule.png",
                        height="40px",
                        width="auto",
                        alt="Logo MenULE",
                    ),
                    rx.vstack(
                        rx.heading("Crear una cuenta", size="6", weight="bold", color="#111827"),
                        rx.text("Únete a la plataforma de comedor MenULE", color="gray", size="2"),
                        spacing="0",
                        align="start",
                    ),
                    align="center",
                    spacing="3",
                    width="100%",
                    margin_bottom="0.5em",
                ),
                rx.divider(),

                rx.grid(
                    rx.vstack(
                        rx.text("Información Personal", weight="bold", size="3", color="#4B5563"),
                        
                        form_field("Nombre", "Tu nombre", RegisterState.nombre, RegisterState.set_nombre, icon="user"),
                        form_field("Apellido", "Tu apellido", RegisterState.apellido, RegisterState.set_apellido, icon="user-check"),
                        form_field("DNI / NIE", "12345678Z", RegisterState.dni, RegisterState.set_dni, icon="id-card"),
                        
                        rx.vstack(
                            rx.text("Tipo de usuario", weight="medium", size="2", color="#374151"),
                            rx.select(
                                ["estudiante", "profesor", "personal_comedor"],
                                value=RegisterState.tipo,
                                on_change=RegisterState.set_tipo,
                                width="100%",
                                size="3",
                                radius="large",
                            ),
                            spacing="1",
                            width="100%",
                            align="start",
                        ),

                        rx.cond(
                            RegisterState.show_grado,
                            form_field(
                                "Grado o Facultad",
                                "Ej: Grado en Ingeniería Informática",
                                RegisterState.grado,
                                RegisterState.set_grado,
                                icon="graduation-cap",
                            ),
                        ),

                        rx.cond(
                            RegisterState.show_especialidad,
                            form_field(
                                "Especialidad en cocina",
                                "Ej: Responsable de línea / Cocina",
                                RegisterState.especialidad,
                                RegisterState.set_especialidad,
                                icon="chef-hat",
                            ),
                        ),

                        spacing="3",
                        width="100%",
                    ),

                    rx.vstack(
                        rx.text("Contacto y Seguridad", weight="bold", size="3", color="#4B5563"),
                        
                        rx.vstack(
                            form_field(
                                "Correo electrónico",
                                "nombre@estudiantes.unileon.es",
                                RegisterState.email,
                                RegisterState.set_email,
                                icon="mail",
                            ),
                            rx.text(
                                RegisterState.email_help_text,
                                size="1",
                                color="#6B7280",
                            ),
                            spacing="1",
                            width="100%",
                        ),

                        form_field("Teléfono", "600123456", RegisterState.telefono, RegisterState.set_telefono, icon="phone"),
                        form_field("Contraseña", "••••••••", RegisterState.password, RegisterState.set_password, type_="password", icon="lock"),
                        form_field("Confirmar contraseña", "••••••••", RegisterState.confirm_password, RegisterState.set_confirm_password, type_="password", icon="shield-check"),

                        spacing="3",
                        width="100%",
                    ),

                    columns="2",
                    spacing="5",
                    width="100%",
                    padding_y="0.5em",
                ),

                rx.cond(
                    RegisterState.error_message != "",
                    rx.callout(
                        RegisterState.error_message,
                        icon="triangle-alert",
                        color_scheme="red",
                        width="100%",
                        radius="large",
                    ),
                ),

                rx.cond(
                    RegisterState.success_message != "",
                    rx.callout(
                        RegisterState.success_message,
                        icon="circle-check",
                        color_scheme="green",
                        width="100%",
                        radius="large",
                    ),
                ),

                rx.vstack(
                    rx.button(
                        "Crear mi cuenta",
                        on_click=RegisterState.register,
                        loading=RegisterState.is_loading,
                        width="100%",
                        size="3",
                        color_scheme="violet",
                        cursor="pointer",
                        radius="large",
                    ),
                    rx.hstack(
                        rx.text("¿Ya tienes cuenta?", size="2", color="gray"),
                        rx.link(
                            "Inicia sesión aquí",
                            href="/",
                            size="2",
                            color_scheme="violet",
                            weight="bold",
                        ),
                        spacing="1",
                        justify="center",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                    margin_top="0.5em",
                ),

                spacing="4",
                width="100%",
            ),
            width="780px",
            max_width="95vw",
            padding="2.5em",
            border_radius="24px",
            box_shadow="0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01)",
            background="#FFFFFF",
        ),
        width="100%",
        min_height="100vh",
        background="#F8FAFC",
        padding_y="2em",
    )