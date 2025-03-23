
import sqlite3
# from db import conectar_db


# Verifica las credenciales del usuario en la base de datos.
def verificar_credenciales(email, password):
    try:
        with sqlite3.connect('db/data.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Usuario WHERE email = ? AND password = ?", (email, password))
            usuario = cursor.fetchone()
            return usuario
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
