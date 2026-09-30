import reflex as rx

from app.states.auth_state import AppState


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # ==========================================
            # LOGO MENULE Y BRANDING
            # ==========================================
            rx.link(
                rx.hstack(
                    rx.image(
                        src="/logo_menule.png",
                        width="46px",
                        height="46px",
                        object_fit="contain",
                        style={
                            "filter": "drop-shadow(0 2px 4px rgba(0,0,0,0.15))",
                            "transition": "transform 0.2s ease",
                        },
                        _hover={
                            "transform": "scale(1.05)",
                        },
                    ),
                    rx.heading(
                        "MenULE",
                        size="6",
                        weight="bold",
                        color="#111827",
                        style={
                            "letterSpacing": "-0.5px",
                        },
                    ),
                    spacing="3",
                    align="center",
                ),
                href="/home",
                underline="none",
            ),

            rx.spacer(),

            # ==========================================
            # USUARIO & PERFIL
            # ==========================================
            rx.hstack(
                # Círculo Violeta con Iniciales
                rx.center(
                    rx.text(
                        AppState.user_initials,
                        font_size="15px",
                        weight="bold",
                        color="#6D28D9",
                    ),
                    background="#F3E8FF",
                    border_radius="full",
                    width="40px",
                    height="40px",
                    display="flex",
                    align_items="center",
                    justify="center",
                ),

                # Info del usuario
                rx.vstack(
                    rx.text(
                        AppState.user_name,
                        weight="bold",
                        size="2",
                        color="#1F2937",
                        style={"lineHeight": "1.2"},
                    ),
                    rx.badge(
                        AppState.user_role,
                        color_scheme="violet",
                        variant="soft",
                        size="1",
                        radius="full",
                    ),
                    spacing="1",
                    align_items="start",
                    justify="center",
                ),

                # Botón de salir
                rx.button(
                    rx.icon("log-out", size=16),
                    rx.text("Cerrar sesión"),
                    color_scheme="red",
                    variant="soft",
                    size="2",
                    radius="large",
                    on_click=AppState.logout,
                    cursor="pointer",
                    margin_left="0.5em",
                ),

                spacing="3",
                align="center",
            ),

            width="100%",
            height="100%",
            align="center",
            justify="between",
        ),

        width="100%",
        height="72px",
        padding_x="2.5em",
        background="rgba(255, 255, 255, 0.95)",
        style={
            "backdropFilter": "blur(12px)",
            "WebkitBackdropFilter": "blur(12px)",
        },
        border_bottom="1px solid #E5E7EB",
        box_shadow="0 4px 20px rgba(0,0,0,.03)",
        position="sticky",
        top="0",
        z_index="100",
    )