from src.modelo.BussinessObject import BussinessObject
from src.modelo.dao.IngredienteDao import IngredienteDao

class ControladorIngredientes(BussinessObject):
    def __init__(self):
        print("Controlador de Ingredientes inicializado")
        super().__init__()

    def obtener_ingredientes(self):
        dao = IngredienteDao()
        return dao.obtener_ingredientes()

    def actualizar_ingrediente(self, id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno):
        dao = IngredienteDao()
        return dao.actualizar_ingrediente(
            id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno
        )

    def guardar_nuevo_ingrediente(self, id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno):
        dao = IngredienteDao()
        return dao.insertar_ingrediente(
            id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno
        )