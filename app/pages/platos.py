import reflex as rx

from app.components.layout import layout
from app.states.plato_state import PlatoState, LISTA_ALERGENOS


def alergeno_checkbox_item(nombre: str) -> rx.Component:
    """Componente individual para cada alérgeno."""
    return rx.hstack(
        rx.checkbox(
            checked=PlatoState.form_alergenos_selected[nombre],
            on_change=lambda val: PlatoState.toggle_alergeno(nombre, val),
        ),
        rx.text(nombre, size="2"),
        align="center",
        spacing="2",
    )


def modal_warning_desactivacion() -> rx.Component:
    """Modal de advertencia si el plato pertenece a menús."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("⚠️ Plato asignado a menús activos"),
            rx.dialog.description(
                f"El plato '{PlatoState.form_nombre}' se encuentra actualmente asignado a {PlatoState.affected_menus_count} menú(s)."
            ),
            rx.vstack(
                rx.callout(
                    "Si deshabilitas este plato, los menús mantendrán la referencia pero se generará un aviso en la campana de notificaciones para sustituirlo.",
                    icon="triangle_alert",
                    color_scheme="amber",
                ),
                rx.text("¿Deseas desactivarlo de todas formas?", size="2"),
                spacing="3",
                padding_y="1em",
            ),
            rx.hstack(
                rx.button(
                    "Cancelar",
                    variant="soft",
                    color_scheme="gray",
                    on_click=lambda: PlatoState.set_show_warning_modal(False),
                ),
                rx.button(
                    "Confirmar Desactivación",
                    color_scheme="red",
                    on_click=PlatoState.confirmar_desactivacion,
                ),
                justify="end",
                spacing="3",
                width="100%",
            ),
            max_width="480px",
        ),
        open=PlatoState.show_warning_modal,
        on_open_change=PlatoState.set_show_warning_modal,
    )


def modal_plato() -> rx.Component:
    """Modal principal para crear y editar platos."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    PlatoState.editando == 0,
                    "Crear Nuevo Plato",
                    "Editar Plato",
                )
            ),
            rx.dialog.description("Define el nombre, categoría, disponibilidad y los alérgenos presentes."),
            
            rx.vstack(
                # Nombre
                rx.vstack(
                    rx.text("Nombre del Plato", weight="bold", size="2"),
                    rx.input(
                        placeholder="Ej: Sopa de Picadillo / Pechuga a la plancha",
                        value=PlatoState.form_nombre,
                        on_change=PlatoState.set_form_nombre,
                        width="100%",
                        radius="large",
                    ),
                    spacing="1",
                    width="100%",
                ),

                # Tipo
                rx.vstack(
                    rx.text("Categoría / Tipo", weight="bold", size="2"),
                    rx.select(
                        ["primero", "segundo", "postre"],
                        value=PlatoState.form_tipo,
                        on_change=PlatoState.set_form_tipo,
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                # Alérgenos
                rx.vstack(
                    rx.text("Declaración de Alérgenos", weight="bold", size="2"),
                    rx.vstack(
                        rx.grid(
                            rx.foreach(
                                LISTA_ALERGENOS,
                                alergeno_checkbox_item,
                            ),
                            columns="2",
                            spacing="3",
                            width="100%",
                        ),
                        rx.divider(),
                        
                        # Opción Otros
                        rx.vstack(
                            rx.hstack(
                                rx.checkbox(
                                    checked=PlatoState.form_otros_active,
                                    on_change=PlatoState.set_form_otros_active,
                                ),
                                rx.text("Otros (especificar alérgeno)", size="2", weight="medium"),
                                align="center",
                                spacing="2",
                            ),
                            rx.cond(
                                PlatoState.form_otros_active,
                                rx.input(
                                    placeholder="Ej: Trigo sarraceno, Canela, Marisco específico...",
                                    value=PlatoState.form_otros_texto,
                                    on_change=PlatoState.set_form_otros_texto,
                                    width="100%",
                                    radius="large",
                                    size="2",
                                ),
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                        padding="1em",
                        border="1px solid var(--gray-5)",
                        border_radius="12px",
                        bg="var(--gray-2)",
                    ),
                    spacing="1",
                    width="100%",
                ),

                # Activo / Switch
                rx.hstack(
                    rx.text("Disponible en Carta", weight="bold", size="2"),
                    rx.switch(
                        checked=PlatoState.form_activo,
                        on_change=PlatoState.set_form_activo,
                    ),
                    align="center",
                    justify="between",
                    width="100%",
                ),

                spacing="4",
                width="100%",
                padding_y="1em",
            ),

            # Acciones
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        on_click=lambda: PlatoState.set_show_modal(False),
                    )
                ),
                rx.button(
                    "Guardar Plato",
                    color_scheme="violet",
                    on_click=PlatoState.intentar_guardar,
                ),
                justify="end",
                spacing="3",
                width="100%",
            ),
            max_width="520px",
        ),
        open=PlatoState.show_modal,
        on_open_change=PlatoState.set_show_modal,
    )


