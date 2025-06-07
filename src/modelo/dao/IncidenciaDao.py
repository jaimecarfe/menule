from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.IncidenciaVo import IncidenciaVo
from datetime import date
class IncidenciaDao:
    def __init__(self):
        self.conexion = Conexion()

    def insertar_incidencia(self, incidencia: IncidenciaVo):
        cursor = self.conexion.getCursor()
        cursor.execute('''
            INSERT INTO incidencias (id_usuario, titulo, descripcion, fecha_reporte, estado, numero_seguimiento)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (incidencia.id, incidencia.titulo, incidencia.descripcion,
              incidencia.fecha, incidencia.estado, incidencia.numero_seguimiento))
        cursor.close()

    def obtener_todas(self):
        cursor = self.conexion.getCursor()
        cursor.execute("SELECT id_incidencia, titulo, descripcion, fecha_reporte, estado, prioridad, id_usuario FROM incidencias")
        filas = cursor.fetchall()
        cursor.close()
        resultado = []
        for fila in filas:
            incidencia = IncidenciaVo(
                id=fila[0],
                titulo=fila[1],
                descripcion=fila[2],
                fecha=fila[3],
                estado=fila[4],
                numero_seguimiento=None,
                correo=self.obtener_correo_usuario(fila[6])
            )
            resultado.append(incidencia)
        return resultado

    def obtener_correo_usuario(self, id_usuario):
        from src.modelo.dao.UserDao import UserDao
        user_dao = UserDao()
        user = user_dao.get_by_id(id_usuario)
        return user.correo if user else "Desconocido"

    def actualizar_estado(self, id_incidencia, nuevo_estado):
        cursor = self.conexion.getCursor()
        cursor.execute("UPDATE incidencias SET estado = ? WHERE id_incidencia = ?", (nuevo_estado, id_incidencia))
        #self.conexion.conexion.commit()
        cursor.close()

    def guardar_respuesta(self, id_incidencia, respuesta, fecha):
        fecha_str = fecha.strftime("%Y-%m-%d") 

        cursor = self.conexion.getCursor()
        query = """
        UPDATE Incidencias
        SET solucion = ?, fecha_resolucion = ?, estado = 'resuelta'
        WHERE id_incidencia = ?
        """
        cursor.execute(query, (respuesta, fecha_str, id_incidencia))
