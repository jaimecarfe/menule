import reflex as rx

from app.pages.login import login_page
from app.pages.home import home_page
from app.pages.users import users_page
from app.pages.menus import menus_page
from app.pages.platos import platos_page
from app.pages.registro import registro_page
from app.pages.pagos import pagos_page
from app.pages.incidencias import incidencias_page
from app.pages.estadisticas import estadisticas_page
from app.pages.reservas import reservas_page
from app.pages.perfil import perfil_page
from app.pages.pedidos import pedidos_page
from app.pages.stock import stock_page
from app.pages.visitante_reserva import visitante_reserva_page

from app.states.home_state import HomeState
from app.states.plato_state import PlatoState
from app.states.pago_state import PagoState
from app.states.pedido_state import PedidoState
from app.states.stock_state import StockState
from app.states.reserva_state import ReservaState
from app.states.user_state import UserState
from app.states.estadistica_state import EstadisticaState


app = rx.App()

# Autenticación y Registro
app.add_page(
    login_page,
    route="/",
    title="Login | MenULE",
)

app.add_page(
    registro_page,
    route="/registro",
    title="Registro | MenULE",
)

# Dashboard Principal
app.add_page(
    home_page,
    route="/home",
    title="Inicio | MenULE",
    on_load=HomeState.load_dashboard_data,
)

# Menús
app.add_page(
    menus_page,
    route="/menus",
    title="Menús | MenULE",
)

app.add_page(
    menus_page,
    route="/menu",
    title="Menú del Día | MenULE",
)

app.add_page(
    menus_page,
    route="/visitante",
    title="Menú del Día | MenULE",
)

# Reservas
app.add_page(
    reservas_page,
    route="/reservas",
    title="Reservas | MenULE",
    on_load=ReservaState.load_reservas,
)

app.add_page(
    reservas_page,
    route="/mis-reservas",
    title="Mis Reservas | MenULE",
    on_load=ReservaState.load_reservas,
)

# Pedidos / Comandas (Personal de Comedor)
app.add_page(
    pedidos_page,
    route="/pedidos",
    title="Procesar Pedidos | MenULE",
    on_load=PedidoState.cargar_pedidos,
)

# Catálogo de Platos
app.add_page(
    platos_page,
    route="/platos",
    title="Platos | MenULE",
    on_load=PlatoState.load_platos,
)

# Gestión de Usuarios
app.add_page(
    users_page,
    route="/usuarios",
    title="Usuarios | MenULE",
    on_load=UserState.load_users,
)

# Pagos / Monedero TUI
app.add_page(
    pagos_page,
    route="/pagos",
    title="Pagos | MenULE",
    on_load=PagoState.load_pagos,
)

# Alias para la vista de Monedero desde la Home
app.add_page(
    pagos_page,
    route="/monedero",
    title="Monedero TUI | MenULE",
    on_load=PagoState.load_pagos,
)

# Incidencias
app.add_page(
    incidencias_page, 
    route="/incidencias", 
    title="Gestión de Incidencias | MenULE",
)

app.add_page(
    incidencias_page, 
    route="/mis-incidencias", 
    title="Mis Incidencias | MenULE",
)

# Estadísticas y Analítica
app.add_page(
    estadisticas_page,
    route="/estadisticas",
    title="Estadísticas y Analítica | MenULE",
    on_load=EstadisticaState.load_estadisticas,
)

# Perfil de Usuario
app.add_page(
    perfil_page, 
    route="/perfil", 
    title="Mi Perfil | MenULE",
)

# Inventario de Stock
app.add_page(
    stock_page,
    route="/stock",
    title="Inventario de Stock | MenULE",
    on_load=StockState.cargar_stock,
)


app.add_page(
    visitante_reserva_page,
    route="/visitante/reserva",
    title="Reserva Visitante | MenULE",
)

