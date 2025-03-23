
import tkinter as tk
from tkinter import messagebox
from auth import verificar_credenciales

# Implementa la interfaz de login.
def mostrar_login():
    ventana = tk.Tk()
    ventana.title("Login")

    # Centrar la ventana en la pantalla.
    ancho_ventana = 300
    alto_ventana = 200
    x_pos = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y_pos = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

    tk.Label(ventana, text="Email:").grid(row=0, column=0, padx=10, pady=10)
    email_entry = tk.Entry(ventana, width=30)
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(ventana, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(ventana, width=30, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Verifica las credenciales.
    def iniciar_sesion():
        email = email_entry.get().strip().lower()  # Elimina espacios y convierte a minúsculas
        password = password_entry.get().strip()   # Elimina espacios

        if not email or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        usuario = verificar_credenciales(email, password)
        if usuario:
            messagebox.showinfo("Éxito", f"Bienvenido, {usuario[1]} (Rol: {usuario[4]})")
            ventana.destroy()
            # Aquí iría la lógica para abrir la siguiente ventana de la aplicación
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def salir():
        ventana.destroy()

    login_button = tk.Button(ventana, text="Iniciar Sesión", command=iniciar_sesion)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    salir_button = tk.Button(ventana, text="Salir", command=salir)
    salir_button.grid(row=3, column=0, columnspan=2, pady=10)

    ventana.mainloop()

# Implementa la interfaz del menu principal.
def mostrar_menu_principal(usuario):
    ventana_menu = tk.Tk()
    ventana_menu.title("Menú Principal")

    # Centrar la ventana en la pantalla.
    ancho_ventana = 300
    alto_ventana = 250  # Aumentamos la altura para acomodar más espacio.
    x_pos = (ventana_menu.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y_pos = (ventana_menu.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana_menu.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

    # Mostrar información del usuario.
    tk.Label(ventana_menu, text=f"Bienvenido, {usuario[1]} ").pack(pady=10)

    # Botones para las opciones del menú.
    if usuario[4] == "Gerente de tienda":   # Validación de usuario con rol/perfil "Gerente de tienda".
        tk.Button(ventana_menu, text="Registrar Viaje", command=lambda: print("Registrar Viaje")).pack(pady=5)
        tk.Button(ventana_menu, text="Asignar Sucursal", command=lambda: print("Asignar Sucursal")).pack(pady=5)
        tk.Button(ventana_menu, text="Generar Reportes", command=lambda: print("Generar Reportes")).pack(pady=5)
    else:   # Opciones para otros usuarios.
        tk.Button(ventana_menu, text="Asignar Sucursal", command=lambda: print("Asignar Sucursal")).pack(pady=5)
        tk.Button(ventana_menu, text="Generar Reportes", command=lambda: print("Generar Reportes")).pack(pady=5)

    tk.Label(ventana_menu, text="").pack(pady=10)  # Etiqueta vacía para crear espacio (estética).

    # Frame para agrupar los botones de salida.
    frame_botones_salida = tk.Frame(ventana_menu)
    frame_botones_salida.pack(pady=10)

    # Función para regresar al login.
    def regresar_al_login():
        ventana_menu.destroy()  # Cierra la ventana actual.
        mostrar_login()         # Abre la ventana de login.

    def salir():
        ventana_menu.destroy()

    # Botón para regresar al login.
    tk.Button(
        frame_botones_salida,
        text="Regresar al Login",
        command=regresar_al_login,  # Llama a la función para regresar al login.
        bg="yellow",  # Fondo amarillo.
        fg="black"    # Texto negro.
    ).pack(side=tk.LEFT, padx=10)  # Alineación horizontal con espacio entre botones.

    # Botón de salir.
    tk.Button(
        frame_botones_salida,
        text="Salir",
        command=salir,  # Cierra la aplicación.
        bg="red",     # Fondo rojo.
        fg="white"    # Texto blanco.
    ).pack(side=tk.LEFT, padx=10)  # Alineación horizontal con espacio entre botones.

    ventana_menu.mainloop()
