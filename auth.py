
import sqlite3

# Conecta a la base de datos.
def conectar_db():
    try:
        conexion = sqlite3.connect('db/data.db')
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

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
