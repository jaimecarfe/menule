import reflex as rx

from app.components.layout import layout
from app.states.stock_state import IngredienteSchema, StockState


def metric_card(title: str, value: rx.Var, icon: str, color: str) -> rx.Component:
    """Tarjeta para mostrar estadísticas rápidas de inventario."""
    return rx.card(
        rx.hstack(
            rx.icon(tag=icon, size=28, color=color),
            rx.vstack(
                rx.text(title, size="2", color="gray"),
                rx.heading(value, size="6"),
                align_items="start",
                spacing="1",
            ),
            align="center",
            spacing="3",
        ),
        padding="1.2em",
        border_radius="16px",
    )


def fila_ingrediente(ing: IngredienteSchema) -> rx.Component:
    """Fila para cada ingrediente en la tabla de stock."""
    return rx.table.row(
        rx.table.cell(rx.text(f"#{ing.id_ingrediente}", weight="bold")),
        rx.table.cell(rx.text(ing.nombre, weight="medium")),
        rx.table.cell(
            rx.hstack(
                rx.text(f"{ing.stock_actual} {ing.unidad_medida}"),
                rx.cond(
                    ing.es_critico,
                    rx.badge("Stock Bajo", color_scheme="red", variant="solid"),
                    rx.badge("OK", color_scheme="green", variant="soft"),
                ),
                align="center",
                spacing="2",
            )
        ),
        rx.table.cell(rx.text(f"{ing.stock_minimo} {ing.unidad_medida}")),
        rx.table.cell(
            rx.cond(
                ing.alergeno,
                rx.badge(ing.tipo_alergeno, color_scheme="amber"),
                rx.text("Sin alérgenos", color="gray", size="2"),
            )
        ),
        rx.table.cell(
            rx.button(
                "Pedir Stock",
                icon="plus",
                size="1",
                color_scheme="violet",
                radius="large",
                on_click=lambda: StockState.abrir_modal_reabastecer(ing),
            )
        ),
    )


