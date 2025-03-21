import ui
import db
import models

#   Muestra todos los usuarios de la base de datos.
def mostrar_usuarios():
    conexion = db.conectar_db()
    if conexion:
        cursor = db.ejecutar_query(conexion, "SELECT * FROM Usuario")
        if cursor:
            resultados = db.obtener_resultados(cursor)
            for fila in resultados:
                print(fila)  # Imprime cada fila de resultados
            db.cerrar_conexion(conexion)
        else:
            print("Error al ejecutar la consulta.")
    else:
        print("No se pudo conectar a la base de datos.")


#   Función principal de la aplicación
def main():

    conexion = db.conectar_db()
    if conexion:
        print("Conexión a la base de datos establecida.")

        db.cerrar_conexion(conexion)
    else:
        print("No se pudo conectar a la base de datos.")


if __name__ == "__main__":

    mostrar_usuarios()
    main()
