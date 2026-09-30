import reflex as rx
from app.components.layout import layout
from app.states.auth_state import AppState
from app.states.perfil_state import PerfilState


def campo_dato_perfil(label: str, valor: str, icon_name: str, color_scheme: str = "gray") -> rx.Component:
    """Componente visual para cada dato del usuario con icono y contenedor pulido."""
    return rx.box(
        rx.hstack(
            rx.center(
                rx.icon(icon_name, size=20, color=rx.color(color_scheme, 10)),
                background=rx.color(color_scheme, 3),
                padding="10px",
                border_radius="12px",
            ),
            rx.vstack(
                rx.text(label, size="1", color="gray", weight="medium"),
                rx.text(valor, size="3", weight="bold"),
                align_items="start",
                spacing="0",
            ),
            spacing="3",
            align="center",
        ),
        background=rx.color("gray", 2),
        padding="14px 18px",
        border_radius="14px",
        border=f"1px solid {rx.color('gray', 4)}",
        width="100%",
    )


def modal_cambiar_contrasena() -> rx.Component:
    """Modal estilizado para cambiar contraseña."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.hstack(
                rx.center(
                    rx.icon("shield-check", size=24, color=rx.color("blue", 10)),
                    background=rx.color("blue", 3),
                    padding="12px",
                    border_radius="50%",
                ),
                rx.vstack(
                    rx.dialog.title("Cambiar Contraseña", margin="0", size="5"),
                    rx.dialog.description(
                        "Ingresa tu clave actual y confirma la nueva contraseña.", size="2"
                    ),
                    spacing="1",
                    align_items="start",
                ),
                spacing="3",
                align="center",
                margin_bottom="1.5em",
            ),
            rx.vstack(
                rx.cond(
                    PerfilState.error_msg != "",
                    rx.callout(PerfilState.error_msg, color_scheme="red", icon="circle-alert", width="100%"),
                ),
                rx.cond(
                    PerfilState.success_msg != "",
                    rx.callout(PerfilState.success_msg, color_scheme="green", icon="circle-check", width="100%"),
                ),
                rx.vstack(
                    rx.text("Contraseña Actual", weight="bold", size="2"),
                    rx.input(
                        type="password",
                        placeholder="••••••••",
                        value=PerfilState.pass_actual,
                        on_change=PerfilState.set_pass_actual,
                        width="100%",
                        size="3",
                        radius="large",
                    ),
                    align_items="start",
                    width="100%",
                ),
                rx.vstack(
                    rx.text("Nueva Contraseña", weight="bold", size="2"),
                    rx.input(
                        type="password",
                        placeholder="••••••••",
                        value=PerfilState.pass_nueva,
                        on_change=PerfilState.set_pass_nueva,
                        width="100%",
                        size="3",
                        radius="large",
                    ),
                    align_items="start",
                    width="100%",
                ),
                rx.vstack(
                    rx.text("Repetir Nueva Contraseña", weight="bold", size="2"),
                    rx.input(
                        type="password",
                        placeholder="••••••••",
                        value=PerfilState.pass_repetir,
                        on_change=PerfilState.set_pass_repetir,
                        width="100%",
                        size="3",
                        radius="large",
                    ),
                    align_items="start",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        size="3",
                        radius="large",
                        on_click=PerfilState.cerrar_modal_contrasena,
                    )
                ),
                rx.button(
                    rx.icon("key-round", size=18),
                    "Guardar Cambios",
                    color_scheme="blue",
                    size="3",
                    radius="large",
                    on_click=PerfilState.cambiar_contrasena,
                ),
                spacing="3",
                justify="end",
                margin_top="1.5em",
                width="100%",
            ),
            max_width="480px",
            border_radius="24px",
            padding="2em",
        ),
        open=PerfilState.modal_contrasena_abierto,
    )


def perfil_page() -> rx.Component:
    """Página principal de Mi Perfil con layout totalmente centrado."""
    return layout(
        rx.vstack(
            modal_cambiar_contrasena(),
            
            # Header de la sección (Centrado)
            rx.vstack(
                rx.heading("Mi Perfil", size="8"),
                rx.text("Gestiona tus datos personales y ajustes de seguridad de tu cuenta.", color="gray", align="center"),
                align_items="center",
                spacing="1",
                width="100%",
            ),

            # Card Principal Estilizada y Centrada
            rx.card(
                rx.vstack(
                    # BANNER HEADER
                    rx.hstack(
                        rx.avatar(
                            fallback=AppState.user_initials,
                            size="7",
                            radius="full",
                            color_scheme="blue",
                            high_contrast=True,
                        ),
                        rx.vstack(
                            rx.heading(AppState.user_full_name, size="6", weight="bold"),
                            rx.hstack(
                                rx.badge(
                                    AppState.user_role.upper(),
                                    color_scheme="blue",
                                    variant="solid",
                                    radius="full",
                                ),
                                rx.badge(
                                    "Cuenta Activa",
                                    color_scheme="green",
                                    variant="soft",
                                    radius="full",
                                ),
                                spacing="2",
                            ),
                            align_items="start",
                            spacing="1",
                        ),
                        spacing="4",
                        align="center",
                        width="100%",
                    ),

                    rx.divider(margin_y="1.2em"),

                    # GRID DE DATOS PERSONALES
                    rx.vstack(
                        rx.text("Información Personal y Académica", size="2", weight="bold", color="gray"),
                        rx.grid(
                            campo_dato_perfil("Correo Electrónico", AppState.user_email, "mail", "blue"),
                            campo_dato_perfil("DNI / Identificación", AppState.user_dni, "id-card", "slate"),
                            rx.cond(
                                AppState.is_estudiante | AppState.is_profesor,
                                campo_dato_perfil("Número TUI / Carné", AppState.user_tui_num, "credit-card", "purple"),
                            ),
                            rx.cond(
                                AppState.is_estudiante | AppState.is_profesor,
                                campo_dato_perfil("Saldo Monedero", AppState.user_saldo_str, "wallet", "green"),
                            ),
                            columns=rx.breakpoints(initial="1", sm="2"),
                            spacing="3",
                            width="100%",
                        ),
                        align_items="start",
                        width="100%",
                        spacing="3",
                    ),

                    rx.divider(margin_y="1.5em"),

                    # ACCIONES DE CUENTA
                    rx.hstack(
                        rx.button(
                            rx.icon("key-round", size=18),
                            "Cambiar Contraseña",
                            color_scheme="blue",
                            variant="soft",
                            size="3",
                            radius="large",
                            on_click=PerfilState.abrir_modal_contrasena,
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon("log-out", size=18),
                            "Cerrar Sesión",
                            color_scheme="red",
                            variant="solid",
                            size="3",
                            radius="large",
                            on_click=AppState.logout,
                        ),
                        width="100%",
                        align="center",
                    ),
                    width="100%",
                ),
                width="100%",
                max_width="750px",
                padding="2em",
                border_radius="24px",
                variant="surface",
            ),
            spacing="6",
            width="100%",
            align_items="center",  # <-- Centra todo el contenido dentro del vstack
            margin_x="auto",       # <-- Asegura el centrado horizontal en el contenedor padre
        )
    )