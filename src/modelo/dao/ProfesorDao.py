from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.ProfesorVo import ProfesorVo

class ProfesorDao(Conexion):
    SQL_INSERT = """
        INSERT INTO Profesores(id_usuario, grado_academico, saldo)
        VALUES (?, ?, ?)
    """

    def insert(self, profesor: ProfesorVo):
        cursor = self.getCursor()
        cursor.execute(self.SQL_INSERT, (
            profesor.id_usuario,
            profesor.grado_academico,
            profesor.saldo
        ))
