from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.EstudianteVo import EstudianteVo

class EstudianteDao(Conexion):
    SQL_INSERT = """
        INSERT INTO Estudiantes(id_usuario, grado_academico, tui_numero, saldo)
        VALUES (?, ?, ?, ?)
    """
    SQL_GET_SALDO = "SELECT saldo FROM Estudiantes WHERE id_usuario = ?"
    SQL_UPDATE_SALDO = "UPDATE Estudiantes SET saldo = ? WHERE id_usuario = ?"

    def insert(self, estudiante: EstudianteVo):
        cursor = self.getCursor()
        try:
            cursor.execute(self.SQL_INSERT, (
                estudiante.id_usuario,
                estudiante.grado_academico,
                estudiante.tui_numero,
                estudiante.saldo
            ))
            return True
        except Exception as e:
            print("Error insertando estudiante:", e)
            return False
    
    def obtener_saldo(self, id_usuario):
        cursor = self.getCursor()
        cursor.execute(self.SQL_GET_SALDO, (id_usuario,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0.0

    def actualizar_saldo(self, id_usuario, nuevo_saldo):
        cursor = self.getCursor()
        cursor.execute(self.SQL_UPDATE_SALDO, (nuevo_saldo, id_usuario))
        return cursor.rowcount > 0
