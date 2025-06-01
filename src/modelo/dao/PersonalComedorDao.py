from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.PersonalComedorVo import PersonalComedorVo
import datetime

class PersonalComedorDao(Conexion):
    SQL_INSERT = """
        INSERT INTO PersonalComedor(id_usuario, fecha_contratacion, especialidad)
        VALUES (?, ?, ?)
    """

    def insert(self, personal: PersonalComedorVo):
        cursor = self.getCursor()
        fecha_contratacion = personal.fecha_contratacion
        if isinstance(fecha_contratacion, (datetime.date, datetime.datetime)):
            fecha_contratacion = fecha_contratacion.strftime('%Y-%m-%d')
        cursor.execute(self.SQL_INSERT, (
            personal.id_usuario,
            fecha_contratacion,
            personal.especialidad
        ))