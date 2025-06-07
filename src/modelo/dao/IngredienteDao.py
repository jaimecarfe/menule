import sqlite3
from src.modelo.conexion.Conexion import Conexion

class IngredienteDao:
    def obtener_ingredientes(self):
        cursor = Conexion().getCursor()
        cursor.execute("SELECT id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno FROM Ingredientes")
        rows = cursor.fetchall()
        cursor.close()
        return rows if rows is not None else []


    def actualizar_ingrediente(self, id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno):
        conexion = Conexion()
        cursor = conexion.getCursor()
        cursor.execute(
            "UPDATE Ingredientes SET nombre=?, unidad_medida=?, stock_actual=?, stock_minimo=?, alergeno=?, tipo_alergeno=? WHERE id_ingrediente=?",
            (nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno, id_ingrediente)
        )
        #conexion.conexion.commit()
    
    def insertar_ingrediente(self, id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno):
        conexion = Conexion()
        cursor = conexion.getCursor()
        if id_ingrediente is not None:
            cursor.execute(
                "INSERT INTO Ingredientes (id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno)
            )
        else:
            cursor.execute(
                "INSERT INTO Ingredientes (nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno) VALUES (?, ?, ?, ?, ?, ?)",
                (nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno)
            )
        #conexion.conexion.commit()