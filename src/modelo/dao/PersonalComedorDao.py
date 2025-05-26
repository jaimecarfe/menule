from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.PersonalComedorVo import PersonalComedorVo

class PersonalComedorDao(Conexion):
    SQL_INSERT = """
        INSERT INTO PersonalComedor(id_usuario, fecha_contratacion, especialidad)
        VALUES (?, ?, ?)
    """

    def insert(self, personal: PersonalComedorVo):
        cursor = self.getCursor()
        cursor.execute(self.SQL_INSERT, (
            personal.id_usuario,
            personal.fecha_contratacion,
            personal.especialidad
        ))
