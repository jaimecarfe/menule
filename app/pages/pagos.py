import reflex as rx

from app.components.layout import layout
from app.states.auth_state import AppState
from app.states.pago_state import PagoState, PagoSchema


def kpi_card(titulo: str, valor: str, icono: str, color: str) -> rx.Component:
    """Tarjeta de métrica destacada."""
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.text(titulo, size="2", color="gray"),
                rx.heading(valor, size="6"),
                align_items="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.icon(icono, size=28, color=rx.color(color, 9)),
            align="center",
            width="100%",
        ),
        width="100%",
        padding="1.25em",
        border_radius="16px",
    )


def badge_metodo(metodo: str) -> rx.Component:
    """Badge estilizado para el método de pago."""
    return rx.match(
        metodo,
        ("tui", rx.badge("TUI", color_scheme="blue", variant="soft")),
        ("bono", rx.badge("Bono", color_scheme="purple", variant="soft")),
        ("tarjeta", rx.badge("Tarjeta", color_scheme="green", variant="soft")),
        ("efectivo", rx.badge("Efectivo", color_scheme="orange", variant="soft")),
        rx.badge(metodo, color_scheme="gray", variant="soft"),
    )


def selector_estado_interactivo(pago: PagoSchema) -> rx.Component:
    """Desplegable para cambiar de estado al instante."""
    badge_actual = rx.match(
        pago.estado,
        ("completado", rx.badge("Completado", color_scheme="green", variant="solid")),
        ("pendiente", rx.badge("Pendiente", color_scheme="amber", variant="solid")),
        ("reembolsado", rx.badge("Reembolsado", color_scheme="blue", variant="solid")),
        ("fallido", rx.badge("Fallido", color_scheme="red", variant="solid")),
        rx.badge(pago.estado, color_scheme="gray", variant="solid"),
    )

    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                badge_actual,
                rx.icon("chevron-down", size=14),
                variant="ghost",
                size="1",
                cursor="pointer",
            )
        ),
        rx.menu.content(
            rx.menu.item(
                "Marcar Completado",
                on_click=lambda: PagoState.cambiar_estado_pago(pago.id_pago, "completado"),
            ),
            rx.menu.item(
                "Marcar Pendiente",
                on_click=lambda: PagoState.cambiar_estado_pago(pago.id_pago, "pendiente"),
            ),
            rx.menu.item(
                "Marcar Reembolsado",
                on_click=lambda: PagoState.cambiar_estado_pago(pago.id_pago, "reembolsado"),
            ),
            rx.menu.item(
                "Marcar Fallido",
                color_scheme="red",
                on_click=lambda: PagoState.cambiar_estado_pago(pago.id_pago, "fallido"),
            ),
        ),
    )


def user_pagos_view() -> rx.Component:
    """Vista de Monedero TUI y Pagos para Estudiantes / Profesores."""
    return rx.vstack(
        # Cabecera
        rx.vstack(
            rx.heading("Mi Monedero TUI", size="8"),
            rx.text(
                "Consulta tu saldo disponible, recarga crédito y revisa tus movimientos.",
                color="gray",
            ),
            align_items="start",
            spacing="1",
            width="100%",
        ),

        # TARJETA TUI VIRTUAL Y MODAL DE RECARGA
        rx.grid(
            # Tarjeta Virtual Estilizada
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.text("Tarjeta Universitaria (TUI)", weight="bold", color="white", size="3"),
                        rx.spacer(),
                        rx.icon("nfc", color="white", size=24),
                        width="100%",
                    ),
                    rx.spacer(),
                    rx.vstack(
                        rx.text("Saldo Disponible", size="2", color="#E5E7EB"),
                        rx.heading(f"{PagoState.saldo_actual:.2f} €", size="9", color="white", weight="bold"),
                        align_items="start",
                        spacing="1",
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.text(PagoState.numero_tui, color="#9CA3AF", size="2"),
                        rx.spacer(),
                        rx.badge("Activa", color_scheme="green", radius="full"),
                        width="100%",
                        align="center",
                    ),
                    height="220px",
                    justify="between",
                ),
                width="100%",
                padding="1.5em",
                style={
                    "background": "linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%)",
                    "borderRadius": "24px",
                    "boxShadow": "0 10px 25px -5px rgba(67, 56, 202, 0.4)",
                },
            ),

            # Panel de Recarga Rápida
            rx.card(
                rx.vstack(
                    rx.heading("Recargar Saldo", size="5"),
                    rx.text("Selecciona el importe y la forma de pago para añadir saldo al instante.", size="2", color="gray"),
                    rx.divider(),
                    
                    rx.vstack(
                        rx.text("Importe a recargar (€)", size="2", weight="bold"),
                        rx.hstack(
                            rx.button("5 €", variant="soft", color_scheme="indigo", on_click=lambda: PagoState.set_monto_recarga("5")),
                            rx.button("10 €", variant="soft", color_scheme="indigo", on_click=lambda: PagoState.set_monto_recarga("10")),
                            rx.button("20 €", variant="soft", color_scheme="indigo", on_click=lambda: PagoState.set_monto_recarga("20")),
                            rx.button("50 €", variant="soft", color_scheme="indigo", on_click=lambda: PagoState.set_monto_recarga("50")),
                            spacing="2",
                        ),
                        rx.input(
                            placeholder="Otro importe...",
                            value=PagoState.monto_recarga,
                            on_change=PagoState.set_monto_recarga,
                            width="100%",
                            radius="large",
                        ),
                        align_items="start",
                        width="100%",
                        spacing="2",
                    ),

                    rx.button(
                        rx.icon("wallet"),
                        "Confirmar Recarga",
                        on_click=PagoState.realizar_recarga,
                        color_scheme="indigo",
                        size="3",
                        radius="large",
                        width="100%",
                    ),
                    spacing="4",
                    justify="between",
                    height="100%",
                ),
                width="100%",
                padding="1.5em",
                border_radius="24px",
            ),
            columns=rx.breakpoints(initial="1", md="2"),
            spacing="5",
            width="100%",
        ),

        # HISTORIAL DE MOVIMIENTOS Y GASTOS
        rx.card(
            rx.vstack(
                rx.heading("Historial de Transacciones", size="5"),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("ID Transacción"),
                            rx.table.column_header_cell("Monto"),
                            rx.table.column_header_cell("Método"),
                            rx.table.column_header_cell("Estado"),
                            rx.table.column_header_cell("Fecha y Hora"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            PagoState.pagos,
                            lambda p: rx.table.row(
                                rx.table.cell(f"#{p.id_pago}"),
                                rx.table.cell(
                                    rx.text(f"{p.monto:.2f} €", weight="bold")
                                ),
                                rx.table.cell(badge_metodo(p.metodo)),
                                rx.table.cell(
                                    rx.badge(
                                        p.estado.capitalize(),
                                        color_scheme=rx.cond(p.estado == "completado", "green", "amber"),
                                        variant="soft",
                                    )
                                ),
                                rx.table.cell(p.fecha_pago),
                            ),
                        )
                    ),
                    variant="surface",
                    size="3",
                    width="100%",
                ),
                width="100%",
                spacing="3",
            ),
            width="100%",
            padding="1.5em",
            border_radius="20px",
        ),

        spacing="5",
        width="100%",
        on_mount=PagoState.load_pagos,
    )


