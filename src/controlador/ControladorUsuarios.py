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
        if not user_vo:
            return False, "No se pudo encontrar la información del usuario."

        # --- BLINDAJE CRIPTOGRÁFICO ---
        contrasena_guardada = user_vo.contrasena if user_vo.contrasena else ""
        es_valida = False

        if contrasena_guardada == "":
            es_valida = True
        elif contrasena_guardada.startswith(('$2a$', '$2b$', '$2y$')):
            try:
                es_valida = bcrypt.checkpw(actual.encode(), contrasena_guardada.encode())
            except ValueError:
                es_valida = False
        else:
            es_valida = (actual == contrasena_guardada)

        if not es_valida:
            return False, "La contraseña actual no es válida."

        try:
            # 1. Generamos el hash seguro de la nueva contraseña con Bcrypt
            nueva_hash = bcrypt.hashpw(nueva.encode(), bcrypt.gensalt()).decode()
            
            # 2. LLAMADA FORMAL MVC
            # Invocamos al método que acabamos de crear en LogicaUsuario
            exito = self._modelo.usuario_service.actualizar_contrasena_usuario(usuario.idUser, nueva_hash)
            
            if exito:
                # Sincronizamos el objeto usuario en la sesión actual
                usuario.contrasena = nueva_hash
                return True, "Contraseña actualizada correctamente."
            else:
                return False, "Error al actualizar la contraseña en el sistema de persistencia."
                
        except Exception as e:
            print("Error en el proceso de guardado de contraseña:", e)
            return False, "Ocurrió un problema interno al procesar los datos."