class Registro():
    def __init__(self, id, nombre, apellido, edad, email):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.email = email

    def __str__(self):
        return f'{self.id} {self.nombre} {self.apellido} {self.edad} {self.email}'