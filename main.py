
import db
from ui import mostrar_login
"""""
#  Función principal de la aplicación
def main():

    conexion = db.conectar_db()
    if conexion:
        print("Conexión a la base de datos establecida.")

        db.cerrar_conexion(conexion)
    else:
        print("No se pudo conectar a la base de datos.")

"""""
if __name__ == "__main__":
    mostrar_login()
