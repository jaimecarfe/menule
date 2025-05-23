from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.EstudianteVo import EstudianteVo

class EstudianteDao(Conexion):
    SQL_INSERT = """
        INSERT INTO Estudiantes(id_usuario, grado_academico, tui_numero, saldo)
        VALUES (?, ?, ?, ?)
    """

    def insert(self, estudiante: EstudianteVo):
        cursor = self.getCursor()
        cursor.execute(self.SQL_INSERT, (
            estudiante.id_usuario,
            estudiante.grado_academico,
            estudiante.tui_numero,
            estudiante.saldo
        ))
        self.conexion.commit()