class IngredienteVo:
    def __init__(self, id_ingrediente: int, nombre: str, unidad_medida: str, stock_actual: float,
                 stock_minimo: float, alergeno: bool, tipo_alergeno: str):
        self.id_ingrediente = id_ingrediente
        self.nombre = nombre
        self.unidad_medida = unidad_medida
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.alergeno = alergeno
        self.tipo_alergeno = tipo_alergeno
