import sqlite3
from src.modelo.conexion.Conexion import Conexion

class IngredienteDao:
    def obtener_ingredientes(self):
        cursor = self.getCursor()
        cursor.execute("SELECT id, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno FROM Ingredientes")
        rows = cursor.fetchall()
        cursor.close()
        return [
            {
                "id": row[0],
                "nombre": row[1],
                "unidad": row[2],
                "stock": row[3],
                "minimo": row[4],
                "alergeno": row[5],
                "tipo": row[6]
            }
            for row in rows
        ]

    def actualizar_ingrediente(self, id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno):
        conexion = Conexion()
        cursor = conexion.getCursor()
        cursor.execute(
            "UPDATE Ingredientes SET nombre=?, unidad_medida=?, stock_actual=?, stock_minimo=?, alergeno=?, tipo_alergeno=? WHERE id_ingrediente=?",
            (nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno, id_ingrediente)
        )
        conexion.conexion.commit()
    
    def insertar_ingrediente(self, id_ingrediente, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno):
        conexion = Conexion()
        cursor = conexion.getCursor()
        cursor.execute(
            "INSERT INTO Ingredientes (nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno)
        )
        # Llama a commit sobre la conexión real
        conexion.conexion.commit()