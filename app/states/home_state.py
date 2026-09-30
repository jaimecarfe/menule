import reflex as rx

from app.services.home_service import HomeService


class HomeState(rx.State):
    total_users: int = 0
    total_menus: int = 0
    total_reservations: int = 0
    total_incidents: int = 0

    upcoming_menus: list[dict] = []

    async def load_dashboard_data(self):
        """Carga las estadísticas y menús desde la BBDD."""
        stats = HomeService.get_dashboard_stats()

        self.total_users = int(stats.get("total_users", 0))
        self.total_menus = int(stats.get("total_menus", 0))
        self.total_reservations = int(stats.get("total_reservations", 0))
        self.total_incidents = int(stats.get("total_incidents", 0))

        self.upcoming_menus = HomeService.get_upcoming_menus()