def desglose_menu_hoy() -> rx.Component:
    """Muestra el menú activo de hoy y los requerimientos calculados para 150 aforos basados en tu catálogo."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon("utensils-crossed", size=22, color="#7C3AED"),
                rx.heading("Menú Activo de Hoy (Almuerzo - 150 Reservas máx.)", size="4"),
                rx.spacer(),
                rx.badge("Servicio Confirmado", color_scheme="green", radius="full"),
                width="100%",
                align="center",
            ),
            rx.text(
                "Platos seleccionados para el servicio de hoy y estimación de materia prima necesaria:",
                size="2",
                color="gray",
            ),
            rx.grid(
                rx.vstack(
                    rx.text("🥣 Primeros Platos", weight="bold", size="2", color="#7C3AED"),
                    rx.badge("• Crema de Verduras", variant="soft", color_scheme="gray"),
                    rx.badge("• Macarrones Bolonesa", variant="soft", color_scheme="gray"),
                    rx.badge("• Frango à brás", variant="soft", color_scheme="gray"),
                    align_items="start",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("🥩 Segundos Platos", weight="bold", size="2", color="#7C3AED"),
                    rx.badge("• Hamburguesa Completa", variant="soft", color_scheme="gray"),
                    rx.badge("• Estofado de Ternera", variant="soft", color_scheme="gray"),
                    rx.badge("• Lomo Adobado", variant="soft", color_scheme="gray"),
                    align_items="start",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("🍰 Postres", weight="bold", size="2", color="#7C3AED"),
                    rx.badge("• Yogur Natural", variant="soft", color_scheme="gray"),
                    rx.badge("• Tarta de Queso", variant="soft", color_scheme="gray"),
                    rx.badge("• Helado de Vainilla", variant="soft", color_scheme="gray"),
                    align_items="start",
                    spacing="1",
                ),
                columns="3",
                spacing="4",
                width="100%",
                padding_y="0.5em",
            ),
            rx.divider(margin_y="2"),
            rx.text("📦 Materia Prima Sugerida para el Servicio Activo (150 Pax):", weight="bold", size="2"),
            rx.grid(
                rx.box(
                    rx.text("Verduras Variadas (Crema)", size="1", color="gray"),
                    rx.text("25 Kg requeridos", size="2", weight="bold", color="#059669"),
                    padding="0.6em", background="#F0FDF4", border_radius="10px", border="1px solid #BBF7D0"
                ),
                rx.box(
                    rx.text("Carne Picada / Ternera (Bolonesa/Hamburguesa)", size="1", color="gray"),
                    rx.text("35 Kg requeridos", size="2", weight="bold", color="#059669"),
                    padding="0.6em", background="#F0FDF4", border_radius="10px", border="1px solid #BBF7D0"
                ),
                rx.box(
                    rx.text("Pollo Deshilachado / Frango & Huevos", size="1", color="gray"),
                    rx.text("20 Kg + 150 Ud. Huevos", size="2", weight="bold", color="#059669"),
                    padding="0.6em", background="#F0FDF4", border_radius="10px", border="1px solid #BBF7D0"
                ),
                rx.box(
                    rx.text("Lomo Adobado de Cerdo", size="1", color="gray"),
                    rx.text("18 Kg requeridos", size="2", weight="bold", color="#059669"),
                    padding="0.6em", background="#F0FDF4", border_radius="10px", border="1px solid #BBF7D0"
                ),
                rx.box(
                    rx.text("Queso Cremoso (Tarta)", size="1", color="gray"),
                    rx.text("8 Kg requeridos", size="2", weight="bold", color="#059669"),
                    padding="0.6em", background="#F0FDF4", border_radius="10px", border="1px solid #BBF7D0"
                ),
                columns="3",
                spacing="3",
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
        padding="1.2em",
        border_radius="20px",
        style={"background": "linear-gradient(135deg, #FFFFFF 0%, #FAF5FF 100%)"},
    )


def stock_view() -> rx.Component:
    """Contenido principal de la vista de Inventario y Stock."""
    return rx.vstack(
        # Encabezado
        rx.vstack(
            rx.heading("Gestión e Inventario de Stock", size="8"),
            rx.text(
                "Control de materia prima, previsión del servicio diario y reabastecimiento.",
                color="gray",
            ),
            align_items="start",
            spacing="1",
            width="100%",
        ),

        # Resumen Estadístico
        rx.grid(
            metric_card(
                "Total Ingredientes",
                StockState.total_ingredientes,
                "package",
                "#7C3AED",
            ),
            metric_card(
                "Ingredientes Críticos",
                StockState.stock_critico_count,
                "triangle-alert",
                "#DC2626",
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),

        # Menú del día
        desglose_menu_hoy(),

        # Contenedor de la Tabla
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.input(
                        placeholder="Buscar ingrediente...",
                        value=StockState.search_text,
                        on_change=StockState.set_search_text,
                        width="280px",
                    ),
                    rx.button(
                        rx.cond(
                            StockState.filtro_critico,
                            "Mostrar Todos",
                            "Ver Solo Críticos",
                        ),
                        color_scheme=rx.cond(
                            StockState.filtro_critico, "gray", "red"
                        ),
                        variant="soft",
                        on_click=StockState.toggle_filtro_critico,
                    ),
                    rx.spacer(),
                    # Botón para abrir modal de nuevo ingrediente
                    rx.button(
                        rx.icon("circle-plus", size=16),
                        "Añadir Ingrediente",
                        color_scheme="violet",
                        radius="large",
                        on_click=StockState.abrir_modal_nuevo,
                    ),
                    rx.button(
                        rx.icon("refresh-cw", size=16),
                        "Actualizar",
                        variant="soft",
                        color_scheme="gray",
                        on_click=StockState.cargar_stock,
                    ),
                    width="100%",
                    align="center",
                ),

                # Tabla Principal
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("ID"),
                            rx.table.column_header_cell("Ingrediente"),
                            rx.table.column_header_cell("Stock Actual"),
                            rx.table.column_header_cell("Stock Mínimo"),
                            rx.table.column_header_cell("Alérgenos"),
                            rx.table.column_header_cell("Acciones"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(StockState.ingredientes, fila_ingrediente)
                    ),
                    variant="surface",
                    size="2",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            width="100%",
            padding="1.5em",
            border_radius="20px",
        ),

        # Modal Reabastecer
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Reabastecer Stock"),
                rx.dialog.description("Introduce la cantidad a ingresar al almacén:"),
                rx.vstack(
                    rx.input(
                        type="number",
                        value=StockState.cantidad_a_pedir.to_string(),
                        on_change=StockState.set_cantidad_a_pedir,
                        width="100%",
                    ),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button("Cancelar", variant="soft", color_scheme="gray")
                        ),
                        rx.button(
                            "Confirmar Pedido",
                            color_scheme="violet",
                            on_click=StockState.confirmar_pedido_stock,
                        ),
                        justify="end",
                        spacing="3",
                        width="100%",
                    ),
                    spacing="4",
                    margin_top="1em",
                ),
                max_width="450px",
            ),
            open=StockState.show_modal_pedido,
            on_open_change=StockState.set_show_modal_pedido,
        ),

        # MODAL MEJORADO: Añadir Nuevo Ingrediente con etiquetas y distribución limpia
        rx.dialog.root(
            rx.dialog.content(
                rx.vstack(
                    rx.hstack(
                        rx.icon("package-plus", size=22, color="#7C3AED"),
                        rx.dialog.title("Añadir Nuevo Ingrediente"),
                        align="center",
                        spacing="2",
                    ),
                    rx.dialog.description(
                        "Registra una nueva materia prima en la base de datos de la cocina."
                    ),
                    rx.vstack(
                        rx.vstack(
                            rx.text("Nombre del Ingrediente", size="2", weight="medium"),
                            rx.input(
                                placeholder="Ej. Arroz Basmati / Pechuga de Pollo",
                                value=StockState.nuevo_nombre,
                                on_change=StockState.set_nuevo_nombre,
                                width="100%",
                            ),
                            align_items="start",
                            width="100%",
                            spacing="1",
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text("Stock Inicial", size="2", weight="medium"),
                                rx.input(
                                    placeholder="20",
                                    type="number",
                                    value=StockState.nuevo_stock_actual.to_string(),
                                    on_change=StockState.set_nuevo_stock_actual,
                                    width="100%",
                                ),
                                align_items="start",
                                width="50%",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Unidad de Medida", size="2", weight="medium"),
                                rx.select(
                                    ["Kg", "Litros", "Gramos", "Unidades", "Barras"],
                                    value=StockState.nueva_unidad,
                                    on_change=StockState.set_nueva_unidad,
                                    width="100%",
                                ),
                                align_items="start",
                                width="50%",
                                spacing="1",
                            ),
                            width="100%",
                            spacing="3",
                        ),
                        rx.vstack(
                            rx.text("Stock Mínimo de Alerta", size="2", weight="medium"),
                            rx.input(
                                placeholder="10",
                                type="number",
                                value=StockState.nuevo_stock_minimo.to_string(),
                                on_change=StockState.set_nuevo_stock_minimo,
                                width="100%",
                            ),
                            align_items="start",
                            width="100%",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Alérgeno Principal (opcional)", size="2", weight="medium"),
                            rx.select(
                                ["Ninguno", "Gluten", "Lácteos", "Frango", "Huevo", "Pescado", "Frutos Secos"],
                                value=StockState.nuevo_tipo_alergeno,
                                on_change=StockState.set_nuevo_tipo_alergeno,
                                width="100%",
                            ),
                            align_items="start",
                            width="100%",
                            spacing="1",
                        ),
                        spacing="3",
                        width="100%",
                        margin_top="0.5em",
                    ),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button("Cancelar", variant="soft", color_scheme="gray")
                        ),
                        rx.button(
                            "Guardar Ingrediente",
                            color_scheme="violet",
                            on_click=StockState.crear_nuevo_ingrediente,
                        ),
                        justify="end",
                        spacing="3",
                        width="100%",
                        margin_top="1em",
                    ),
                    spacing="3",
                    width="100%",
                ),
                max_width="500px",
            ),
            open=StockState.show_modal_nuevo_ingrediente,
            on_open_change=StockState.set_show_modal_nuevo_ingrediente,
        ),

        spacing="5",
        width="100%",
        on_mount=StockState.cargar_stock,
    )


def stock_page() -> rx.Component:
    """Envuelve la vista dentro del layout de MenULE."""
    return layout(stock_view())