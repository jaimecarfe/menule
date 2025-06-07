import mysql.connector

# CONFIGURA TU CONEXIÓN
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",  # Cambia esto si tu contraseña es diferente
    database="menule"
)
cursor = conn.cursor()

# Elimina el contenido de la tabla Ingredientes y reinicia el contador de autoincremento
cursor.execute("DELETE FROM Ingredientes")
cursor.execute("ALTER TABLE Ingredientes AUTO_INCREMENT = 1")

# Lista de ingredientes a insertar: (nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno)
ingredientes = [
    ("Leche", "litros", 20, 5, True, "Lácteos"),
    ("Harina", "kg", 50, 10, False, ""),
    ("Huevos", "unidades", 100, 20, True, "Huevo"),
    ("Tomate", "kg", 30, 5, False, ""),
    ("Pollo", "kg", 25, 5, False, ""),
    ("Pescado", "kg", 15, 3, True, "Pescado"),
    ("Frutos secos", "kg", 10, 2, True, "Frutos secos"),
    ("Pan", "unidades", 40, 10, False, ""),
    ("Queso", "kg", 12, 3, True, "Lácteos"),
    ("Manzana", "kg", 20, 5, False, "")
]

for nombre, unidad, stock, minimo, alergeno, tipo in ingredientes:
    cursor.execute("""
        INSERT INTO Ingredientes (nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, unidad, stock, minimo, int(alergeno), tipo))

conn.commit()
cursor.close()
conn.close()

print("Ingredientes insertados correctamente.")