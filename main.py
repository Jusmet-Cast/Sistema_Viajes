
import db
from ui import mostrar_login

#  Función principal de la aplicación
def main():
    if db.conectar_db():  # Verificar si la conexión se establece correctamente.
        print("Conexión a la base de datos establecida.")
        db.ejecutar_esquema()  # Ejecutar el esquema de la base de datos.
    else:
        print("No se pudo conectar a la base de datos.")


if __name__ == "__main__":
    main()
    mostrar_login()
