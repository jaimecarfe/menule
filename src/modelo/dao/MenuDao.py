# src/modelo/dao/MenuDao.py
from src.modelo.conexion.Conexion import Conexion

class MenuDao:
    def getCursor(self):
        return Conexion().getCursor()

    def insertar_o_modificar_menu_con_tipo(self, fecha, lista_platos_con_tipo):
        """
        Inserta o actualiza un menú y sus platos clasificados por tipo.
        :param fecha: Objeto datetime.date o str 'YYYY-MM-DD'
        :param lista_platos_con_tipo: lista de tuplas (nombre_plato, tipo)
        """
        cursor = self.getCursor()
        connection = None
        try:
            if hasattr(cursor, '_connection'):
                connection = cursor._connection
            elif hasattr(cursor, 'connection'):
                connection = cursor.connection

            # Forzar formato string limpio para MySQL DATE
            fecha_str = fecha.strftime('%Y-%m-%d') if hasattr(fecha, 'strftime') else str(fecha)

            try:
                cursor.execute("""
                    INSERT INTO Menus (fecha, tipo, max_reservas, disponible)
                    VALUES (?, 'almuerzo', 100, 1)
                """, (fecha_str,))
            except Exception:
                cursor.execute("""
                    UPDATE Menus SET disponible = 1 WHERE fecha = ? AND tipo = 'almuerzo'
                """, (fecha_str,))

            cursor.execute("SELECT id_menu FROM Menus WHERE fecha = ? AND tipo = 'almuerzo'", (fecha_str,))
            result = cursor.fetchone()
            if not result:
                print("No se pudo obtener el menú para la fecha:", fecha_str)
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
                        INSERT INTO Platos (nombre, tipo)
                        VALUES (?, ?)
                    """, (nombre, tipo))

                    cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (nombre,))
                    id_plato = cursor.fetchone()[0]

                cursor.execute("INSERT INTO MenuPlatos (id_menu, id_plato) VALUES (?, ?)", (id_menu, id_plato))

            if connection:
                connection.commit()
            return True

        except Exception as e:
            print("Error al modificar menú:", e)
            if connection:
                try: connection.rollback()
                except Exception: pass
            return False
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    def obtener_platos_por_fecha(self, fecha):
        cursor = self.getCursor()
        try:
            fecha_str = fecha.strftime('%Y-%m-%d') if hasattr(fecha, 'strftime') else str(fecha)
            cursor.execute("""
                SELECT p.nombre, p.tipo, p.alergenos
                FROM Menus m
                JOIN MenuPlatos mp ON m.id_menu = mp.id_menu
                JOIN Platos p ON mp.id_plato = p.id_plato
                WHERE m.fecha = ? AND m.tipo = 'almuerzo'
            """, (fecha_str,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener platos para la fecha {fecha}:", e)
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
    
    def listar_disponibles(self):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT m.id_menu, m.fecha, m.tipo
                FROM Menus m
                WHERE m.disponible = 1
                ORDER BY m.fecha ASC
            """)
            rows = cursor.fetchall()
            return [
                {"id_menu": row[0], "fecha": str(row[1]), "tipo": row[2]}
                for row in rows
            ]
        except Exception as e:
            print("Error al listar menús disponibles:", e)
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
    
    def guardar_menu_con_alergenos(self, fecha, lista_platos):
        cursor = self.getCursor()
        connection = None
        try:
            if hasattr(cursor, '_connection'):
                connection = cursor._connection
            elif hasattr(cursor, 'connection'):
                connection = cursor.connection

            fecha_str = fecha.strftime('%Y-%m-%d') if hasattr(fecha, 'strftime') else str(fecha)

            # Verificar existencia previa manualmente de forma segura
            cursor.execute("SELECT id_menu FROM Menus WHERE fecha = ? AND tipo = 'almuerzo'", (fecha_str,))
            row_menu = cursor.fetchone()
            
            if row_menu:
                id_menu = row_menu[0]
                cursor.execute("UPDATE Menus SET disponible = 1 WHERE id_menu = ?", (id_menu,))
            else:
                cursor.execute("""
                    INSERT INTO Menus (fecha, tipo, max_reservas, disponible)
                    VALUES (?, 'almuerzo', 100, 1)
                """, (fecha_str,))
                cursor.execute("SELECT LAST_INSERT_ID()")
                id_menu = cursor.fetchone()[0]

            cursor.execute("DELETE FROM MenuPlatos WHERE id_menu = ?", (id_menu,))

            for nombre, tipo, alergenos in lista_platos:
                cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (nombre,))
                row = cursor.fetchone()
                if row:
                    id_plato = row[0]
                    cursor.execute("UPDATE Platos SET tipo = ?, alergenos = ? WHERE id_plato = ?", (tipo, alergenos, id_plato))
                else:
                    cursor.execute("INSERT INTO Platos (nombre, tipo, alergenos) VALUES (?, ?, ?)", (nombre, tipo, alergenos))
                    cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (nombre,))
                    id_plato = cursor.fetchone()[0]

                cursor.execute("INSERT INTO MenuPlatos (id_menu, id_plato) VALUES (?, ?)", (id_menu, id_plato))

            if connection:
                connection.commit()
            return True
        except Exception as e:
            print("Error al guardar menú con alérgenos:", e)
            if connection:
                try: connection.rollback()
                except Exception: pass
            return False
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    def obtener_id_menu_por_fecha(self, fecha_str):
        cursor = self.getCursor()
        try:
            # Aseguramos limpieza del string de la fecha
            fecha_limpia = fecha_str.strftime('%Y-%m-%d') if hasattr(fecha_str, 'strftime') else str(fecha_str)
            cursor.execute("""
                SELECT id_menu FROM Menus WHERE fecha = ? AND tipo = 'almuerzo'
            """, (fecha_limpia,))
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print("Error al obtener ID del menú por fecha:", e)
            return None
        finally:
            try:
                cursor.close()
            except Exception:
                pass