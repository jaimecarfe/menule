import reflex as rx

from app.components.layout import layout
from app.states.menu_state import MenuState, PlatoSimpleSchema
from app.states.auth_state import AppState


def selector_platos_categoria(titulo: str, id_var_1, set_func_1, id_var_2, set_func_2, id_var_3, set_func_3, tipo_filtro: str) -> rx.Component:
    """Genera 3 selectores independientes para configurar hasta 3 platos por categoría."""
    return rx.vstack(
        rx.text(titulo, weight="bold", size="2"),
        rx.select.root(
            rx.select.trigger(placeholder=f"Opción 1 - {titulo}..."),
            rx.select.content(
                rx.foreach(
                    MenuState.platos_disponibles,
                    lambda p: rx.cond(
                        rx.Var.create(tipo_filtro) == p.tipo,
                        rx.select.item(f"{p.nombre} (Alérgenos: {p.alergenos})", value=p.id_plato.to_string()),
                        rx.fragment()
                    )
                )
            ),
            value=id_var_1,
            on_change=set_func_1,
            width="100%",
        ),
        rx.select.root(
            rx.select.trigger(placeholder=f"Opción 2 - {titulo} (Opcional)..."),
            rx.select.content(
                rx.foreach(
                    MenuState.platos_disponibles,
                    lambda p: rx.cond(
                        rx.Var.create(tipo_filtro) == p.tipo,
                        rx.select.item(f"{p.nombre} (Alérgenos: {p.alergenos})", value=p.id_plato.to_string()),
                        rx.fragment()
                    )
                )
            ),
            value=id_var_2,
            on_change=set_func_2,
            width="100%",
        ),
        rx.select.root(
            rx.select.trigger(placeholder=f"Opción 3 - {titulo} (Opcional)..."),
            rx.select.content(
                rx.foreach(
                    MenuState.platos_disponibles,
                    lambda p: rx.cond(
                        rx.Var.create(tipo_filtro) == p.tipo,
                        rx.select.item(f"{p.nombre} (Alérgenos: {p.alergenos})", value=p.id_plato.to_string()),
                        rx.fragment()
                    )
                )
            ),
            value=id_var_3,
            on_change=set_func_3,
            width="100%",
        ),
        spacing="2",
        width="100%",
    )


def selector_platos_form() -> rx.Component:
    """Componente para seleccionar 3 primeros, 3 segundos y 3 postres."""
    return rx.vstack(
        selector_platos_categoria(
            "Primeros Platos", 
            MenuState.id_primero_1, MenuState.set_id_primero_1,
            MenuState.id_primero_2, MenuState.set_id_primero_2,
            MenuState.id_primero_3, MenuState.set_id_primero_3,
            "primero"
        ),
        selector_platos_categoria(
            "Segundos Platos", 
            MenuState.id_segundo_1, MenuState.set_id_segundo_1,
            MenuState.id_segundo_2, MenuState.set_id_segundo_2,
            MenuState.id_segundo_3, MenuState.set_id_segundo_3,
            "segundo"
        ),
        selector_platos_categoria(
            "Postres", 
            MenuState.id_postre_1, MenuState.set_id_postre_1,
            MenuState.id_postre_2, MenuState.set_id_postre_2,
            MenuState.id_postre_3, MenuState.set_id_postre_3,
            "postre"
        ),
        spacing="4",
        width="100%",
    )


