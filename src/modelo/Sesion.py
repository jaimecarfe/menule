class Sesion:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Sesion, cls).__new__(cls)
            cls._instancia.usuario = None
        return cls._instancia

    def set_usuario(self, usuario):
        self.usuario = usuario

    def get_usuario(self):
        return self.usuario

    def cerrar_sesion(self):
        self.usuario = None