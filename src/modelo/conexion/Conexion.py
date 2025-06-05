import jaydebeapi

class Conexion:
    _instancia = None

    def __new__(cls, host='localhost', database='menule', user='root', password='Liverpool.840'):
        if cls._instancia is None:
            cls._instancia = super(Conexion, cls).__new__(cls)
            cls._instancia._host = host
            cls._instancia._database = database
            cls._instancia._user = user
            cls._instancia._password = password
            cls._instancia.conexion = cls._instancia.createConnection()
        return cls._instancia

    def createConnection(self):
        try:
            jdbc_driver = "com.mysql.cj.jdbc.Driver"
            jar_file = "lib/mysql-connector-j-9.2.0.jar"
            self.conexion = jaydebeapi.connect(
                jdbc_driver,
                f"jdbc:mysql://{self._host}/{self._database}",
                [self._user, self._password],
                jar_file
            )
            return self.conexion
        except Exception as e:
            print("Error creando conexión:", e)
            return None

    def getCursor(self):
        if self.conexion is None:
            self.createConnection()
        return self.conexion.cursor()

    def closeConnection(self):
        try:
            if self.conexion:
                self.conexion.close()
                self.conexion = None
        except Exception as e:
            print("Error cerrando conexión:", e)

if __name__ == "__main__":
    conexion = Conexion()
    cursor = conexion.getCursor()
    
    if cursor:
        cursor.execute("SELECT DATABASE();")
        print("Base de datos seleccionada:", cursor.fetchone()[0])
        conexion.closeConnection()
    else:
        print("No se pudo obtener el cursor.")