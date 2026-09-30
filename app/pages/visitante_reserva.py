import reflex as rx
from app.states.visitante_state import VisitanteState
from app.states.menu_state import PlatoSimpleSchema
from app.components.layout import layout


def option_card_visitante(plato: PlatoSimpleSchema, selected_var: rx.Var, set_func) -> rx.Component:
    """Tarjeta interactiva para seleccionar un plato (Acceso Visitante)."""
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
                is_selected,
                rx.icon("circle-check", color="#7C3AED", size=24),
                rx.icon("circle", color="#D1D5DB", size=24),
            ),
            align="center",
            width="100%",
        ),
        on_click=set_func(plato.nombre),
        width="100%",
        padding="1em",
        cursor="pointer",
        style={
            "borderRadius": "14px",
            "border": rx.cond(is_selected, "2px solid #7C3AED", "1px solid #EEF2F7"),
            "backgroundColor": rx.cond(is_selected, "#F3E8FF", "#FFFFFF"),
            "transition": "all 0.15s ease-in-out",
        },
    )


def section_platos_visitante(title: str, icon: str, lista_platos: rx.Var, selected_var: rx.Var, set_func) -> rx.Component:
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
                lambda p: option_card_visitante(p, selected_var, set_func)
            ),
            width="100%",
            spacing="2",
        ),
        spacing="3",
        width="100%",
    )


def modal_correo_visitante() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Comprobante de Reserva"),
            rx.dialog.description("Introduce tu correo electrónico para enviarte el ticket con el código de acceso."),
            rx.vstack(
                rx.input(
                    placeholder="ejemplo@correo.com",
                    value=VisitanteState.email_visitante,
                    on_change=VisitanteState.set_email_visitante,
                    width="100%",
                ),
                rx.cond(
                    VisitanteState.error_correo != "",
                    rx.text(VisitanteState.error_correo, color="red", size="2")
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button("Cancelar", variant="soft", color_scheme="gray")
                    ),
                    rx.button(
                        "Confirmar y Enviar Ticket",
                        on_click=VisitanteState.validar_y_finalizar_reserva,
                        color_scheme="purple"
                    ),
                    justify="end",
                    width="100%",
                    spacing="3"
                ),
                spacing="4",
                padding_y="1em"
            )
        ),
        open=VisitanteState.show_modal_correo,
    )


def modal_pago_tarjeta() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Pago con Tarjeta - Tarifa Visitante"),
            rx.dialog.description("El importe total a pagar es de 7,50 €."),
            rx.vstack(
                rx.input(placeholder="Número de Tarjeta (16 dígitos)", width="100%"),
                rx.hstack(
                    rx.input(placeholder="MM/AA", width="50%"),
                    rx.input(placeholder="CVC", width="50%"),
                    width="100%"
                ),
                rx.hstack(
                    rx.button("Cancelar", on_click=VisitanteState.cerrar_modal_pago, variant="soft", color_scheme="gray"),
                    rx.button("Pagar 7,50 €", on_click=VisitanteState.proceder_al_correo, color_scheme="green"),
                    justify="end",
                    width="100%",
                    spacing="3"
                ),
                spacing="4",
                padding_y="1em"
            )
        ),
        open=VisitanteState.show_modal_pago,
    )


def visitante_reserva_content() -> rx.Component:
    """Contenido interior de la vista de reserva del visitante."""
    return rx.vstack(
        rx.card(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.badge("Acceso Visitante", color_scheme="purple", variant="surface", radius="full"),
                        rx.badge("7,50 €", color_scheme="green", variant="surface", radius="full"),
                        spacing="2",
                    ),
                    rx.heading("Elige tu Menú de Hoy", size="6", weight="bold", color="#111827"),
                    rx.text("Selecciona tus platos preferidos para el día de hoy. Tarifa general fija sin acreditación ULE.", color="#4B5563", size="3"),
                    spacing="2",
                    align_items="start",
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
        rx.cond(
            VisitanteState.has_menu_hoy,
            rx.vstack(
                rx.grid(
                    section_platos_visitante(
                        "Primer Plato", 
                        "soup", 
                        VisitanteState.platos_primeros, 
                        VisitanteState.plato_1_sel, 
                        VisitanteState.set_plato_1_sel
                    ),
                    section_platos_visitante(
                        "Segundo Plato", 
                        "utensils", 
                        VisitanteState.platos_segundos, 
                        VisitanteState.plato_2_sel, 
                        VisitanteState.set_plato_2_sel
                    ),
                    section_platos_visitante(
                        "Postre", 
                        "apple", 
                        VisitanteState.platos_postres, 
                        VisitanteState.postre_sel, 
                        VisitanteState.set_postre_sel
                    ),
                    columns="3",
                    spacing="4",
                    width="100%",
                ),
                rx.divider(margin_y="1em"),
                rx.hstack(
                    rx.spacer(),
                    rx.button(
                        rx.icon("credit-card", size=20),
                        rx.text("Pagar Menú (7,50 €)", weight="bold"),
                        size="4",
                        color_scheme="purple",
                        radius="large",
                        cursor="pointer",
                        on_click=VisitanteState.abrir_modal_pago,
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
        modal_pago_tarjeta(),
        modal_correo_visitante(),
        spacing="5",
        width="100%",
    )


@rx.page(route="/visitante/reserva", title="Reserva Visitante | MenULE", on_load=VisitanteState.cargar_menu_del_dia)
def visitante_reserva_page() -> rx.Component:
    """Página principal envuelta en el Layout para conservar la barra lateral."""
    return layout(visitante_reserva_content())