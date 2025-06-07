from src.modelo.dao.IngredienteDao import IngredienteDao

class LogicaIngrediente:
    def __init__(self):
        self.dao = IngredienteDao()

    def obtener_ingredientes(self):
        return self.dao.obtener_ingredientes()

    def actualizar_ingrediente(self, id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno):
        return self.dao.actualizar_ingrediente(
            id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno
        )

    def guardar_nuevo_ingrediente(self, id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno):
        return self.dao.insertar_ingrediente(
            id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno
        )