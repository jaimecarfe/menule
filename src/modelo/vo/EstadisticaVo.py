class EstadisticaVo:
    def __init__(self, tipo, datos):
        self.tipo = tipo  # 'pagos', 'incidencias', 'menus', 'reservas'
        self.datos = datos  # lista de tuplas/objetos con la información