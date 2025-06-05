from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.MenuVo import MenuVo

class MenuDao:
    def getCursor(self):
        return Conexion().getCursor()

    def insertar_o_modificar_menu_con_tipo(self, fecha, lista_platos_con_tipo):
        """
        Inserta o actualiza un menú y sus platos clasificados por tipo.
        :param fecha: str 'YYYY-MM-DD'
        :param lista_platos_con_tipo: lista de tuplas (nombre_plato, tipo)
        """
        try:
            conn = Conexion()
            cursor = conn.getCursor()

            try:
                cursor.execute("""
                    INSERT INTO Menus (fecha, tipo, max_reservas, disponible)
                    VALUES (?, 'almuerzo', 100, 1)
                """, (fecha,))
            except Exception:
                cursor.execute("""
                    UPDATE Menus SET disponible = 1 WHERE fecha = ? AND tipo = 'almuerzo'
                """, (fecha,))

            cursor.execute("SELECT id_menu FROM Menus WHERE fecha = ? AND tipo = 'almuerzo'", (fecha,))
            result = cursor.fetchone()
            if not result:
                print("No se pudo obtener el menú para la fecha:", fecha)
                cursor.close()
                return False

            id_menu = result[0]

            cursor.execute("DELETE FROM MenuPlatos WHERE id_menu = ?", (id_menu,))

            for nombre, tipo in lista_platos_con_tipo:
                cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (nombre,))
                row = cursor.fetchone()

                if row:
                    id_plato = row[0]
                else:
                    cursor.execute("""
                        INSERT INTO Platos (nombre, tipo, precio)
                        VALUES (?, ?, 0.00)
                    """, (nombre, tipo))

                    cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (nombre,))
                    id_plato = cursor.fetchone()[0]

                cursor.execute("INSERT INTO MenuPlatos (id_menu, id_plato) VALUES (?, ?)", (id_menu, id_plato))

            cursor.close()
            return True

        except Exception as e:
            print("Error al modificar menú:", e)
            try:
                cursor.close()
            except Exception:
                pass
            return False

    def obtener_platos_por_fecha(self, fecha):
        cursor = self.getCursor()
        cursor.execute("""
            SELECT p.nombre, p.tipo, p.alergenos
            FROM Menus m
            JOIN MenuPlatos mp ON m.id_menu = mp.id_menu
            JOIN Platos p ON mp.id_plato = p.id_plato
            WHERE m.fecha = ? AND m.tipo = 'almuerzo'
        """, (fecha,))
        platos = cursor.fetchall()
        cursor.close()
        return platos
    
    def listar_disponibles(self):
        cursor = self.getCursor()
        cursor.execute("""
            SELECT m.id_menu, m.fecha, m.tipo
            FROM Menus m
            WHERE m.disponible = 1
        """)
        rows = cursor.fetchall()
        cursor.close()
        return [
            {"id_menu": row[0], "fecha": row[1], "tipo": row[2]}
            for row in rows
        ]
    
    def guardar_menu_con_alergenos(self, fecha, lista_platos):
        try:
            conn = Conexion()
            cursor = conn.getCursor()

            # Crear menú si no existe
            cursor.execute("""
                INSERT INTO Menus (fecha, tipo, max_reservas, disponible)
                VALUES (?, 'almuerzo', 100, 1)
                ON DUPLICATE KEY UPDATE disponible = 1
            """, (fecha,))
            cursor.execute("SELECT id_menu FROM Menus WHERE fecha = ?", (fecha,))
            id_menu = cursor.fetchone()[0]

            cursor.execute("DELETE FROM MenuPlatos WHERE id_menu = ?", (id_menu,))

            for nombre, tipo, alergenos in lista_platos:
                cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (nombre,))
                row = cursor.fetchone()
                if row:
                    id_plato = row[0]
                    cursor.execute("UPDATE Platos SET tipo = ?, alergenos = ? WHERE id_plato = ?", (tipo, alergenos, id_plato))
                else:
                    cursor.execute("INSERT INTO Platos (nombre, tipo, precio, alergenos) VALUES (?, ?, 0.00, ?)", (nombre, tipo, alergenos))
                    cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (nombre,))
                    id_plato = cursor.fetchone()[0]

                cursor.execute("INSERT INTO MenuPlatos (id_menu, id_plato) VALUES (?, ?)", (id_menu, id_plato))

            return True
        except Exception as e:
            print("Error al guardar menú con alérgenos:", e)
            return False

    def obtener_id_menu_por_fecha(self, fecha_str):
        cursor = self.getCursor()
        cursor.execute("""
            SELECT id_menu FROM Menus WHERE fecha = ? AND tipo = 'almuerzo'
        """, (fecha_str,))
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else None
