from src.modelo.conexion.Conexion import Conexion

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

            # 1. Insertar o actualizar menú
            cursor.execute("""
                INSERT INTO Menus (fecha, tipo, max_reservas, disponible)
                VALUES (?, 'almuerzo', 100, 1)
                ON DUPLICATE KEY UPDATE disponible = 1
            """, (fecha,))

            # 2. Obtener el id del menú insertado o existente
            cursor.execute("SELECT id_menu FROM Menus WHERE fecha = ?", (fecha,))
            result = cursor.fetchone()
            if not result:
                print("❌ No se pudo obtener el menú para la fecha:", fecha)
                return False

            id_menu = result[0]

            # 3. Eliminar platos anteriores del menú
            cursor.execute("DELETE FROM MenuPlatos WHERE id_menu = ?", (id_menu,))

            # 4. Insertar platos y relacionarlos
            for nombre, tipo in lista_platos_con_tipo:
                cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (nombre,))
                row = cursor.fetchone()

                if row:
                    id_plato = row[0]
                else:
                    # Insertar nuevo plato si no existe
                    cursor.execute("""
                        INSERT INTO Platos (nombre, tipo, precio)
                        VALUES (?, ?, 0.00)
                    """, (nombre, tipo))

                    # Reconsultar el id recién insertado
                    cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (nombre,))
                    id_plato = cursor.fetchone()[0]

                # Relacionar plato con menú
                cursor.execute("INSERT INTO MenuPlatos (id_menu, id_plato) VALUES (?, ?)", (id_menu, id_plato))

            #conn.conexion.commit()
            return True

        except Exception as e:
            print("❌ Error al modificar menú:", e)
            return False

    def obtener_platos_por_fecha(self, fecha):
        cursor = self.getCursor()
        cursor.execute("""
            SELECT p.nombre, p.tipo
            FROM Menus m
            JOIN MenuPlatos mp ON m.id_menu = mp.id_menu
            JOIN Platos p ON mp.id_plato = p.id_plato
            WHERE m.fecha = ?
        """, (fecha,))
        return cursor.fetchall()
