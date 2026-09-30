import reflex as rx
from app.components.layout import layout
from app.states.incidencia_state import IncidenciaState
from app.states.auth_state import AppState


def badge_estado(estado: str) -> rx.Component:
    """Badge dinámico según el estado."""
    return rx.match(
        estado,
        ("resuelta", rx.badge("Resuelta", color_scheme="green", variant="solid")),
        ("en_proceso", rx.badge("En proceso", color_scheme="amber", variant="solid")),
        ("abierta", rx.badge("Abierta", color_scheme="red", variant="solid")),
        ("cerrada", rx.badge("Cerrada", color_scheme="gray", variant="solid")),
        rx.badge(estado, color_scheme="gray", variant="soft"),
    )


def modal_responder_incidencia() -> rx.Component:
    """Modal para que el admin responda una incidencia."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Responder Incidencia"),
            rx.dialog.description(
                "Consulta los detalles reportados por el usuario y redacta la solución."
            ),
            rx.cond(
                IncidenciaState.incidencia_seleccionada.is_none(),
                rx.text("Cargando detalles..."),
                rx.vstack(
                    rx.hstack(
                        rx.text("Título:", weight="bold", size="2"),
                        rx.text(IncidenciaState.incidencia_seleccionada.titulo, size="2"),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.text("Usuario:", weight="bold", size="2"),
                        rx.text(IncidenciaState.incidencia_seleccionada.correo_usuario, size="2"),
                        spacing="2",
                    ),
                    rx.vstack(
                        rx.text("Descripción:", weight="bold", size="2"),
                        rx.callout(
                            IncidenciaState.incidencia_seleccionada.descripcion,
                            color_scheme="gray",
                            icon="info",
                        ),
                        align_items="start",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Respuesta / Solución:", weight="bold", size="2"),
                        rx.text_area(
                            placeholder="Escribe aquí la respuesta que se enviará por correo...",
                            value=IncidenciaState.texto_respuesta,
                            on_change=IncidenciaState.set_texto_respuesta,
                            rows="5",
                            width="100%",
                        ),
                        align_items="start",
                        width="100%",
                    ),
                    spacing="4",
                    margin_top="1em",
                ),
            ),
            rx.hstack(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="gray", on_click=IncidenciaState.cerrar_modal)
                ),
                rx.button(
                    rx.icon("send", size=16),
                    "Enviar Respuesta",
                    color_scheme="green",
                    on_click=IncidenciaState.enviar_respuesta,
                ),
                spacing="3",
                justify="end",
                margin_top="1.5em",
            ),
            max_width="550px",
            border_radius="16px",
        ),
        open=IncidenciaState.modal_abierto,
    )

def modal_nueva_incidencia() -> rx.Component:
    """Modal para que Estudiantes y Profesores reporten incidencias."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Reportar Nueva Incidencia"),
            rx.dialog.description(
                "Describe detalladamente el inconveniente para que el personal correspondiente pueda asistirte."
            ),
            rx.vstack(
                rx.vstack(
                    rx.text("Dirigido a / Departamento", weight="bold", size="2"),

                    rx.select.root(
                        rx.select.trigger(
                            placeholder="Selecciona un departamento",
                            width="100%",
                            radius="large",
                        ),
                        rx.select.content(
                            rx.select.item(
                                "Administración (Pagos, Saldo, TUI, Cuenta)",
                                value="administracion",
                            ),
                            rx.select.item(
                                "Personal de Cocina / Comedor (Menú, Comida)",
                                value="cocina",
                            ),
                        ),
                        value=IncidenciaState.nuevo_destino,
                        on_change=IncidenciaState.set_nuevo_destino,
                        width="100%",
                    ),

                    align_items="start",
                    width="100%",
                ),

                rx.vstack(
                    rx.text("Título del problema", weight="bold", size="2"),
                    rx.input(
                        placeholder="Ej. Problema con mi recarga / Cobro duplicado...",
                        value=IncidenciaState.nuevo_titulo,
                        on_change=IncidenciaState.set_nuevo_titulo,
                        width="100%",
                        radius="large",
                    ),
                    align_items="start",
                    width="100%",
                ),

                rx.vstack(
                    rx.text("Descripción detallada", weight="bold", size="2"),
                    rx.text_area(
                        placeholder="Escribe aquí todos los detalles...",
                        value=IncidenciaState.nueva_descripcion,
                        on_change=IncidenciaState.set_nueva_descripcion,
                        rows="5",
                        width="100%",
                    ),
                    align_items="start",
                    width="100%",
                ),

                spacing="4",
                margin_top="1em",
            ),

            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        on_click=IncidenciaState.cerrar_modal_crear,
                    )
                ),

                rx.button(
                    rx.icon("send", size=16),
                    "Enviar Reporte",
                    color_scheme="blue",
                    on_click=IncidenciaState.crear_incidencia,
                ),

                spacing="3",
                justify="end",
                margin_top="1.5em",
            ),

            max_width="550px",
            border_radius="16px",
        ),

        open=IncidenciaState.modal_crear_abierto,
    )