def admin_pagos_view() -> rx.Component:
    """Vista de Auditoría para Administradores."""
    return rx.vstack(
        # Cabecera
        rx.vstack(
            rx.heading("Auditoría de Pagos", size="8"),
            rx.text(
                "Registro global de transacciones financieras y estados de cobro.",
                color="gray",
            ),
            align_items="start",
            spacing="1",
            width="100%",
        ),

        # Fila de Métricas / KPIs
        rx.grid(
            kpi_card("Recaudación Total", f"{PagoState.kpi_ingresos:.2f} €", "circle-dollar-sign", "green"),
            kpi_card("Transacciones", f"{PagoState.kpi_operaciones}", "receipt", "blue"),
            kpi_card("Uso TUI / Bono", f"{PagoState.kpi_tui_bono}", "credit-card", "purple"),
            kpi_card("Pagos Visitantes", f"{PagoState.kpi_visitantes}", "users", "orange"),
            columns=rx.breakpoints(initial="1", sm="2", md="4"),
            spacing="4",
            width="100%",
        ),

        # Filtros y Búsqueda
        rx.card(
            rx.hstack(
                rx.input(
                    placeholder="Buscar por ID, Reserva o Correo...",
                    value=PagoState.search_text,
                    on_change=PagoState.set_search_text,
                    width="320px",
                    radius="large",
                ),
                rx.button(
                    rx.icon("search"),
                    "Buscar",
                    on_click=PagoState.load_pagos,
                    variant="soft",
                    color_scheme="gray",
                    radius="large",
                ),
                rx.spacer(),
                rx.segmented_control.root(
                    rx.segmented_control.item("Todos", value="todos"),
                    rx.segmented_control.item("TUI", value="tui"),
                    rx.segmented_control.item("Bono", value="bono"),
                    rx.segmented_control.item("Tarjeta", value="tarjeta"),
                    rx.segmented_control.item("Efectivo", value="efectivo"),
                    value=PagoState.filtro_metodo,
                    on_change=PagoState.set_filtro_metodo,
                    radius="large",
                ),
                width="100%",
                align="center",
            ),
            width="100%",
            padding="1.25em",
            border_radius="20px",
        ),

        # Tabla de Pagos con Selector Interactivo
        rx.card(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID Pago"),
                        rx.table.column_header_cell("Usuario / Correo"),
                        rx.table.column_header_cell("ID Reserva"),
                        rx.table.column_header_cell("Monto"),
                        rx.table.column_header_cell("Método"),
                        rx.table.column_header_cell("Estado (Click para cambiar)"),
                        rx.table.column_header_cell("Fecha"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        PagoState.pagos,
                        lambda p: rx.table.row(
                            rx.table.cell(f"#{p.id_pago}"),
                            rx.table.cell(p.correo),
                            rx.table.cell(
                                rx.cond(
                                    p.id_reserva.is_none(),
                                    "-",
                                    f"#{p.id_reserva}",
                                )
                            ),
                            rx.table.cell(
                                rx.text(f"{p.monto:.2f} €", weight="bold")
                            ),
                            rx.table.cell(badge_metodo(p.metodo)),
                            rx.table.cell(selector_estado_interactivo(p)),
                            rx.table.cell(p.fecha_pago),
                        ),
                    )
                ),
                variant="surface",
                size="3",
                width="100%",
            ),
            width="100%",
            padding="1.5em",
            border_radius="20px",
        ),

        spacing="5",
        width="100%",
        on_mount=PagoState.load_pagos,
    )


def pagos_page() -> rx.Component:
    """Renderizado condicional según rol."""
    return layout(
        rx.cond(
            AppState.is_admin,
            admin_pagos_view(),
            user_pagos_view(),
        )
    )