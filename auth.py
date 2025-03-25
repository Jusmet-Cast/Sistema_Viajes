
from db import conectar_db


# Verifica las credenciales del usuario en la base de datos.
def verificar_credenciales(email, password):
    with conectar_db() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE email = ? AND password = ?", (email, password))
        return cursor.fetchone()