def platos_page() -> rx.Component:
    return layout(
        rx.vstack(
            # Cabecera
            rx.vstack(
                rx.heading("Gestión de Platos", size="8"),
                rx.text(
                    "Catálogo general de platos y control de alérgenos para comedores.",
                    color="gray",
                ),
                align_items="start",
                spacing="1",
                width="100%",
            ),

            # Buscador y Añadir
            rx.card(
                rx.hstack(
                    rx.input(
                        placeholder="Buscar plato o alérgeno...",
                        value=PlatoState.search_text,
                        on_change=PlatoState.set_search_text,
                        width="340px",
                        radius="large",
                        size="3",
                    ),
                    rx.button(
                        rx.icon("search"),
                        "Buscar",
                        on_click=PlatoState.load_platos,
                        variant="soft",
                        color_scheme="gray",
                        radius="large",
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon("plus"),
                        "Nuevo plato",
                        on_click=PlatoState.nuevo_plato,
                        color_scheme="violet",
                        radius="large",
                        cursor="pointer",
                    ),
                    width="100%",
                    align="center",
                ),
                width="100%",
                padding="1.25em",
                border_radius="20px",
            ),

            # Tabla
            rx.card(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("ID"),
                            rx.table.column_header_cell("Nombre"),
                            rx.table.column_header_cell("Tipo"),
                            rx.table.column_header_cell("Alérgenos"),
                            rx.table.column_header_cell("Estado"),
                            rx.table.column_header_cell("Menús"),
                            rx.table.column_header_cell("Acciones"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            PlatoState.platos,
                            lambda plato: rx.table.row(
                                rx.table.cell(plato.id_plato),
                                rx.table.cell(
                                    rx.text(plato.nombre, weight="medium")
                                ),
                                rx.table.cell(
                                    rx.badge(
                                        plato.tipo.capitalize(),
                                        color_scheme="violet",
                                        variant="soft",
                                    )
                                ),
                                rx.table.cell(
                                    rx.text(
                                        plato.alergenos,
                                        size="2",
                                        color=rx.cond(
                                            plato.alergenos == "Ninguno",
                                            "gray",
                                            "red",
                                        ),
                                    )
                                ),
                                rx.table.cell(
                                    rx.badge(
                                        rx.cond(
                                            plato.activo,
                                            "Activo",
                                            "Inactivo",
                                        ),
                                        color_scheme=rx.cond(
                                            plato.activo,
                                            "green",
                                            "red",
                                        ),
                                        variant="soft",
                                    )
                                ),
                                rx.table.cell(
                                    rx.badge(
                                        plato.num_menus,
                                        color_scheme="blue",
                                        variant="soft",
                                    )
                                ),
                                rx.table.cell(
                                    rx.hstack(
                                        rx.button(
                                            rx.icon("square-pen"),
                                            variant="soft",
                                            color_scheme="gray",
                                            radius="large",
                                            size="2",
                                            on_click=lambda: PlatoState.editar_plato(plato.id_plato),
                                        ),
                                        rx.button(
                                            rx.icon("trash-2"),
                                            variant="soft",
                                            color_scheme="red",
                                            radius="large",
                                            size="2",
                                            on_click=lambda: PlatoState.eliminar(plato.id_plato),
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

            # Modales
            modal_plato(),
            modal_warning_desactivacion(),

            spacing="5",
            width="100%",
            on_mount=PlatoState.load_platos,
        )
    )