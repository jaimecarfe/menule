import reflex as rx
from app.components.layout import layout
from app.states.estadistica_state import EstadisticaState


def seccion_pagos() -> rx.Component:
    """Componente para renderizar la analítica financiera por rol."""
    return rx.vstack(
        rx.grid(
            # Tabla explicativa por rol
            rx.card(
                rx.vstack(
                    rx.heading("Desglose Financiero por Rol", size="4"),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Rol / Tipo Usuario"),
                                rx.table.column_header_cell("Nº Transacciones"),
                                rx.table.column_header_cell("Total Pagado (€)"),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                EstadisticaState.datos_pagos_rol,
                                lambda item: rx.table.row(
                                    rx.table.cell(rx.badge(item["rol"], color_scheme="violet")),
                                    rx.table.cell(item["cantidad_pagos"]),
                                    rx.table.cell(f"{item['total_pagado']:.2f} €", weight="bold"),
                                ),
                            )
                        ),
                        variant="surface",
                        width="100%",
                    ),
                ),
                padding="1.5em",
                border_radius="16px",
            ),
            # Gráfico de barras de Ingresos por Rol
            rx.card(
                rx.vstack(
                    rx.heading("Comparativa de Ingresos por Rol", size="4"),
                    rx.recharts.bar_chart(
                        rx.recharts.bar(
                            data_key="total_pagado",
                            fill=rx.color("violet", 9),
                            radius=[6, 6, 0, 0],
                        ),
                        rx.recharts.x_axis(data_key="rol"),
                        rx.recharts.y_axis(),
                        rx.recharts.tooltip(),
                        data=EstadisticaState.datos_pagos_rol,
                        height=260,
                        width="100%",
                    ),
                ),
                padding="1.5em",
                border_radius="16px",
            ),
            columns=rx.breakpoints(initial="1", lg="2"),
            spacing="4",
            width="100%",
        ),
        width="100%",
    )


def seccion_incidencias() -> rx.Component:
    """Componente para renderizar la métrica de soporte e incidencias."""
    return rx.vstack(
        rx.grid(
            # Tabla de Incidencias por Rol
            rx.card(
                rx.vstack(
                    rx.heading("Volumen de Soporte por Rol", size="4"),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Rol / Perfil"),
                                rx.table.column_header_cell("Cantidad de Incidencias"),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                EstadisticaState.datos_incidencias_rol,
                                lambda item: rx.table.row(
                                    rx.table.cell(rx.badge(item["rol"], color_scheme="amber")),
                                    rx.table.cell(item["cantidad_incidencias"], weight="bold"),
                                ),
                            )
                        ),
                        variant="surface",
                        width="100%",
                    ),
                ),
                padding="1.5em",
                border_radius="16px",
            ),
            # Gráfico de Tarta / Área de Incidencias
            rx.card(
                rx.vstack(
                    rx.heading("Distribución de Soporte", size="4"),
                    rx.recharts.bar_chart(
                        rx.recharts.bar(
                            data_key="cantidad_incidencias",
                            fill=rx.color("amber", 9),
                            radius=[6, 6, 0, 0],
                        ),
                        rx.recharts.x_axis(data_key="rol"),
                        rx.recharts.y_axis(),
                        rx.recharts.tooltip(),
                        data=EstadisticaState.datos_incidencias_rol,
                        height=260,
                        width="100%",
                    ),
                ),
                padding="1.5em",
                border_radius="16px",
            ),
            columns=rx.breakpoints(initial="1", lg="2"),
            spacing="4",
            width="100%",
        ),
        width="100%",
    )


def seccion_evolucion_diaria() -> rx.Component:
    """Explota la vista VistaEstadisticasDiarias de SQL."""
    return rx.card(
        rx.vstack(
            rx.heading("Tendencia Diaria de Ingresos y Reservas (Vista SQL)", size="4"),
            rx.text("Datos agregados mediante la vista VistaEstadisticasDiarias.", color="gray", size="2"),
            rx.cond(
                EstadisticaState.datos_diarios.length() > 0,
                rx.recharts.area_chart(
                    rx.recharts.area(
                        data_key="ingresos",
                        stroke=rx.color("violet", 9),
                        fill=rx.color("violet", 4),
                        name="Ingresos (€)",
                    ),
                    rx.recharts.x_axis(data_key="fecha"),
                    rx.recharts.y_axis(),
                    rx.recharts.tooltip(),
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                    data=EstadisticaState.datos_diarios,
                    height=300,
                    width="100%",
                ),
                rx.callout("No hay datos registrados en la vista diaria.", icon="info", color_scheme="gray"),
            ),
        ),
        padding="1.5em",
        border_radius="16px",
        width="100%",
    )


def estadisticas_page() -> rx.Component:
    return layout(
        rx.vstack(
            # Cabecera
            rx.hstack(
                rx.vstack(
                    rx.heading("Panel de Estadísticas y Analítica", size="8"),
                    rx.text("Métricas agregadas del sistema por perfil de usuario y rendimiento diario.", color="gray"),
                    align_items="start",
                    spacing="1",
                ),
                rx.spacer(),
                # Selector entre Pagos e Incidencias (Equivalente al QComboBox original)
                rx.segmented_control.root(
                    rx.segmented_control.item("Pagos", value="Pagos"),
                    rx.segmented_control.item("Incidencias", value="Incidencias"),
                    value=EstadisticaState.tipo_vista,
                    on_change=EstadisticaState.set_tipo_vista,
                    radius="large",
                    size="2",
                ),
                width="100%",
                align="center",
            ),

            # Vista condicional según el selector
            rx.match(
                EstadisticaState.tipo_vista,
                ("Pagos", seccion_pagos()),
                ("Incidencias", seccion_incidencias()),
                seccion_pagos(),
            ),

            # Sección inferior: Evolución temporal diaria basada en la vista SQL
            seccion_evolucion_diaria(),

            spacing="6",
            width="100%",
            on_mount=EstadisticaState.load_estadisticas,
        )
    )