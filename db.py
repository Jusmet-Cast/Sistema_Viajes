
import sqlite3


#   Conecta a la base de datos data.db.
def conectar_db():
    try:
        conexion = sqlite3.connect('db/data.db')
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

#   Ejecuta el esquema de la base de datos.
def ejecutar_esquema(conexion):
    try:
        cursor = conexion.cursor()
        with open('db/schema.sql', 'r') as archivo_sql:
            esquema = archivo_sql.read()
            cursor.executescript(esquema)
        conexion.commit()
        print("Esquema ejecutado correctamente.")
    except sqlite3.Error as e:
        print(f"Error al ejecutar el esquema: {e}")


# Ejecuta una consulta SQL.
def ejecutar_query(conexion, query, parametros=()):
    cursor = conexion.cursor()
    try:
        cursor.execute(query, parametros)
        conexion.commit()
        return cursor
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None


#  Obtiene todos los resultados de una consulta.
def obtener_resultados(cursor):
    try:
        resultados = cursor.fetchall()
        return resultados
    except sqlite3.Error as e:
        print(f"Error al obtener los resultados: {e}")
        return None


#   Cierra la conexión a la base de datos.
def cerrar_conexion(conexion):
    try:
        conexion.close()
    except sqlite3.Error as e:
        print(f"Error al cerrar la conexión: {e}")
