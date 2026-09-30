import reflex as rx
from app.states.auth_state import AppState


def login_page() -> rx.Component:
    return rx.flex(
        # PANEL IZQUIERDO (Se oculta en móviles para que no rompa la pantalla)
        rx.box(
            rx.box(
                rx.vstack(
                    rx.spacer(),
                    rx.image(
                        src="/logo_menule.png",
                        width=["250px", "300px", "380px"],
                        height="auto",
                        style={
                            "filter": "drop-shadow(0 12px 30px rgba(0,0,0,.5))",
                            "transition": "transform 0.4s ease",
                        },
                        _hover={"transform": "scale(1.03)"},
                    ),
                    rx.heading(
                        "MenULE",
                        size="9",
                        color="white",
                        weight="bold",
                        style={
                            "letterSpacing": "-1.5px",
                            "textShadow": "0 8px 28px rgba(0,0,0,.45)",
                        },
                    ),
                    rx.text(
                        "Sistema inteligente para la gestión\n"
                        "de comedores universitarios",
                        white_space="pre-line",
                        color="rgba(255,255,255,.94)",
                        size="4",
                        text_align="center",
                        max_width="520px",
                        style={
                            "lineHeight": "1.6",
                            "textShadow": "0 3px 10px rgba(0,0,0,.45)",
                        },
                    ),
                    rx.hstack(
                        rx.badge("Reservas", color_scheme="violet", radius="full", variant="solid", size="3"),
                        rx.badge("Pagos", color_scheme="green", radius="full", variant="solid", size="3"),
                        rx.badge("Incidencias", color_scheme="orange", radius="full", variant="solid", size="3"),
                        spacing="3",
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.box(
                            rx.image(src="/logo.png", width="90px"),
                            background="rgba(255,255,255,.96)",
                            padding="0.8em 1.2em",
                            border_radius="18px",
                            box_shadow="0 12px 35px rgba(0,0,0,.25)",
                            transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                            _hover={
                                "transform": "translateY(-4px) scale(1.02)",
                                "boxShadow": "0 18px 40px rgba(0,0,0,.35)",
                            },
                        ),
                        rx.box(
                            rx.image(src="/logo_eeia.png", width="90px"),
                            background="rgba(255,255,255,.96)",
                            padding="0.8em 1.2em",
                            border_radius="18px",
                            box_shadow="0 12px 35px rgba(0,0,0,.25)",
                            transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                            _hover={
                                "transform": "translateY(-4px) scale(1.02)",
                                "boxShadow": "0 18px 40px rgba(0,0,0,.35)",
                            },
                        ),
                        spacing="4",
                    ),
                    rx.text(
                        "Universidad de León · Escuela de Ingeniería\nInformática, Industrial y Aeroespacial",
                        color="rgba(255,255,255,.8)",
                        text_align="center",
                        size="2",
                        white_space="pre-line",
                    ),
                    height="100%",
                    width="100%",
                    padding=["1.5em", "2em", "3.5em"],
                    align="center",
                ),
                width="100%",
                height="100%",
                background="""
                linear-gradient(
                180deg,
                rgba(18,22,35,.20) 0%,
                rgba(18,22,35,.50) 40%,
                rgba(18,22,35,.88) 100%
                )
                """,
            ),
            width=["100%", "100%", "58%"],
            min_height=["300px", "400px", "100vh"],
            display=["none", "none", "block"],  # 👈 Oculto en móviles
            background_image="url('/comedor.jpg')",
            background_size="cover",
            background_position="center",
        ),
        # PANEL DERECHO (Formulario de Login)
        rx.center(
            rx.card(
                rx.vstack(
                    rx.vstack(
                        rx.badge("Universidad de León", color_scheme="violet", radius="full", size="2"),
                        rx.heading("Bienvenido", size="7", weight="bold", color="#111827"),
                        rx.text("Accede con tu cuenta institucional", size="2", color="gray", text_align="center"),
                        spacing="2",
                        align="center",
                        width="100%",
                    ),
                    rx.divider(),
                    
                    rx.vstack(
                        rx.text("Correo electrónico", weight="medium", size="2", color="#374151", width="100%"),
                        rx.input(
                            rx.input.slot(rx.icon("mail", size=18, color="#9CA3AF")),
                            placeholder="nombre@unileon.es",
                            value=AppState.email,
                            on_change=AppState.set_email,
                            size="3",
                            width="100%",
                            radius="large",
                        ),
                        spacing="1",
                        width="100%",
                        align="start",
                    ),

                    rx.vstack(
                        rx.text("Contraseña", weight="medium", size="2", color="#374151", width="100%"),
                        rx.input(
                            rx.input.slot(rx.icon("lock", size=18, color="#9CA3AF")),
                            placeholder="••••••••",
                            type="password",
                            value=AppState.password,
                            on_change=AppState.set_password,
                            size="3",
                            width="100%",
                            radius="large",
                        ),
                        spacing="1",
                        width="100%",
                        align="start",
                    ),

                    rx.cond(
                        AppState.error_message != "",
                        rx.callout(
                            AppState.error_message,
                            icon="triangle-alert",
                            color_scheme="red",
                            width="100%",
                            radius="large",
                        ),
                    ),

                    rx.button(
                        rx.icon("log-in", size=18),
                        rx.text("Iniciar sesión", weight="bold"),
                        on_click=AppState.login,
                        loading=AppState.is_loading,
                        width="100%",
                        size="3",
                        height="48px",
                        radius="large",
                        color_scheme="violet",
                        cursor="pointer",
                        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
                        _hover={
                            "transform": "translateY(-2px)",
                            "boxShadow": "0 8px 20px rgba(124, 58, 237, 0.35)",
                        },
                        _active={"transform": "translateY(0)"},
                    ),

                    rx.hstack(
                        rx.divider(width="40%"),
                        rx.text("o", color="#9CA3AF", size="2", weight="medium"),
                        rx.divider(width="40%"),
                        align="center",
                        justify="between",
                        width="100%",
                        padding_y="0.2em",
                    ),

                    rx.button(
                        rx.icon("user-check", size=18),
                        rx.text("Acceder como visitante"),
                        variant="soft",
                        color_scheme="gray",
                        width="100%",
                        size="3",
                        height="48px",
                        radius="large",
                        cursor="pointer",
                        on_click=AppState.login_visitante,
                        transition="all 0.2s ease",
                        _hover={"background": "#E5E7EB"},
                    ),

                    rx.divider(),

                    rx.hstack(
                        rx.text("¿No tienes cuenta?", color="gray", size="2"),
                        rx.link(
                            "Crear una cuenta",
                            href="/registro",
                            weight="bold",
                            color_scheme="violet",
                            size="2",
                        ),
                        spacing="2",
                        justify="center",
                        width="100%",
                        wrap="wrap",
                    ),
                    spacing="4",
                    width="100%",
                    align="center",
                ),
                width="100%",
                max_width="450px",
                padding=["1.5em", "2em", "3em"],
                border_radius="28px",
                background="rgba(255,255,255,0.85)",
                style={
                    "backdropFilter": "blur(24px)",
                    "WebkitBackdropFilter": "blur(24px)",
                    "boxShadow": "0 20px 50px rgba(0,0,0,0.08), 0 10px 20px rgba(0,0,0,0.04)",
                    "border": "1px solid rgba(255, 255, 255, 0.6)",
                    "transition": "all .3s cubic-bezier(0.4, 0, 0.2, 1)",
                },
                _hover={
                    "transform": "translateY(-4px)",
                    "boxShadow": "0 30px 70px rgba(0,0,0,0.12), 0 15px 30px rgba(0,0,0,0.06)",
                },
            ),
            width=["100%", "100%", "42%"],
            min_height="100vh",
            padding="1.5em",
            background="#F8FAFC",
        ),
        flex_direction=["column", "column", "row"],  # 👈 CORREGIDO: flex_direction CSS nativo
        width="100vw",
        min_height="100vh",
    )