def modal_warning_desactivar_menu() -> rx.Component:
    """Modal de aviso al desactivar un menú activo."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("⚠️ Desactivación de Menú"),
            rx.dialog.description(
                f"Estás a punto de marcar como no disponible el menú de {MenuState.form_tipo} para el {MenuState.form_fecha}."
            ),
            rx.vstack(
                rx.callout(
                    "Al desactivarlo, los usuarios no podrán realizar nuevas reservas para este día.",
                    icon="triangle-alert",
                    color_scheme="amber",
                ),
                rx.text("¿Deseas continuar y guardar los cambios?", size="2"),
                spacing="3",
                padding_y="1em",
            ),
            rx.hstack(
                rx.button(
                    "Cancelar",
                    variant="soft",
                    color_scheme="gray",
                    on_click=lambda: MenuState.set_show_warning_desactivar(False),
                ),
                rx.button(
                    "Sí, Desactivar",
                    color_scheme="red",
                    on_click=MenuState.confirmar_desactivacion_menu,
                ),
                justify="end",
                spacing="3",
                width="100%",
            ),
            max_width="450px",
        ),
        open=MenuState.show_warning_desactivar,
        on_open_change=MenuState.set_show_warning_desactivar,
    )


def modal_nuevo_menu() -> rx.Component:
    """Modal para crear un nuevo menú."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Crear Nuevo Menú Diario"),
            rx.dialog.description("Configura la oferta gastronómica y asigna los platos del día."),
            rx.scroll_area(
                rx.vstack(
                    rx.vstack(
                        rx.text("Fecha", weight="bold", size="2"),
                        rx.input(
                            type_="date",
                            value=MenuState.form_fecha,
                            on_change=MenuState.set_form_fecha,
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Tipo de Menú", weight="bold", size="2"),
                        rx.select.root(
                            rx.select.trigger(placeholder="Seleccionar tipo..."),
                            rx.select.content(
                                rx.select.item("Almuerzo", value="almuerzo"),
                                rx.select.item("Cena", value="cena"),
                            ),
                            value=MenuState.form_tipo,
                            on_change=MenuState.set_form_tipo,
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),

                    selector_platos_form(),

                    rx.vstack(
                        rx.text("Máximo de Reservas Permitidas", weight="bold", size="2"),
                        rx.input(
                            type_="number",
                            value=MenuState.form_max_reservas.to_string(),
                            on_change=MenuState.set_form_max_reservas,
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.text("Disponible para Reserva", weight="bold", size="2"),
                        rx.switch(
                            checked=MenuState.form_disponible,
                            on_change=MenuState.set_form_disponible,
                        ),
                        align="center",
                        justify="between",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                    padding_y="1em",
                ),
                max_height="65vh",
            ),
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        on_click=lambda: MenuState.set_show_modal_nuevo_menu(False),
                    )
                ),
                rx.button(
                    "Guardar Menú",
                    color_scheme="violet",
                    on_click=MenuState.crear_menu,
                ),
                justify="end",
                spacing="3",
                width="100%",
                margin_top="1em",
            ),
            max_width="520px",
        ),
        open=MenuState.show_modal_nuevo_menu,
        on_open_change=MenuState.set_show_modal_nuevo_menu,
    )


