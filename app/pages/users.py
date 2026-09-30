import reflex as rx

from app.components.layout import layout
from app.states.user_state import UserState


def modal_nuevo_usuario():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Nuevo usuario"),
            rx.dialog.description(
                "Introduce la información del nuevo usuario."
            ),
            rx.vstack(
                rx.vstack(
                    rx.text("DNI", weight="medium"),
                    rx.input(
                        placeholder="12345678X",
                        value=UserState.form_dni,
                        on_change=UserState.set_form_dni,
                        width="100%",
                        radius="large",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Nombre", weight="medium"),
                    rx.input(
                        placeholder="Nombre",
                        value=UserState.form_nombre,
                        on_change=UserState.set_form_nombre,
                        width="100%",
                        radius="large",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Apellido", weight="medium"),
                    rx.input(
                        placeholder="Apellido",
                        value=UserState.form_apellido,
                        on_change=UserState.set_form_apellido,
                        width="100%",
                        radius="large",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Correo electrónico", weight="medium"),
                    rx.input(
                        placeholder="correo@unileon.es",
                        value=UserState.form_email,
                        on_change=UserState.set_form_email,
                        width="100%",
                        radius="large",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Contraseña", weight="medium"),
                    rx.input(
                        placeholder="••••••••",
                        type="password",
                        value=UserState.form_password,
                        on_change=UserState.set_form_password,
                        width="100%",
                        radius="large",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Teléfono", weight="medium"),
                    rx.input(
                        placeholder="600000000",
                        value=UserState.form_telefono,
                        on_change=UserState.set_form_telefono,
                        width="100%",
                        radius="large",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Rol", weight="medium"),
                    rx.select(
                        [
                            "estudiante",
                            "profesor",
                            "administrador",
                            "personal_comedor",
                            "visitante",
                        ],
                        value=UserState.form_tipo,
                        on_change=UserState.set_form_tipo,
                        width="100%",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            variant="soft",
                            color_scheme="gray",
                            radius="large",
                        )
                    ),
                    rx.button(
                        rx.icon("user-plus"),
                        "Crear usuario",
                        color_scheme="violet",
                        radius="large",
                        on_click=UserState.crear_usuario,
                    ),
                    justify="end",
                    width="100%",
                    padding_top="1em",
                ),
                spacing="4",
            ),
            max_width="520px",
            padding="2em",
        ),
        open=UserState.show_modal_nuevo,
        on_open_change=UserState.set_show_modal_nuevo,
    )


def modal_editar_usuario():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Editar usuario"),
            rx.dialog.description(
                "Modifica la información del usuario."
            ),
            rx.vstack(
                rx.vstack(
                    rx.text("DNI", weight="medium"),
                    rx.input(
                        value=UserState.form_dni,
                        on_change=UserState.set_form_dni,
                        width="100%",
                        radius="large",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Nombre", weight="medium"),
                    rx.input(
                        value=UserState.form_nombre,
                        on_change=UserState.set_form_nombre,
                        width="100%",
                        radius="large",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Apellido", weight="medium"),
                    rx.input(
                        value=UserState.form_apellido,
                        on_change=UserState.set_form_apellido,
                        width="100%",
                        radius="large",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Email", weight="medium"),
                    rx.input(
                        value=UserState.form_email,
                        on_change=UserState.set_form_email,
                        width="100%",
                        radius="large",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Nueva contraseña (dejar en blanco para conservar la actual)", weight="medium"),
                    rx.input(
                        placeholder="••••••••",
                        type="password",
                        value=UserState.form_password,
                        on_change=UserState.set_form_password,
                        width="100%",
                        radius="large",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Teléfono", weight="medium"),
                    rx.input(
                        value=UserState.form_telefono,
                        on_change=UserState.set_form_telefono,
                        width="100%",
                        radius="large",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Rol", weight="medium"),
                    rx.select(
                        [
                            "estudiante",
                            "profesor",
                            "administrador",
                            "personal_comedor",
                            "visitante",
                        ],
                        value=UserState.form_tipo,
                        on_change=UserState.set_form_tipo,
                        width="100%",
                    ),
                    width="100%",
                    align_items="start",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            variant="soft",
                            color_scheme="gray",
                            radius="large",
                        )
                    ),
                    rx.button(
                        rx.icon("save"),
                        "Guardar cambios",
                        color_scheme="violet",
                        radius="large",
                        on_click=UserState.guardar_edicion_usuario,
                    ),
                    justify="end",
                    width="100%",
                    padding_top="1em",
                ),
                spacing="4",
            ),
            max_width="520px",
            padding="2em",
        ),
        open=UserState.show_modal_editar,
        on_open_change=UserState.set_show_modal_editar,
    )


def users_page():
    return layout(
        rx.vstack(
            modal_nuevo_usuario(),
            modal_editar_usuario(),
            rx.vstack(
                rx.heading(
                    "Usuarios",
                    size="8",
                ),
                rx.text(
                    "Gestiona las cuentas registradas en MenULE.",
                    color="gray",
                ),
                align_items="start",
                spacing="1",
                width="100%",
            ),
            rx.card(
                rx.hstack(
                    rx.input(
                        placeholder="Buscar usuario...",
                        value=UserState.search_text,
                        on_change=UserState.set_search_text,
                        width="340px",
                        radius="large",
                    ),
                    rx.button(
                        rx.icon("search"),
                        "Buscar",
                        on_click=UserState.load_users,
                        variant="soft",
                        color_scheme="gray",
                        radius="large",
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon("user-plus"),
                        "Nuevo usuario",
                        on_click=UserState.abrir_modal_nuevo,
                        color_scheme="violet",
                        radius="large",
                    ),
                    width="100%",
                    align="center",
                ),
                width="100%",
                padding="1.25em",
            ),
            rx.card(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("ID"),
                            rx.table.column_header_cell("Nombre"),
                            rx.table.column_header_cell("Apellido"),
                            rx.table.column_header_cell("Correo"),
                            rx.table.column_header_cell("Rol"),
                            rx.table.column_header_cell("Acciones"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            UserState.users,
                            lambda user: rx.table.row(
                                rx.table.cell(user.id_usuario),
                                rx.table.cell(user.nombre),
                                rx.table.cell(user.apellido),
                                rx.table.cell(user.email),
                                rx.table.cell(
                                    rx.badge(
                                        user.tipo,
                                        variant="soft",
                                        color_scheme=rx.cond(
                                            user.tipo == "administrador",
                                            "red",
                                            rx.cond(
                                                user.tipo == "estudiante",
                                                "blue",
                                                rx.cond(
                                                    user.tipo == "profesor",
                                                    "indigo",
                                                    rx.cond(
                                                        user.tipo == "personal_comedor",
                                                        "orange",
                                                        "gray",
                                                    ),
                                                ),
                                            ),
                                        ),
                                    )
                                ),
                                rx.table.cell(
                                    rx.hstack(
                                        rx.button(
                                            rx.icon("square-pen"),
                                            variant="soft",
                                            color_scheme="gray",
                                            radius="large",
                                            on_click=lambda: UserState.abrir_modal_editar(user),
                                        ),
                                        rx.button(
                                            rx.icon("trash-2"),
                                            variant="soft",
                                            color_scheme="red",
                                            radius="large",
                                            on_click=lambda: UserState.eliminar_usuario(
                                                user.id_usuario
                                            ),
                                        ),
                                        spacing="2",
                                    )
                                ),
                            ),
                        )
                    ),
                    variant="surface",
                    size="3",
                ),
                width="100%",
                padding="1.5em",
                border_radius="20px",
            ),
            spacing="5",
            width="100%",
            on_mount=UserState.load_users,
        )
    )