def vista_estudiante() -> rx.Component:
    """Vista dedicada a Estudiantes y Profesores."""
    return rx.vstack(
        modal_nueva_incidencia(),
        rx.hstack(
            rx.vstack(
                rx.heading("Mis Incidencias", size="8"),
                rx.text(
                    "Consulta el estado de tus reportes o envía un nuevo comunicado al soporte.",
                    color="gray",
                ),
                align_items="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.button(
                rx.icon("plus", size=18),
                "Reportar Incidencia",
                color_scheme="blue",
                radius="large",
                size="3",
                on_click=IncidenciaState.abrir_modal_crear,
            ),
            width="100%",
            align="center",
        ),
        rx.card(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Código Ref."),
                        rx.table.column_header_cell("Fecha"),
                        rx.table.column_header_cell("Título"),
                        rx.table.column_header_cell("Estado"),
                        rx.table.column_header_cell("Respuesta / Solución"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        IncidenciaState.incidencias,
                        lambda inc: rx.table.row(
                            rx.table.cell(rx.code(inc.numero_seguimiento)),
                            rx.table.cell(inc.fecha_reporte),
                            rx.table.cell(
                                rx.vstack(
                                    rx.text(inc.titulo, weight="bold", size="2"),
                                    rx.text(inc.descripcion, size="1", color="gray", max_lines=2),
                                    align_items="start",
                                    spacing="0",
                                )
                            ),
                            rx.table.cell(badge_estado(inc.estado)),
                            rx.table.cell(
                                rx.cond(
                                    inc.respuesta != "",
                                    rx.callout(inc.respuesta, color_scheme="green", size="1"),
                                    rx.text("En espera de atención...", color="gray", size="1", italic=True),
                                )
                            ),
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
    )


def vista_administrador() -> rx.Component:
    """Vista dedicada a Administradores y Personal."""
    return rx.vstack(
        modal_responder_incidencia(),
        rx.vstack(
            rx.heading("Gestión de Incidencias", size="8"),
            rx.text(
                "Atiende, gestiona y resuelve los reportes recibidos de estudiantes y personal.",
                color="gray",
            ),
            align_items="start",
            spacing="1",
            width="100%",
        ),
        rx.grid(
            rx.card(
                rx.hstack(
                    rx.vstack(rx.text("Total Registradas", size="2", color="gray"), rx.heading(f"{IncidenciaState.kpi_total}", size="6")),
                    rx.spacer(),
                    rx.icon("life-buoy", size=28, color=rx.color("blue", 9)),
                ),
                padding="1.25em", border_radius="16px",
            ),
            rx.card(
                rx.hstack(
                    rx.vstack(rx.text("Abiertas / En Proceso", size="2", color="gray"), rx.heading(f"{IncidenciaState.kpi_en_proceso + IncidenciaState.kpi_abiertas}", size="6")),
                    rx.spacer(),
                    rx.icon("circle-alert", size=28, color=rx.color("amber", 9)),
                ),
                padding="1.25em", border_radius="16px",
            ),
            rx.card(
                rx.hstack(
                    rx.vstack(rx.text("Resueltas", size="2", color="gray"), rx.heading(f"{IncidenciaState.kpi_resueltas}", size="6")),
                    rx.spacer(),
                    rx.icon("circle-check", size=28, color=rx.color("green", 9)),
                ),
                padding="1.25em", border_radius="16px",
            ),
            columns=rx.breakpoints(initial="1", sm="3"),
            spacing="4",
            width="100%",
        ),
        rx.card(
            rx.hstack(
                rx.input(
                    placeholder="Buscar por Título, Cód. Seguimiento o Correo...",
                    value=IncidenciaState.search_text,
                    on_change=IncidenciaState.set_search_text,
                    width="340px",
                    radius="large",
                ),
                rx.button(
                    rx.icon("search"),
                    "Buscar",
                    on_click=IncidenciaState.load_incidencias,
                    variant="soft",
                    color_scheme="gray",
                    radius="large",
                ),
                rx.spacer(),
                rx.segmented_control.root(
                    rx.segmented_control.item("Todos", value="todos"),
                    rx.segmented_control.item("En proceso", value="en_proceso"),
                    rx.segmented_control.item("Resuelta", value="resuelta"),
                    value=IncidenciaState.filtro_estado,
                    on_change=IncidenciaState.set_filtro_estado,
                    radius="large",
                ),
                width="100%",
                align="center",
            ),
            width="100%",
            padding="1.25em",
            border_radius="20px",
        ),
        rx.card(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID"),
                        rx.table.column_header_cell("Fecha"),
                        rx.table.column_header_cell("Título / Detalles"),
                        rx.table.column_header_cell("Correo"),
                        rx.table.column_header_cell("Estado"),
                        rx.table.column_header_cell("Acciones"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        IncidenciaState.incidencias,
                        lambda inc: rx.table.row(
                            rx.table.cell(f"#{inc.id_incidencia}"),
                            rx.table.cell(inc.fecha_reporte),
                            rx.table.cell(
                                rx.vstack(
                                    rx.text(inc.titulo, weight="bold", size="2"),
                                    rx.text(f"Ref: {inc.numero_seguimiento}", size="1", color="gray"),
                                    align_items="start",
                                    spacing="0",
                                )
                            ),
                            rx.table.cell(inc.correo_usuario),
                            rx.table.cell(
                                rx.menu.root(
                                    rx.menu.trigger(
                                        rx.button(
                                            badge_estado(inc.estado),
                                            rx.icon("chevron-down", size=14),
                                            variant="ghost",
                                            size="1",
                                        )
                                    ),
                                    rx.menu.content(
                                        rx.menu.item(
                                            "En proceso",
                                            on_click=lambda: IncidenciaState.cambiar_estado_rapido(inc.id_incidencia, "en_proceso"),
                                        ),
                                        rx.menu.item(
                                            "Resuelta",
                                            on_click=lambda: IncidenciaState.cambiar_estado_rapido(inc.id_incidencia, "resuelta"),
                                        ),
                                    ),
                                )
                            ),
                            rx.table.cell(
                                rx.button(
                                    rx.icon("eye", size=14),
                                    "Ver / Responder",
                                    size="1",
                                    variant="soft",
                                    color_scheme="blue",
                                    on_click=lambda: IncidenciaState.abrir_modal_respuesta(inc),
                                )
                            ),
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
    )


def incidencias_page() -> rx.Component:
    """Página de incidencias adaptada automáticamente al rol del usuario."""
    return layout(
        rx.box(
            rx.cond(
                AppState.is_estudiante,
                vista_estudiante(),
                rx.cond(
                    AppState.is_profesor,
                    vista_estudiante(),
                    vista_administrador(),
                )
            ),
            on_mount=IncidenciaState.load_incidencias,
            width="100%",
        )
    )