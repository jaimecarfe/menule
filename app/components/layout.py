import reflex as rx
from datetime import datetime
from app.components.sidebar import sidebar
from app.states.auth_state import AppState


def _fecha_hoy_es() -> str:
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    ]
    hoy = datetime.now()
    return f"{hoy.day} {meses[hoy.month - 1]} {hoy.year}"


def _saludo_segun_hora() -> str:
    hora = datetime.now().hour
    if 5 <= hora < 12:
        return "Buenos días, "
    elif 12 <= hora < 20:
        return "Buenas tardes, "
    else:
        return "Buenas noches, "


def campana_notificaciones() -> rx.Component:
    """Componente con Popover funcional para desplegar alertas individuales por usuario."""
    return rx.popover.root(
        rx.popover.trigger(
            rx.box(
                rx.button(
                    rx.icon("bell", size=16),
                    variant="soft",
                    color_scheme=rx.cond(
                        AppState.notificaciones.length() > 0,
                        "amber",
                        "gray",
                    ),
                    size="2",
                    radius="large",
                ),
                rx.cond(
                    AppState.notificaciones.length() > 0,
                    rx.badge(
                        AppState.notificaciones.length(),
                        color_scheme="red",
                        radius="full",
                        size="1",
                        position="absolute",
                        top="-4px",
                        right="-4px",
                    ),
                ),
                position="relative",
            )
        ),
        rx.popover.content(
            rx.vstack(
                rx.hstack(
                    rx.text("Notificaciones y Avisos", weight="bold", size="2"),
                    rx.spacer(),
                    rx.cond(
                        AppState.notificaciones.length() > 0,
                        rx.button(
                            "Limpiar",
                            size="1",
                            variant="ghost",
                            color_scheme="gray",
                            on_click=AppState.limpiar_notificaciones,
                        ),
                    ),
                    width="100%",
                    align="center",
                ),
                rx.divider(),
                rx.cond(
                    AppState.notificaciones.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            AppState.notificaciones,
                            lambda notif: rx.callout(
                                notif,
                                size="1",
                                color_scheme="amber",
                                icon="triangle-alert",
                            ),
                        ),
                        spacing="2",
                        width="100%",
                        max_height="250px",
                        overflow_y="auto",
                    ),
                    rx.text("Sin avisos pendientes.", size="2", color="#6B7280"),
                ),
                spacing="2",
                width="320px",
                padding="0.5em",
            ),
            align="end",
            side="bottom",
        ),
    )


def menu_usuario_dropdown() -> rx.Component:
    """Menú desplegable contextual adaptado para Usuarios Registrados y Visitantes."""
    return rx.dropdown_menu.root(
        rx.dropdown_menu.trigger(
            rx.box(
                rx.avatar(
                    fallback=AppState.user_initials,
                    size="2",
                    radius="full",
                    color_scheme=rx.cond(AppState.is_visitante, "gray", "blue"),
                    high_contrast=False,
                    style={
                        "cursor": "pointer",
                        "transition": "transform 0.2s ease, box-shadow 0.2s ease",
                        "&:hover": {
                            "transform": "scale(1.08)",
                            "box-shadow": "0 0 0 2px var(--blue-8)",
                        },
                    },
                ),
            )
        ),
        rx.dropdown_menu.content(
            # Si es visitante: Texto + Cerrar sesión
            rx.cond(
                AppState.is_visitante,
                rx.fragment(
                    rx.dropdown_menu.item(
                        "Modo Visitante (Sesión no registrada)",
                        disabled=True,
                    ),
                    rx.dropdown_menu.separator(),
                    rx.dropdown_menu.item(
                        rx.hstack(
                            rx.icon("log-out", size=16),
                            "Cerrar Sesión",
                            align="center",
                            spacing="2",
                        ),
                        color_scheme="red",
                        on_click=AppState.logout,
                    ),
                ),
                # Si es usuario registrado: Nombre/Email + Mi Perfil + Cerrar sesión
                rx.fragment(
                    rx.dropdown_menu.item(
                        AppState.user_full_name,
                        disabled=True,
                    ),
                    rx.dropdown_menu.separator(),
                    rx.dropdown_menu.item(
                        rx.hstack(
                            rx.icon("user", size=16),
                            "Mi Perfil",
                            align="center",
                            spacing="2",
                        ),
                        on_click=rx.redirect("/perfil"),
                    ),
                    rx.dropdown_menu.separator(),
                    rx.dropdown_menu.item(
                        rx.hstack(
                            rx.icon("log-out", size=16),
                            "Cerrar Sesión",
                            align="center",
                            spacing="2",
                        ),
                        color_scheme="red",
                        on_click=AppState.logout,
                    ),
                ),
            ),
            align="end",
            side="bottom",
        ),
    )

def navbar() -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text("MenULE", size="2", color="#6B7280"),
            rx.heading(
                rx.text(_saludo_segun_hora(), AppState.user_name),
                size="5",
                weight="bold",
                color="#111827",
            ),
            rx.text(_fecha_hoy_es(), size="2", color="#6B7280"),
            spacing="0",
            align_items="start",
        ),
        rx.spacer(),
        rx.hstack(
            # Buscador estilizado con icono de lupa integrado
            rx.input(
                rx.input.slot(rx.icon("search", size=16, color="gray")),
                placeholder="Buscar en el sistema...",
                width="220px",
                size="2",
                radius="large",
                variant="surface",
            ),
            # Campana individual conectada a AppState
            campana_notificaciones(),
            
            # Avatar con Menú Desplegable Profesional
            menu_usuario_dropdown(),

            rx.button(
                rx.icon("log-out", size=16),
                "Cerrar sesión",
                variant="soft",
                color_scheme="red",
                size="2",
                radius="large",
                on_click=AppState.logout,
            ),
            spacing="3",
            align="center",
        ),
        width="100%",
        padding="0.9em 1.2em",
        background="rgba(255,255,255,0.88)",
        style={
            "backdropFilter": "blur(8px)",
            "WebkitBackdropFilter": "blur(8px)",
        },
        border_bottom="1px solid #E5E7EB",
        position="sticky",
        top="0",
        z_index="20",
        align="center",
    )


def layout(page_content: rx.Component) -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.vstack(
            navbar(),
            rx.box(
                page_content,
                padding="1.25em",
                width="100%",
                max_width="1600px",
                margin="0 auto",
            ),
            flex="1",
            min_height="100vh",
            background="#F8FAFC",
            spacing="0",
            align_items="stretch",
        ),
        width="100%",
        min_height="100vh",
        spacing="0",
        align="stretch",
    )