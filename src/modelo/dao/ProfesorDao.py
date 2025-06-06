from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.ProfesorVo import ProfesorVo

class ProfesorDao(Conexion):
    SQL_INSERT = """
        INSERT INTO Profesores(id_usuario, grado_academico, tui_numero, saldo)
        VALUES (?, ?, ?, ?)
    """
    SQL_GET_SALDO = "SELECT saldo FROM Profesores WHERE id_usuario = ?"
    SQL_UPDATE_SALDO = "UPDATE Profesores SET saldo = ? WHERE id_usuario = ?"

    def insert(self, profesor: ProfesorVo):
        cursor = self.getCursor()
        cursor.execute(self.SQL_INSERT, (
            profesor.id_usuario,
            profesor.grado_academico,
            profesor.tui_numero,
            profesor.saldo
        ))

    def actualizar_saldo(self, id_usuario, nuevo_saldo):
        cursor = self.getCursor()
        cursor.execute(self.SQL_UPDATE_SALDO, (nuevo_saldo, id_usuario))
        return cursor.rowcount > 0
