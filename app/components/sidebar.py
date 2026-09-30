import reflex as rx
from app.states.auth_state import AppState
from app.config.navigation import NavigationItem


def _section_title(title: str) -> rx.Component:
    return rx.text(
        title,
        size="1",
        weight="bold",
        color="#9CA3AF",
        style={"letterSpacing": "0.08em"},
        text_transform="uppercase",
        margin_top="0.5em",
    )


def sidebar_item(item: NavigationItem) -> rx.Component:
    is_active = rx.State.router.page.path == item.href

    return rx.link(
        rx.hstack(
            rx.icon(
                item.icon,
                size=18,
                color=rx.cond(is_active, "#7C3AED", "#6B7280"),
            ),
            rx.text(
                item.title,
                weight=rx.cond(is_active, "bold", "medium"),
                color=rx.cond(is_active, "#111827", "#374151"),
            ),
            spacing="3",
            width="100%",
            padding="0.72em 0.8em",
            border_radius="12px",
            background=rx.cond(is_active, "rgba(124,58,237,0.10)", "transparent"),
            border=rx.cond(is_active, "1px solid rgba(124,58,237,0.22)", "1px solid transparent"),
            style={"transition": "all 180ms ease"},
            _hover={
                "background": "#F3F4F6",
                "transform": "translateX(2px)",
            },
        ),
        href=item.href,
        underline="none",
        width="100%",
    )


def _grouped_items() -> rx.Component:
    return rx.vstack(
        rx.cond(
            AppState.is_admin,
            rx.vstack(
                _section_title("General"),
                rx.foreach(AppState.navigation_items[:2], sidebar_item),
                _section_title("Gestión"),
                rx.foreach(AppState.navigation_items[2:6], sidebar_item),
                _section_title("Sistema"),
                rx.foreach(AppState.navigation_items[6:], sidebar_item),
                spacing="2",
                width="100%",
                align_items="start",
            ),
            rx.cond(
                (AppState.is_estudiante | AppState.is_profesor),
                rx.vstack(
                    _section_title("General"),
                    rx.foreach(AppState.navigation_items[:2], sidebar_item),
                    _section_title("Servicios"),
                    rx.foreach(AppState.navigation_items[2:5], sidebar_item),
                    _section_title("Cuenta"),
                    rx.foreach(AppState.navigation_items[5:], sidebar_item),
                    spacing="2",
                    width="100%",
                    align_items="start",
                ),
                rx.cond(
                    AppState.is_cocina,
                    rx.vstack(
                        _section_title("Operación"),
                        rx.foreach(AppState.navigation_items[:4], sidebar_item),
                        _section_title("Cuenta"),
                        rx.foreach(AppState.navigation_items[4:], sidebar_item),
                        spacing="2",
                        width="100%",
                        align_items="start",
                    ),
                    rx.vstack(
                        _section_title("Visitante"),
                        rx.foreach(AppState.navigation_items, sidebar_item),
                        spacing="2",
                        width="100%",
                        align_items="start",
                    ),
                ),
            ),
        ),
        width="100%",
        spacing="1",
        align_items="start",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.image(src="/logo_menule.png", width="34px", height="34px"),
                rx.heading("MenULE", size="6", weight="bold", color="#111827"),
                spacing="3",
                align="center",
                width="100%",
            ),
            rx.divider(),
            _grouped_items(),
            rx.spacer(),
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text(AppState.user_name, weight="bold", size="2", color="#111827"),
                            rx.text(AppState.user_role, size="1", color="#6B7280"),
                            spacing="0",
                            align_items="start",
                        ),
                        rx.spacer(),
                        rx.cond(
                            (AppState.is_estudiante | AppState.is_profesor),
                            rx.badge(
                                AppState.user_saldo.to_string() + " €",
                                color_scheme="violet",
                                variant="soft",
                                radius="full",
                            ),
                        ),
                        align="center",
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                width="100%",
                padding="0.8em 0.9em",
                style={
                    "borderRadius": "14px",
                    "border": "1px solid #E5E7EB",
                    "background": "white",
                },
            ),
            spacing="4",
            width="100%",
            height="100%",
            align_items="stretch",
        ),
        width="272px",
        min_width="272px",
        max_width="272px",
        padding="1.2em",
        border_right="1px solid #E5E7EB",
        background="white",
        position="sticky",
        top="0",
        height="100vh",
    )