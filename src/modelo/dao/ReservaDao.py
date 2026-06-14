# src/modelo/dao/ReservaDao.py
from src.modelo.conexion.Conexion import Conexion
from datetime import datetime
from src.modelo.vo.ReservaVo import ReservaVo

class ReservaDao:
    def getCursor(self):
        return Conexion().getCursor()

    def insert(self, reservaVO):
        cursor = self.getCursor()
        connection = None
        try:
            if hasattr(cursor, '_connection'):
                connection = cursor._connection
            elif hasattr(cursor, 'connection'):
                connection = cursor.connection

            cursor.execute("""
                INSERT INTO Reservas (id_usuario, id_menu, fecha_reserva, estado)
                VALUES (?, ?, ?, ?)
            """, (
                reservaVO.id_usuario,
                reservaVO.id_menu,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                reservaVO.estado
            ))
            
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_id = cursor.fetchone()[0]
            
            if connection:
                try: connection.commit()
                except Exception: pass
            return last_id
        except Exception as e:
            print("Error al crear reserva:", e)
            if connection:
                try: connection.rollback()
                except Exception: pass
            return None
        finally:
            try: cursor.close()
            except Exception: pass

    def obtener_ultima_reserva_id(self, id_usuario):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT id_reserva FROM Reservas 
                WHERE id_usuario = ? 
                ORDER BY fecha_reserva DESC LIMIT 1
            """, (id_usuario,))
            row = cursor.fetchone()
            if row:
                # Asegurar conversión limpia si Java devuelve BigInteger
                return int(str(row[0]))
            return None
        except Exception as e:
            print("Error al obtener última reserva:", e)
            return None
        finally:
            try: cursor.close()
            except Exception: pass
        
    def crear_reserva_anonima(self, fecha, primero, segundo, postre):
        cursor = self.getCursor()
        connection = None
        try:
            if hasattr(cursor, '_connection'):
                connection = cursor._connection
            elif hasattr(cursor, 'connection'):
                connection = cursor.connection

            cursor.execute("SELECT id_menu FROM Menus WHERE fecha = ?", (fecha,))
            menu_row = cursor.fetchone()
            if not menu_row:
                return None
            id_menu = menu_row[0]

            cursor.execute("""
                INSERT INTO Reservas (id_usuario, id_menu, fecha_reserva, estado)
                VALUES (0, ?, NOW(), 'pendiente')
            """, (id_menu,))
            
            cursor.execute("SELECT LAST_INSERT_ID()")
            id_reserva = cursor.fetchone()[0]

            for plato_nombre in [primero, segundo, postre]:
                cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (plato_nombre,))
                plato_row = cursor.fetchone()
                if plato_row:
                    id_plato = plato_row[0]
                    cursor.execute("INSERT INTO ReservaPlatos (id_reserva, id_plato) VALUES (?, ?)", (id_reserva, id_plato))

            if connection:
                try: connection.commit()
                except Exception: pass
            return int(str(id_reserva))
        except Exception as e:
            print("Error al crear reserva anónima:", e)
            if connection:
                try: connection.rollback()
                except Exception: pass
            return None
        finally:
            try: cursor.close()
            except Exception: pass
    
    def crear_reserva_completa_por_fecha(self, id_usuario, fecha, primero, segundo, postre):
        cursor = self.getCursor()
        connection = None
        
        if hasattr(cursor, '_connection'):
            connection = cursor._connection
        elif hasattr(cursor, 'connection'):
            connection = cursor.connection

        try:
            # 1. Buscar el id del menú correspondiente a la fecha
            cursor.execute("SELECT id_menu FROM Menus WHERE fecha = ? AND tipo = 'almuerzo'", (fecha,))
            row = cursor.fetchone()
            if not row:
                print(f"⚠️ No hay menú disponible para la fecha {fecha}")
                return None
            id_menu = row[0]

            # 2. Insertar la Reserva principal
            cursor.execute("""
                INSERT INTO Reservas (id_usuario, id_menu, fecha_reserva, estado)
                VALUES (?, ?, NOW(), 'confirmada')
            """, (id_usuario, id_menu))
            
            cursor.execute("SELECT LAST_INSERT_ID()")
            id_reserva = cursor.fetchone()[0]

            # 3. Vincular los platos seleccionados en la tabla intermedia correcta: ReservaPlatos
            for nombre_plato in [primero, segundo, postre]:
                cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (nombre_plato,))
                plato_row = cursor.fetchone()
                if plato_row:
                    id_plato = plato_row[0]
                    cursor.execute("""
                        INSERT INTO ReservaPlatos (id_reserva, id_plato)
                        VALUES (?, ?)
                    """, (id_reserva, id_plato))

            if connection:
                try: connection.commit()
                except Exception: pass

            # Retornamos convirtiendo explícitamente a través de string para disolver el BigInteger de Java
            return int(str(id_reserva))

        except Exception as e:
            print("Error al crear reserva completa por fecha:", e)
            if connection:
                try: connection.rollback()
                except Exception: pass
            return None
        finally:
            try: cursor.close()
            except Exception: pass
            
    def get_all(self):
        cursor = self.getCursor()
        try:
            cursor.execute("SELECT * FROM Reservas")
            rows = cursor.fetchall()
            return [ReservaVo(*row) for row in rows]
        except Exception as e:
            print("Error al obtener todas las reservas:", e)
            return []
        finally:
            try: cursor.close()
            except Exception: pass

    def obtener_platos_de_reserva(self, id_reserva):
        cursor = self.getCursor()
        try:
            # Desarmar BigInteger/dict preventivo
            if isinstance(id_reserva, dict):
                id_reserva = id_reserva.get('id_reserva', id_reserva.get('id', 0))
            id_reserva_limpio = int(str(id_reserva))

            cursor.execute("""
                SELECT p.nombre
                FROM ReservaPlatos rp
                JOIN Platos p ON rp.id_plato = p.id_plato
                WHERE rp.id_reserva = ?
            """, (id_reserva_limpio,))
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            print("Error al obtener platos de la reserva:", e)
            return []
        finally:
            try: cursor.close()
            except Exception: pass

    def listar_reservas(self):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT id_reserva, id_usuario, id_menu, fecha_reserva, estado
                FROM Reservas
                ORDER BY id_reserva asc
            """)
            reservas = []
            for row in cursor.fetchall():
                id_reserva, id_usuario, id_menu, fecha_reserva, estado = row
                reserva = ReservaVo(
                    id_reserva=int(str(id_reserva)),
                    id_usuario=id_usuario,
                    id_menu=id_menu,
                    fecha_reserva=fecha_reserva,
                    estado=estado,
                )
                reservas.append(reserva)
            return reservas
        except Exception as e:
            print("Error al listar reservas:", e)
            return []
        finally:
            try: cursor.close()
            except Exception: pass

    def obtener_por_usuario(self, id_usuario):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT id_reserva, id_usuario, id_menu, fecha_reserva, estado
                FROM Reservas
                WHERE id_usuario = ?
                ORDER BY id_reserva asc
            """, (id_usuario,))
            reservas = []
            for row in cursor.fetchall():
                id_reserva, id_usuario, id_menu, fecha_reserva, estado = row
                reserva = ReservaVo(
                    id_reserva=int(str(id_reserva)),
                    id_usuario=id_usuario,
                    id_menu=id_menu,
                    fecha_reserva=fecha_reserva,
                    estado=estado,
                )
                reservas.append(reserva)
            return reservas
        except Exception as e:
            print("Error al obtener por usuario:", e)
            return []
        finally:
            try: cursor.close()
            except Exception: pass
    
    def obtener_reservas_confirmadas(self):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT r.id_reserva, r.fecha_reserva, u.email,
                    GROUP_CONCAT(p.nombre, ', ') AS platos
                FROM Reservas r
                JOIN Usuarios u ON r.id_usuario = u.id_usuario
                JOIN ReservaPlatos rp ON r.id_reserva = rp.id_reserva
                JOIN Platos p ON rp.id_plato = p.id_plato
                WHERE r.estado = 'confirmada'
                GROUP BY r.id_reserva
                ORDER BY r.fecha_reserva DESC
            """)
            resultado = cursor.fetchall()
            return resultado
        except Exception as e:
            print("Error al obtener reservas confirmadas:", e)
            return []
        finally:
            try: cursor.close()
            except Exception: pass

    def obtener_reservas_con_detalle(self, estados=('confirmada', 'pendiente')):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT r.id_reserva, r.fecha_reserva, u.email,
                    GROUP_CONCAT(p.nombre, ', ') as menu,
                    r.estado_bit
                FROM Reservas r
                JOIN Usuarios u ON r.id_usuario = u.id_usuario
                JOIN ReservaPlatos rp ON r.id_reserva = rp.id_reserva
                JOIN Platos p ON rp.id_plato = p.id_plato
                WHERE r.estado IN ({})
                GROUP BY r.id_reserva
                ORDER BY r.fecha_reserva DESC
            """.format(','.join(['?']*len(estados))), estados)
            rows = cursor.fetchall()
            return [
                {
                    'id_reserva': int(str(row[0])),
                    'fecha': row[1],
                    'correo': row[2],
                    'menu': row[3],
                    'estado_bit': row[4]
                }
                for row in rows
            ]
        except Exception as e:
            print("Error al obtener reservas con detalle:", e)
            return []
        finally:
            try: cursor.close()
            except Exception: pass

    def actualizar_estado_reserva(self, id_reserva, bit):
        cursor = self.getCursor()
        connection = None
        try:
            if hasattr(cursor, '_connection'):
                connection = cursor._connection
            elif hasattr(cursor, 'connection'):
                connection = cursor.connection

            if isinstance(id_reserva, dict):
                id_reserva = id_reserva.get('id_reserva', id_reserva.get('id', 0))
            id_reserva_limpio = int(str(id_reserva))

            cursor.execute("UPDATE Reservas SET estado_bit = ? WHERE id_reserva = ?", (bit, id_reserva_limpio))
            
            if connection:
                try: connection.commit()
                except Exception: pass
        except Exception as e:
            print("Error al actualizar estado de la reserva:", e)
            if connection:
                try: connection.rollback()
                except Exception: pass
        finally:
            try: cursor.close()
            except Exception: pass

    def es_reserva_de_visitante(self, id_reserva):
        if isinstance(id_reserva, dict):
            id_reserva = id_reserva.get('id_reserva', id_reserva.get('id', 0))
        
        # --- EL ARREGLO MAESTRO ---
        # Primero forzamos a String de Python, rompiendo el BigInteger de Java, 
        # y luego realizamos el casting a int() de forma 100% compatible.
        id_reserva_limpio = int(str(id_reserva))
        
        cursor = self.getCursor()
        try:
            cursor.execute("SELECT id_usuario FROM Reservas WHERE id_reserva = ?", (id_reserva_limpio,))
            row = cursor.fetchone()
            return row and (row[0] == 0 or row[0] is None)
        except Exception as e:
            print("Error al comprobar visitante:", e)
            return False
        finally:
            try: cursor.close()
            except Exception: pass