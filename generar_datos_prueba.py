# generar_datos_prueba.py
import random
from datetime import datetime, timedelta
from src.modelo.conexion.Conexion import Conexion

# Clasificamos correctamente la comida para que haga match con los IFs de la Vista
DICCIONARIO_PLATOS = {
    "primero": ["Crema de Verduras", "Lentejas Pardinas", "Ensalada Cesar", "Macarrones Bolonesa", "Salmorejo Cordobes", "Arroz Tres Delicias"],
    "segundo": ["Pechuga de Pollo", "Merluza al Horno", "Hamburguesa Completa", "Estofado de Ternera", "Lomo Adobado", "Lasana Vegetal"],
    "postre": ["Flan de Huevo", "Fruta de Temporada", "Yogur Natural", "Tarta de Queso", "Helado de Vainilla", "Brownie de Chocolate"]
}

def sembrar_datos_correctos():
    db = Conexion()
    cursor = db.getCursor()
    connection = None
    
    if hasattr(cursor, '_connection'):
        connection = cursor._connection
    elif hasattr(cursor, 'connection'):
        connection = cursor.connection

    print("🧹 Limpiando menús de prueba antiguos esquivando restricciones...")
    try:
        # DESACTIVAR temporalmente restricciones de clave foránea
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        # Vaciamos con seguridad las tablas para eliminar el histórico viejo
        cursor.execute("DELETE FROM MenuPlatos")
        cursor.execute("DELETE FROM Menus")
        cursor.execute("DELETE FROM Platos")
        
        if connection:
            try: connection.commit()
            except Exception: pass
        print("✅ Base de datos de menús reseteada con éxito.")

        print("⏳ Inyectando platos estructurados (primeros, segundos y postres) para 2026...")

        # 1. Insertar todos los platos con sus tipos reales requeridos por la UI ('primero', 'segundo', 'postre')
        for tipo_real, lista_comida in DICCIONARIO_PLATOS.items():
            for nombre_plato in lista_comida:
                cursor.execute("""
                    INSERT INTO Platos (nombre, tipo, alergenos) 
                    VALUES (?, ?, 'Ninguno')
                """, (nombre_plato, tipo_real))
        
        if connection: 
            try: connection.commit()
            except Exception: pass

        # 2. Generar menús para los próximos 30 días
        fecha_inicio = datetime.now().date() - timedelta(days=2)
        
        for i in range(32):
            fecha_target = fecha_inicio + timedelta(days=i)
            fecha_str = fecha_target.strftime('%Y-%m-%d')

            # Creamos el contenedor del menú para este día
            cursor.execute("INSERT INTO Menus (fecha, tipo, max_reservas, disponible) VALUES (?, 'almuerzo', 100, 1)", (fecha_str,))
            
            cursor.execute("SELECT id_menu FROM Menus WHERE fecha = ? AND tipo = 'almuerzo'", (fecha_str,))
            id_menu = cursor.fetchone()[0]

            # Seleccionamos un plato aleatorio real de cada categoría
            p1 = random.choice(DICCIONARIO_PLATOS["primero"])
            p2 = random.choice(DICCIONARIO_PLATOS["segundo"])
            p3 = random.choice(DICCIONARIO_PLATOS["postre"])

            for nombre_p in [p1, p2, p3]:
                cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (nombre_p,))
                id_plato = cursor.fetchone()[0]
                
                # Asociamos a la tabla intermedia MenuPlatos
                cursor.execute("INSERT INTO MenuPlatos (id_menu, id_plato) VALUES (?, ?)", (id_menu, id_plato))
            
            print(f" 📅 Menú estructurado listo: {fecha_str} -> [{p1} (1º) | {p2} (2º) | {p3} (Postre)]")

        if connection: 
            try: connection.commit()
            except Exception: pass
            
        print("\n🚀 ¡Sincronización completa! Las categorías ya están corregidas.")

    except Exception as e:
        print(f"❌ Error crítico durante la siembra: {e}")
        if connection:
            try: connection.rollback()
            except Exception: pass
    finally:
        # REACTIVAR siempre las restricciones de clave foránea al terminar
        try:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        except Exception:
            pass
        try: 
            cursor.close()
        except Exception: 
            pass

if __name__ == "__main__":
    sembrar_datos_correctos()