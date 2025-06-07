from src.modelo.BussinessObject import BussinessObject
import bcrypt

class ControladorUsuarios:
    def __init__(self):
        self._modelo = BussinessObject()

    def listar_usuarios(self):
        return self._modelo.usuario_service.listar_usuarios()

    def eliminar_usuario(self, user_id):
        return self._modelo.usuario_service.eliminar_usuario_fisico(user_id)

    def dar_de_baja_usuario(self, user_id):
        return self._modelo.usuario_service.dar_de_baja_usuario(user_id)

    def actualizar_usuario(self, id_usuario, campo, nuevo_valor):
        return self._modelo.usuario_service.actualizar_usuario(id_usuario, campo, nuevo_valor)

    def cambiar_contrasena(self, usuario, actual, nueva, repetir):
        if not actual or not nueva or not repetir:
            return False, "Todos los campos son obligatorios."

        if nueva != repetir:
            return False, "Las contraseñas nuevas no coinciden."

        user_vo = self._modelo.usuario_service.obtener_usuario_por_id(usuario.idUser)

        if not bcrypt.checkpw(actual.encode(), user_vo.contrasena.encode()):
            return False, "La contraseña actual no es válida."

        nueva_hash = bcrypt.hashpw(nueva.encode(), bcrypt.gensalt()).decode()
        exito = self._modelo.usuario_service.actualizar_usuario(usuario.idUser, "contrasena", nueva_hash)
        return exito, "Contraseña actualizada correctamente." if exito else "Error al actualizar contraseña."