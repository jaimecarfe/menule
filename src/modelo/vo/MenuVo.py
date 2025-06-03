class MenuVo:
    def __init__(self, id_menu=None, fecha=None, tipo=None, max_reservas=100, disponible=True):
        self.id_menu = id_menu
        self.fecha = fecha
        self.tipo = tipo
        self.max_reservas = max_reservas
        self.disponible = disponible