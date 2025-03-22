import tkinter as tk
import db

def ejecutar_esquema_ui():
    conexion = db.conectar_db()
    if conexion:
        db.ejecutar_esquema(conexion)
        db.cerrar_conexion(conexion)
        resultado_label.config(text="Esquema ejecutado.")

# Implementa la interfaz de login.
def mostrar_login():
    ventana = tk.Tk()
    ventana.title("Sistema de Viajes")

    ejecutar_esquema_button = tk.Button(ventana, text="Ejecutar Esquema", command=ejecutar_esquema_ui)
    ejecutar_esquema_button.pack()

    insertar_usuario_button = tk.Button(ventana, text="Insertar Usuario", command=insertar_usuario_ui)
    insertar_usuario_button.pack()

    consultar_usuarios_button = tk.Button(ventana, text="Consultar Usuarios", command=consultar_usuarios_ui)
    consultar_usuarios_button.pack()

    resultado_label = tk.Label(ventana, text="")
    resultado_label.pack()

    ventana.mainloop()
