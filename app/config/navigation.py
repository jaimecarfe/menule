from pydantic import BaseModel


ROLE_ADMINISTRADOR = "administrador"
ROLE_ESTUDIANTE = "estudiante"
ROLE_PROFESOR = "profesor"
ROLE_PERSONAL_COMEDOR = "personal_comedor"
ROLE_VISITANTE = "visitante"


class NavigationItem(BaseModel):
    title: str
    icon: str
    href: str


NAV_ITEMS = {
    ROLE_ADMINISTRADOR: [
        NavigationItem(title="Dashboard", icon="layout-dashboard", href="/home"),
        NavigationItem(title="Usuarios", icon="users", href="/usuarios"),
        NavigationItem(title="Menús", icon="utensils-crossed", href="/menus"),
        NavigationItem(title="Platos", icon="soup", href="/platos"),
        NavigationItem(title="Reservas", icon="calendar-days", href="/reservas"),
        NavigationItem(title="Pagos", icon="credit-card", href="/pagos"),
        NavigationItem(title="Incidencias", icon="triangle-alert", href="/incidencias"),
        NavigationItem(title="Estadísticas", icon="chart-column", href="/estadisticas"),
        NavigationItem(title="Mi perfil", icon="user", href="/perfil"),
    ],
    ROLE_ESTUDIANTE: [
        NavigationItem(title="Inicio", icon="house", href="/home"),
        NavigationItem(title="Menú del día", icon="utensils", href="/menu"),
        NavigationItem(title="Mis reservas", icon="calendar-check", href="/reservas"),  # 🛠️ Apunta a /reservas
        NavigationItem(title="Monedero", icon="wallet", href="/monedero"),
        NavigationItem(title="Incidencias", icon="triangle-alert", href="/mis-incidencias"),
        NavigationItem(title="Mi perfil", icon="user", href="/perfil"),
    ],
    ROLE_PROFESOR: [
        NavigationItem(title="Inicio", icon="house", href="/home"),
        NavigationItem(title="Menú del día", icon="utensils", href="/menu"),
        NavigationItem(title="Mis reservas", icon="calendar-check", href="/reservas"),  # 🛠️ Apunta a /reservas
        NavigationItem(title="Monedero", icon="wallet", href="/monedero"),
        NavigationItem(title="Incidencias", icon="triangle-alert", href="/mis-incidencias"),
        NavigationItem(title="Mi perfil", icon="user", href="/perfil"),
    ],
    ROLE_PERSONAL_COMEDOR: [
        NavigationItem(title="Inicio", icon="layout-dashboard", href="/home"),
        NavigationItem(title="Menú", icon="utensils-crossed", href="/menus"),
        NavigationItem(title="Pedidos", icon="chef-hat", href="/pedidos"),
        NavigationItem(title="Stock", icon="boxes", href="/stock"),
        NavigationItem(title="Incidencias", icon="triangle-alert", href="/incidencias"),
        NavigationItem(title="Mi perfil", icon="user", href="/perfil"),
    ],
    ROLE_VISITANTE: [
        NavigationItem(title="Inicio", icon="layout-dashboard", href="/home"),
        NavigationItem(title="Menú", icon="utensils", href="/visitante"),
        NavigationItem(title="Reservar", icon="ticket", href="/visitante/reserva"),
    ],
}