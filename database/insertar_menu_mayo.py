import mysql.connector
from datetime import datetime, timedelta

# CONFIGURA TU CONEXIÓN
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin123",  # <--- cambia esto
    database="menule"
)
cursor = conn.cursor()

# 1. Insertar platos si no existen
platos = [
    ("Sopa de verduras", "primero", 3.50),
    ("Ensalada mixta", "primero", 3.00),
    ("Macarrones con tomate", "primero", 3.80),
    ("Pollo asado", "segundo", 5.00),
    ("Merluza al horno", "segundo", 5.50),
    ("Tortilla española", "segundo", 4.80),
    ("Fruta fresca", "postre", 2.00),
    ("Yogur natural", "postre", 2.20)
]

for nombre, tipo, precio in platos:
    cursor.execute("""
        INSERT IGNORE INTO Platos (nombre, tipo, precio)
        VALUES (%s, %s, %s)
    """, (nombre, tipo, precio))

# 2. Insertar menús del 1 al 31 de mayo 2025
fechas_mayo = [datetime(2025, 5, 1) + timedelta(days=i) for i in range(31)]
for fecha in fechas_mayo:
    cursor.execute("""
        INSERT INTO Menus (fecha, tipo, max_reservas, disponible)
        VALUES (%s, 'almuerzo', 100, TRUE)
    """, (fecha.strftime("%Y-%m-%d"),))

# 3. Vincular todos los platos con todos los menús de mayo
cursor.execute("""
    SELECT id_menu FROM Menus WHERE fecha BETWEEN '2025-05-01' AND '2025-05-31'
""")
id_menus = [row[0] for row in cursor.fetchall()]

cursor.execute("""
    SELECT id_plato FROM Platos
    WHERE nombre IN (
        'Sopa de verduras', 'Ensalada mixta', 'Macarrones con tomate',
        'Pollo asado', 'Merluza al horno', 'Tortilla española',
        'Fruta fresca', 'Yogur natural'
    )
""")
id_platos = [row[0] for row in cursor.fetchall()]

for id_menu in id_menus:
    for id_plato in id_platos:
        cursor.execute("""
            INSERT INTO MenuPlatos (id_menu, id_plato)
            VALUES (%s, %s)
        """, (id_menu, id_plato))

# Guardar cambios
conn.commit()
cursor.close()
conn.close()

print("✅ Inserción completada.")
