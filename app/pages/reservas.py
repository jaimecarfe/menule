import reflex as rx

from app.components.layout import layout
from app.states.auth_state import AppState
from app.states.reserva_state import ReservaState


def admin_reservas_view() -> rx.Component:
    """Vista de Administración Global de Reservas (Admin / Personal de Comedor)."""
    return rx.vstack(
        rx.vstack(
            rx.heading("Gestión Global de Reservas", size="8"),
            rx.text("Supervisión y control de todas las reservas realizadas en el comedor.", color="gray"),
            align_items="start",
            spacing="1",
            width="100%",
        ),

        # BARRA DE BÚSQUEDA
        rx.card(
            rx.hstack(
                rx.input(
                    placeholder="Buscar por ID de reserva o usuario...",
                    value=ReservaState.search_text,
                    on_change=ReservaState.set_search_text,
                    width="360px",
                    radius="large",
                    size="3",
                ),
                rx.button(
                    rx.icon("search"),
                    "Buscar",
                    on_click=ReservaState.load_reservas,
                    variant="soft",
                    color_scheme="gray",
                    radius="large",
                ),
                rx.spacer(),
                width="100%",
                align="center",
            ),
            width="100%",
            padding="1.25em",
            border_radius="20px",
        ),

        # TABLA DE RESERVAS
        rx.card(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID Reserva"),
                        rx.table.column_header_cell("Usuario"),
                        rx.table.column_header_cell("Menú"),
                        rx.table.column_header_cell("Fecha y Hora"),
                        rx.table.column_header_cell("Estado"),
                        rx.table.column_header_cell("Acciones"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        ReservaState.reservas,
                        lambda res: rx.table.row(
                            rx.table.cell(f"#{res.id_reserva}"),
                            rx.table.cell(res.correo_usuario),
                            rx.table.cell(res.detalle_menu),
                            rx.table.cell(res.fecha_reserva),
                            rx.table.cell(
                                rx.badge(
                                    res.estado.capitalize(),
                                    color_scheme=rx.cond(
                                        res.estado == "confirmada",
                                        "green",
                                        rx.cond(
                                            res.estado == "recogida",
                                            "blue",
                                            rx.cond(res.estado == "cancelada", "red", "amber"),
                                        ),
                                    ),
                                    variant="soft",
                                )
                            ),
                            rx.table.cell(
                                rx.hstack(
                                    rx.button(
                                        rx.icon("eye", size=16),
                                        "Ver Platos",
                                        variant="soft",
                                        color_scheme="violet",
                                        size="2",
                                        on_click=lambda: ReservaState.abrir_detalle(res),
                                    ),
                                    rx.button(
                                        rx.icon("circle-check", size=16),
                                        "Entregado",
                                        variant="soft",
                                        color_scheme="green",
                                        size="2",
                                        on_click=lambda: ReservaState.marcar_recogida(res.id_reserva),
                                    ),
                                    spacing="2",
                                )
                            ),
                        ),
                    ),
                ),
                variant="surface",
                size="3",
                width="100%",
            ),
            width="100%",
            padding="1.5em",
            border_radius="20px",
        ),

        # MODAL DETALLE DE PLATOS PARA EL COMEDOR
        rx.dialog.root(
            rx.dialog.content(
                rx.cond(
                    ReservaState.reserva_seleccionada,
                    rx.vstack(
                        rx.heading("Detalle de Comanda / Reserva", size="5"),
                        rx.hstack(
                            rx.text("ID Reserva:", weight="bold"),
                            rx.badge(f"#{ReservaState.reserva_seleccionada.id_reserva}", color_scheme="violet"),
                            spacing="2",
                        ),
                        rx.hstack(
                            rx.text("Usuario:", weight="bold"),
                            rx.text(ReservaState.reserva_seleccionada.correo_usuario),
                            spacing="2",
                        ),
                        rx.divider(),
                        rx.text("Platos Seleccionados por el Cliente:", weight="bold", size="3"),
                        rx.box(
                            rx.vstack(
                                rx.foreach(
                                    ReservaState.reserva_seleccionada.platos_lista,
                                    lambda plato: rx.hstack(
                                        rx.icon("chef-hat", size=18, color="#7C3AED"),
                                        rx.text(plato, size="3", weight="medium"),
                                        align="center",
                                        spacing="2",
                                    ),
                                ),
                                spacing="2",
                                align_items="start",
                            ),
                            background="#F9FAFB",
                            padding="1em",
                            border_radius="12px",
                            width="100%",
                        ),
                        rx.hstack(
                            rx.button("Cerrar", variant="soft", color_scheme="gray", on_click=ReservaState.cerrar_detalle),
                            justify="end",
                            width="100%",
                            margin_top="1em",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                ),
                max_width="450px",
            ),
            open=ReservaState.show_modal_detalle,
            on_open_change=ReservaState.set_show_modal_detalle,
        ),

        spacing="5",
        width="100%",
        on_mount=ReservaState.load_reservas,
    )


def user_reservas_view() -> rx.Component:
    """Vista Individual de Historial y Tickets (Estudiante / Profesor)."""
    return rx.vstack(
        rx.card(
            rx.hstack(
                rx.vstack(
                    rx.badge("Mis Tickets", color_scheme="purple", variant="surface", radius="full"),
                    rx.heading("Historial de Reservas", size="6", weight="bold", color="#111827"),
                    rx.text(
                        "Consulta el estado de tus menús reservados y presenta tus códigos QR.",
                        color="#4B5563",
                        size="3",
                    ),
                    spacing="2",
                    align_items="start",
                ),
                rx.spacer(),
                align="center",
                width="100%",
            ),
            width="100%",
            padding="1.8em",
            style={
                "borderRadius": "22px",
                "background": "linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%)",
                "border": "1px solid #E5E7EB",
            },
        ),

        # TARJETAS DE TICKETS CON QR Y PLATOS
        rx.cond(
            ReservaState.reservas.length() > 0,
            rx.grid(
                rx.foreach(
                    ReservaState.reservas,
                    lambda res: rx.card(
                        rx.vstack(
                            rx.hstack(
                                rx.badge(f"Ticket #{res.id_reserva}", color_scheme="violet", radius="large"),
                                rx.badge(
                                    res.estado.capitalize(),
                                    color_scheme=rx.cond(
                                        res.estado == "confirmada",
                                        "green",
                                        rx.cond(res.estado == "recogida", "blue", "red"),
                                    ),
                                    radius="large",
                                ),
                                justify="between",
                                width="100%",
                            ),
                            rx.divider(),
                            rx.vstack(
                                rx.text(f"Fecha: {res.fecha_reserva}", weight="bold", size="2"),
                                rx.text(f"Menú Referencia: #{res.id_menu}", size="2", color="gray"),
                                align_items="start",
                                spacing="1",
                            ),

                            # PLATOS ELEGIDOS POR EL USUARIO
                            rx.vstack(
                                rx.text("Mis Platos Pedidos:", weight="bold", size="2", color="#7C3AED"),
                                rx.foreach(
                                    res.platos_lista,
                                    lambda plato: rx.hstack(
                                        rx.icon("utensils", size=14, color="#7C3AED"),
                                        rx.text(plato, size="2", weight="medium"),
                                        align="center",
                                        spacing="2",
                                    ),
                                ),
                                align_items="start",
                                spacing="1",
                                width="100%",
                                background="#F9FAFB",
                                padding="0.8em",
                                border_radius="10px",
                            ),

                            # CÓDIGO QR DE VALIDACIÓN
                            rx.center(
                                rx.image(
                                    src=f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=TICKET_{res.id_reserva}",
                                    alt="Código QR de Validación",
                                    width="130px",
                                    height="130px",
                                ),
                                width="100%",
                                padding_y="0.5em",
                            ),

                            rx.spacer(),
                            rx.button(
                                rx.icon("refresh-cw", size=16),
                                "Refrescar Estado",
                                color_scheme="gray",
                                variant="soft",
                                radius="large",
                                size="2",
                                width="100%",
                                on_click=ReservaState.load_reservas,
                            ),
                            spacing="3",
                            height="100%",
                        ),
                        width="100%",
                        padding="1.2em",
                        style={"borderRadius": "16px"},
                    ),
                ),
                columns="3",
                spacing="4",
                width="100%",
            ),
            rx.card(
                rx.vstack(
                    rx.icon("ticket", size=48, color="#9CA3AF"),
                    rx.heading("No tienes reservas activas", size="4", color="#374151"),
                    rx.text("Haz tu reserva desde la sección 'Menú del Día'.", color="#6B7280", size="2"),
                    align="center",
                    spacing="2",
                    padding="3em",
                ),
                width="100%",
                style={"borderRadius": "20px", "border": "1px dashed #D1D5DB"},
            ),
        ),

        spacing="5",
        width="100%",
        on_mount=ReservaState.load_reservas,
    )


def reservas_page() -> rx.Component:
    """Renderiza según el Rol."""
    return layout(
        rx.cond(
            AppState.is_admin,
            admin_reservas_view(),
            user_reservas_view(),
        )
    )