
import tkinter as tk
from tkinter import messagebox
from auth import verificar_credenciales

# Implementa la interfaz de login.
def mostrar_login():
    ventana = tk.Tk()
    ventana.title("Login")

    # Centrar la ventana en la pantalla
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
