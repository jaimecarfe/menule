from src.modelo.conexion.Conexion import Conexion
from datetime import datetime
from src.modelo.vo.ReservaVo import ReservaVo

class ReservaDao:
    def getCursor(self):
        return Conexion().getCursor()

    def insert(self, reservaVO):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                INSERT INTO Reservas (id_usuario, id_menu, fecha_reserva, estado)
                VALUES (?, ?, ?, ?)
            """, (
                reservaVO.id_usuario,
                reservaVO.id_menu,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                reservaVO.estado
            ))
            # Obtener el último ID insertado con JayDeBeApi/MySQL
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_id = cursor.fetchone()[0]
            cursor.close()
            return last_id
        except Exception as e:
            print("Error al crear reserva:", e)
            try:
                cursor.close()
            except Exception:
                pass
            return None

    def obtener_ultima_reserva_id(self, id_usuario):
        cursor = self.getCursor()
        try:
            cursor.execute("""
                SELECT id_reserva FROM Reservas 
                WHERE id_usuario = ? 
                ORDER BY fecha_reserva DESC LIMIT 1
            """, (id_usuario,))
            row = cursor.fetchone()
            cursor.close()
            return row[0] if row else None
        except Exception as e:
            print("Error al obtener última reserva:", e)
            try:
                cursor.close()
            except Exception:
                pass
            return None
        
    def crear_reserva_anonima(self, fecha, primero, segundo, postre):
        cursor = self.getCursor()
        try:
            cursor.execute("SELECT id_menu FROM Menus WHERE fecha = ?", (fecha,))
            id_menu = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO Reservas (id_usuario, id_menu, fecha_reserva, estado)
                VALUES (0, ?, NOW(), 'pendiente')
            """, (id_menu,))
            cursor.execute("SELECT LAST_INSERT_ID()")
            id_reserva = cursor.fetchone()[0]

            for plato_nombre in [primero, segundo, postre]:
                cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (plato_nombre,))
                id_plato = cursor.fetchone()[0]
                cursor.execute("INSERT INTO ReservaPlatos (id_reserva, id_plato) VALUES (?, ?)", (id_reserva, id_plato))

            return id_reserva
        except Exception as e:
            print("Error al crear reserva anónima:", e)
            return None

    def crear_reserva_completa_por_fecha(self, id_usuario, fecha, primero, segundo, postre):
        cursor = self.getCursor()
        try:
            cursor.execute("SELECT id_menu FROM Menus WHERE fecha = ?", (fecha,))
            id_menu = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO Reservas (id_usuario, id_menu, fecha_reserva, estado)
                VALUES (?, ?, NOW(), 'pendiente')
            """, (id_usuario, id_menu))
            cursor.execute("SELECT LAST_INSERT_ID()")
            id_reserva = cursor.fetchone()[0]

            for plato_nombre in [primero, segundo, postre]:
                cursor.execute("SELECT id_plato FROM Platos WHERE nombre = ?", (plato_nombre,))
                id_plato = cursor.fetchone()[0]
                cursor.execute("INSERT INTO ReservaPlatos (id_reserva, id_plato) VALUES (?, ?)", (id_reserva, id_plato))

            return id_reserva
        except Exception as e:
            print("Error al crear reserva completa por fecha:", e)
            return None    

    def get_all(self):
        cursor = self.getCursor()
        try:
            cursor.execute("SELECT * FROM Reservas")
            rows = cursor.fetchall()
            return [ReservaVo(*row) for row in rows]
        finally:
            cursor.close()

    def obtener_platos_de_reserva(self, id_reserva):
        cursor = self.getCursor()
        cursor.execute("""
            SELECT p.nombre
            FROM ReservaPlatos rp
            JOIN Platos p ON rp.id_plato = p.id_plato
            WHERE rp.id_reserva = ?
        """, (id_reserva,))
        rows = cursor.fetchall()
        cursor.close()
        return [row[0] for row in rows]

    def listar_reservas(self):
        cursor = self.getCursor()
        cursor.execute("""
            SELECT id_reserva, id_usuario, id_menu, fecha_reserva, estado
            FROM Reservas
            ORDER BY id_reserva asc
        """)
        reservas = []
        for row in cursor.fetchall():
            id_reserva, id_usuario, id_menu, fecha_reserva, estado = row
            reserva = ReservaVo(
                id_reserva=id_reserva,
                id_usuario=id_usuario,
                id_menu=id_menu,
                fecha_reserva=fecha_reserva,
                estado=estado,
            )
            reservas.append(reserva)
        return reservas

    def obtener_por_usuario(self, id_usuario):
        cursor = self.getCursor()
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
                id_reserva=id_reserva,
                id_usuario=id_usuario,
                id_menu=id_menu,
                fecha_reserva=fecha_reserva,
                estado=estado,
            )
            reservas.append(reserva)
        return reservas
    
    def obtener_reservas_confirmadas(self):
        cursor = self.getCursor()
        cursor.execute("""
            SELECT r.id_reserva, r.fecha_reserva, u.email,
                GROUP_CONCAT(p.nombre, ', ') AS platos
            FROM Reservas r
            JOIN Usuarios u ON r.id_usuario = u.id_usuario
            JOIN MenuPlatos mp ON r.id_menu = mp.id_menu
            JOIN Platos p ON mp.id_plato = p.id_plato
            WHERE r.estado = 'confirmada'
            GROUP BY r.id_reserva
            ORDER BY r.fecha_reserva DESC
        """)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado

    def obtener_reservas_con_detalle(self, estados=('confirmada', 'pendiente')):
        cursor = self.getCursor()
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
        cursor.close()
        return [
            {
                'id_reserva': row[0],
                'fecha': row[1],
                'correo': row[2],
                'menu': row[3],
                'estado_bit': row[4]
            }
            for row in rows
        ]

    def actualizar_estado_reserva(self, id_reserva, bit):
        cursor = self.getCursor()
        cursor.execute("UPDATE Reservas SET estado_bit = ? WHERE id_reserva = ?", (bit, id_reserva))
        cursor.close()