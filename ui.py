import tkinter as tk
import db

def ejecutar_esquema_ui():
    conexion = db.conectar_db()
    if conexion:
        db.ejecutar_esquema(conexion)
        db.cerrar_conexion(conexion)
        resultado_label.config(text="Esquema ejecutado.")

def insertar_usuario_ui():
    conexion = db.conectar_db()
    if conexion:
        db.ejecutar_query(conexion, "INSERT INTO Usuario (nombre, email, password, rol) VALUES (?, ?, ?, ?)", ("Usuario de prueba", "prueba@email.com", "password123", "Gerente de tienda"))
        db.cerrar_conexion(conexion)
        resultado_label.config(text="Usuario insertado.")

def consultar_usuarios_ui():
    conexion = db.conectar_db()
    if conexion:
        cursor = db.ejecutar_query(conexion, "SELECT * FROM Usuario")
        if cursor:
            resultados = db.obtener_resultados(cursor)
            resultado_label.config(text=str(resultados))
        db.cerrar_conexion(conexion)

def crear_ventana_principal():
    global resultado_label  # Para poder modificar la etiqueta desde las funciones
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
