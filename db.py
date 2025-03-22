
import sqlite3

# Conecta a la base de datos data.db.
def conectar_db():
    try:
        conexion = sqlite3.connect('db/data.db')
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Ejecuta el esquema de la base de datos.
def ejecutar_esquema(conexion):
    try:
        with open('db/schema.sql', 'r') as archivo_sql:
            esquema = archivo_sql.read()
            with conexion:
                cursor = conexion.cursor()
                cursor.executescript(esquema)
        print("Esquema ejecutado correctamente.")
    except FileNotFoundError:
        print("Error: El archivo schema.sql no existe.")
    except sqlite3.Error as e:
        print(f"Error al ejecutar el esquema: {e}")

# Ejecuta una consulta SQL.
def ejecutar_query(conexion, query, parametros=()):
    try:
        with conexion:
            cursor = conexion.cursor()
            cursor.execute(query, parametros)
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()  # Devuelve los resultados para consultas SELECT
            else:
                return cursor.rowcount  # Devuelve el número de filas afectadas para INSERT, UPDATE, DELETE
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None