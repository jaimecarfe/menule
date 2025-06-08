import subprocess

def exportar_base_de_datos(ruta_destino, usuario="root", password="Liverpool.840", nombre_bd="menule", host="localhost"):
    comando = [
        "mysqldump",
        f"-u{usuario}",
        f"-p{password}",
        "-h", host,
        nombre_bd
    ]
    with open(ruta_destino, "w") as salida:
        resultado = subprocess.run(comando, stdout=salida, stderr=subprocess.PIPE, text=True)
    return resultado
