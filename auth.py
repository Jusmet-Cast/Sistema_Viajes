import tkinter as tk
from tkinter import messagebox
import sqlite3

#   Conecta a la base de datos.
def conectar_db():
    try:
        conexion = sqlite3.connect('db/data.db')
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

#   Verifica las credenciales del usuario en la base de datos.
def verificar_credenciales(email, password):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE email = ? AND password = ?", (email, password))
        usuario = cursor.fetchone()
        conexion.close()
        return usuario
    return None

#   Implementa la interfaz de login.
def login():
    ventana = tk.Tk()
    ventana.title("Login")

    tk.Label(ventana, text="Email:").grid(row=0, column=0, padx=10, pady=10)
    email_entry = tk.Entry(ventana, width=30)
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(ventana, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(ventana, width=30, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    #   Verifica las credenciales.
    def iniciar_sesion():
        email = email_entry.get().lower()
        password = password_entry.get()
        usuario = verificar_credenciales(email, password)
        if usuario:
            messagebox.showinfo("Éxito", f"Bienvenido, {usuario[1]} (Rol: {usuario[4]})")
            ventana.destroy()
            # Aquí iría la lógica para abrir la siguiente ventana de la aplicación
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    login_button = tk.Button(ventana, text="Iniciar Sesión", command=iniciar_sesion)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    ventana.mainloop()


if __name__ == "__main__":
    login()