def modal_editar_menu() -> rx.Component:
    """Modal para editar un menú existente."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Modificar Menú y Alérgenos"),
            rx.dialog.description("Actualiza platos, alérgenos asignados o el aforo del menú."),
            rx.scroll_area(
                rx.vstack(
                    rx.vstack(
                        rx.text("Fecha", weight="bold", size="2"),
                        rx.input(
                            type_="date",
                            value=MenuState.form_fecha,
                            on_change=MenuState.set_form_fecha,
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Tipo de Menú", weight="bold", size="2"),
                        rx.select.root(
                            rx.select.trigger(placeholder="Seleccionar tipo..."),
                            rx.select.content(
                                rx.select.item("Almuerzo", value="almuerzo"),
                                rx.select.item("Cena", value="cena"),
                            ),
                            value=MenuState.form_tipo,
                            on_change=MenuState.set_form_tipo,
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),

                    selector_platos_form(),

                    rx.vstack(
                        rx.text("Máximo de Reservas", weight="bold", size="2"),
                        rx.input(
                            type_="number",
                            value=MenuState.form_max_reservas.to_string(),
                            on_change=MenuState.set_form_max_reservas,
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.text("Disponible", weight="bold", size="2"),
                        rx.switch(
                            checked=MenuState.form_disponible,
                            on_change=MenuState.set_form_disponible,
                        ),
                        align="center",
                        justify="between",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                    padding_y="1em",
                ),
                max_height="65vh",
            ),
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        on_click=lambda: MenuState.set_show_modal_editar_menu(False),
                    )
                ),
                rx.button(
                    "Guardar Cambios",
                    color_scheme="violet",
                    on_click=MenuState.intentar_guardar_edicion,
                ),
                justify="end",
                spacing="3",
                width="100%",
                margin_top="1em",
            ),
            max_width="520px",
        ),
        open=MenuState.show_modal_editar_menu,
        on_open_change=MenuState.set_show_modal_editar_menu,
    )


def comedor_menus_view() -> rx.Component:
    """Vista Operativa para Personal de Comedor."""
    return rx.vstack(
        rx.vstack(
            rx.heading("Panel de Personal de Comedor", size="8"),
            rx.text(
                "Gestión operativa diaria: edición de menú, control de alérgenos y seguimiento de comandas.",
                color="gray",
            ),
            align_items="start",
            spacing="1",
            width="100%",
        ),

        # TARJETAS DE ACCESO RÁPIDO
        rx.grid(
            rx.card(
                rx.hstack(
                    rx.icon("utensils-crossed", size=32, color="#7C3AED"),
                    rx.vstack(
                        rx.text("Publicar / Editar Menú", weight="bold"),
                        rx.text("Configurar menú del día y alérgenos", size="1", color="gray"),
                        align_items="start",
                    ),
                    align="center",
                ),
                on_click=MenuState.abrir_modal_nuevo_menu,
                cursor="pointer",
                padding="1.2em",
            ),
            rx.card(
                rx.hstack(
                    rx.icon("chef-hat", size=32, color="#2563EB"),
                    rx.vstack(
                        rx.text("Procesar Pedidos", weight="bold"),
                        rx.hstack(
                            rx.text("Reservas de hoy: ", size="1", color="gray"),
                            rx.badge(MenuState.total_reservas_hoy, color_scheme="blue", radius="full"),
                            spacing="1",
                            align="center",
                        ),
                        align_items="start",
                    ),
                    align="center",
                ),
                on_click=rx.redirect("/pedidos"),
                cursor="pointer",
                padding="1.2em",
            ),
            rx.card(
                rx.hstack(
                    rx.icon("boxes", size=32, color="#059669"),
                    rx.vstack(
                        rx.text("Consultar Stock", weight="bold"),
                        rx.text("Inventario de ingredientes y cocina", size="1", color="gray"),
                        align_items="start",
                    ),
                    align="center",
                ),
                on_click=rx.redirect("/stock"),
                cursor="pointer",
                padding="1.2em",
            ),
            columns="3",
            spacing="4",
            width="100%",
        ),

        # TABLA DE MENÚS DIARIOS
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.heading("Menús Disponibles y Programados", size="4"),
                    rx.spacer(),
                    rx.input(
                        placeholder="Buscar por fecha...",
                        value=MenuState.search_text,
                        on_change=MenuState.set_search_text,
                        width="240px",
                    ),
                    rx.button(
                        rx.icon("search", size=16),
                        "Buscar",
                        on_click=MenuState.load_menus,
                        variant="soft",
                        color_scheme="gray",
                    ),
                    width="100%",
                    align="center",
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Fecha"),
                            rx.table.column_header_cell("Tipo"),
                            rx.table.column_header_cell("Aforo Máx."),
                            rx.table.column_header_cell("Estado"),
                            rx.table.column_header_cell("Platos"),
                            rx.table.column_header_cell("Acciones"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            MenuState.menus,
                            lambda menu: rx.table.row(
                                rx.table.cell(menu.fecha),
                                rx.table.cell(rx.badge(menu.tipo.capitalize(), color_scheme="violet", variant="soft")),
                                rx.table.cell(menu.max_reservas),
                                rx.table.cell(
                                    rx.badge(
                                        rx.cond(menu.disponible, "Disponible", "No disponible"),
                                        color_scheme=rx.cond(menu.disponible, "green", "red"),
                                        variant="soft",
                                    )
                                ),
                                rx.table.cell(rx.badge(menu.num_platos, color_scheme="blue", variant="soft")),
                                rx.table.cell(
                                    rx.hstack(
                                        rx.button(
                                            rx.icon("square-pen", size=16),
                                            "Modificar",
                                            variant="soft",
                                            color_scheme="violet",
                                            size="2",
                                            on_click=lambda: MenuState.abrir_modal_editar_menu(menu),
                                        ),
                                        spacing="2",
                                    )
                                ),
                            ),
                        ),
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

        modal_nuevo_menu(),
        modal_editar_menu(),
        modal_warning_desactivar_menu(),

        spacing="5",
        width="100%",
        on_mount=[MenuState.load_menus, MenuState.load_resumen_comedor],
    )


def admin_menus_view() -> rx.Component:
    """Vista de Administración Global de Menús (Admin)."""
    return rx.vstack(
        rx.vstack(
            rx.heading("Gestión General de Menús (Admin)", size="8"),
            rx.text(
                "Administración completa de la oferta gastronómica y borrado de registros.",
                color="gray",
            ),
            align_items="start",
            spacing="1",
            width="100%",
        ),

        rx.card(
            rx.hstack(
                rx.input(
                    placeholder="Buscar menú...",
                    value=MenuState.search_text,
                    on_change=MenuState.set_search_text,
                    width="340px",
                    radius="large",
                    size="3",
                ),
                rx.button(
                    rx.icon("search"),
                    "Buscar",
                    on_click=MenuState.load_menus,
                    variant="soft",
                    color_scheme="gray",
                    radius="large",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("utensils-crossed"),
                    "Nuevo menú",
                    on_click=MenuState.abrir_modal_nuevo_menu,
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

        rx.card(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID"),
                        rx.table.column_header_cell("Fecha"),
                        rx.table.column_header_cell("Tipo"),
                        rx.table.column_header_cell("Máx. reservas"),
                        rx.table.column_header_cell("Estado"),
                        rx.table.column_header_cell("Platos"),
                        rx.table.column_header_cell("Acciones"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        MenuState.menus,
                        lambda menu: rx.table.row(
                            rx.table.cell(menu.id_menu),
                            rx.table.cell(menu.fecha),
                            rx.table.cell(
                                rx.badge(
                                    menu.tipo.capitalize(),
                                    color_scheme="violet",
                                    variant="soft",
                                )
                            ),
                            rx.table.cell(menu.max_reservas),
                            rx.table.cell(
                                rx.badge(
                                    rx.cond(
                                        menu.disponible,
                                        "Disponible",
                                        "No disponible",
                                    ),
                                    color_scheme=rx.cond(
                                        menu.disponible,
                                        "green",
                                        "red",
                                    ),
                                    variant="soft",
                                )
                            ),
                            rx.table.cell(
                                rx.badge(
                                    menu.num_platos,
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
                                        on_click=lambda: MenuState.abrir_modal_editar_menu(menu),
                                    ),
                                    rx.button(
                                        rx.icon("trash-2"),
                                        variant="soft",
                                        color_scheme="red",
                                        radius="large",
                                        size="2",
                                        on_click=lambda: MenuState.eliminar_menu(menu.id_menu),
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

        modal_nuevo_menu(),
        modal_editar_menu(),
        modal_warning_desactivar_menu(),

        spacing="5",
        width="100%",
        on_mount=MenuState.load_menus,
    )


def option_card(plato: PlatoSimpleSchema, selected_var: rx.Var, set_func, es_visitante: rx.Var = rx.Var.create(False)) -> rx.Component:
    """Tarjeta de plato. Si es visitante la muestra en modo lectura elegante sin interactividad de click."""
    is_selected = selected_var == plato.nombre

    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.text(plato.nombre, weight="bold", size="3", color="#111827"),
                rx.hstack(
                    rx.icon("info", size=14, color="#6B7280"),
                    rx.text(f"Alérgenos: {plato.alergenos}", size="1", color="#6B7280"),
                    spacing="1",
                    align="center",
                ),
                spacing="1",
                align_items="start",
            ),
            rx.spacer(),
            rx.cond(
                ~es_visitante,
                rx.cond(
                    is_selected,
                    rx.icon("circle-check", color="#7C3AED", size=24),
                    rx.icon("circle", color="#D1D5DB", size=24),
                ),
                rx.badge("Oferta del día", color_scheme="purple", variant="soft", radius="full")
            ),
            align="center",
            width="100%",
        ),
        on_click=rx.cond(~es_visitante, set_func(plato.nombre), rx.console_log("Modo lectura")),
        width="100%",
        padding="1em",
        cursor=rx.cond(~es_visitante, "pointer", "default"),
        style={
            "borderRadius": "14px",
            "border": rx.cond(is_selected & ~es_visitante, "2px solid #7C3AED", "1px solid #EEF2F7"),
            "backgroundColor": rx.cond(is_selected & ~es_visitante, "#F3E8FF", "#FFFFFF"),
            "transition": "all 0.15s ease-in-out",
        },
    )


def section_platos(title: str, icon: str, lista_platos: rx.Var, selected_var: rx.Var, set_func, es_visitante: rx.Var = rx.Var.create(False)) -> rx.Component:
    """Sección de lista de platos por categoría."""
    return rx.vstack(
        rx.hstack(
            rx.center(
                rx.icon(icon, size=20, color="#7C3AED"),
                background="#F3E8FF",
                border_radius="10px",
                padding="6px",
            ),
            rx.heading(title, size="4", weight="bold", color="#111827"),
            spacing="2",
            align="center",
        ),
        rx.vstack(
            rx.foreach(
                lista_platos,
                lambda p: option_card(p, selected_var, set_func, es_visitante)
            ),
            width="100%",
            spacing="2",
        ),
        spacing="3",
        width="100%",
    )


def user_menu_view() -> rx.Component:
    """Vista pública para consultar el menú del día y reservar (Estudiantes, Profesores y Visitantes)."""
    es_visitante = AppState.is_visitante

    precio_texto = rx.cond(
        AppState.is_estudiante,
        "5,50 €",
        rx.cond(AppState.is_profesor, "6,50 €", "7,50 €")
    )

    return rx.vstack(
        # HEADER SUPERIOR
        rx.card(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.badge(
                            rx.cond(es_visitante, "Menú Público / Visitante", "Menú del Día"),
                            color_scheme="purple",
                            variant="surface",
                            radius="full"
                        ),
                        rx.badge(precio_texto, color_scheme="green", variant="surface", radius="full"),
                        spacing="2",
                    ),
                    rx.heading(
                        rx.cond(es_visitante, "Oferta Gastronómica de Hoy", "Elige tu Menú de Hoy"),
                        size="6",
                        weight="bold",
                        color="#111827"
                    ),
                    rx.text(
                        rx.cond(
                            es_visitante,
                            "Consulta los platos y alérgenos disponibles en el Comedor Universitario.",
                            "Selecciona tus platos preferidos y confirma tu reserva instantánea descontando de tu saldo TUI."
                        ),
                        color="#4B5563",
                        size="3"
                    ),
                    spacing="2",
                    align_items="start",
                ),
                rx.spacer(),
                # Muestra saldo TUI sólo a usuarios autenticados
                rx.cond(
                    ~es_visitante,
                    rx.vstack(
                        rx.text("Tu Saldo TUI", size="1", color="#6B7280", weight="medium"),
                        rx.heading(AppState.user_saldo_str, size="5", color="#7C3AED", weight="bold"),
                        align_items="end",
                        spacing="0",
                    ),
                ),
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

        # PLATOS DEL DÍA
        rx.cond(
            MenuState.has_menu_hoy,
            rx.vstack(
                rx.grid(
                    section_platos("Primer Plato", "soup", MenuState.platos_primeros, MenuState.plato_1_sel, MenuState.set_plato_1_sel, es_visitante),
                    section_platos("Segundo Plato", "utensils", MenuState.platos_segundos, MenuState.plato_2_sel, MenuState.set_plato_2_sel, es_visitante),
                    section_platos("Postre", "apple", MenuState.platos_postres, MenuState.postre_sel, MenuState.set_postre_sel, es_visitante),
                    columns="3",
                    spacing="4",
                    width="100%",
                ),
                rx.divider(margin_y="1em"),
                
                # BOTÓN DE ACCIÓN SEGÚN EL ROL
                rx.hstack(
                    rx.spacer(),
                    rx.cond(
                        es_visitante,
                        # Botón destacado para Visitantes -> Redirige a la reserva
                        rx.button(
                            rx.text("Ir a Reservar Menú (7,50 €)", weight="bold"),
                            rx.icon("arrow-right", size=20),
                            size="4",
                            color_scheme="purple",
                            radius="large",
                            cursor="pointer",
                            on_click=rx.redirect("/visitante/reserva"),
                        ),
                        # Botón para Estudiantes / Profesores
                        rx.button(
                            rx.icon("ticket", size=20),
                            rx.text(f"Confirmar Reserva ({precio_texto})", weight="bold"),
                            size="4",
                            color_scheme="purple",
                            radius="large",
                            cursor="pointer",
                            on_click=MenuState.realizar_reserva,
                        ),
                    ),
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            rx.card(
                rx.vstack(
                    rx.icon("utensils-crossed", size=48, color="#9CA3AF"),
                    rx.heading("No hay menú publicado para hoy", size="4", color="#374151"),
                    rx.text("El equipo de cocina aún no ha habilitado la oferta gastronómica del día.", color="#6B7280", size="2"),
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
        on_mount=MenuState.load_menu_del_dia,
    )


def menus_page() -> rx.Component:
    """Distribuye dinámicamente la vista según el rol exacto del usuario."""
    return layout(
        rx.match(
            AppState.user_role,
            ("administrador", admin_menus_view()),
            ("personal_comedor", comedor_menus_view()),
            user_menu_view(),
        )
    )