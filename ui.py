
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


#  Implementa la interfaz de la ventana para registrar viajes.
def mostrar_registrar_viaje(usuario, ventana_menu):
    ventana_viaje = tk.Toplevel()  # Usar Toplevel para ventanas secundarias
    ventana_viaje.title("Registrar Viaje")

    #  Centrar la ventana en la pantalla.
    ancho_ventana = 300
    alto_ventana = 465  # Aumentamos la altura para acomodar la lista de colaboradores.
    x_pos = (ventana_viaje.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y_pos = (ventana_viaje.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana_viaje.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

    #  Ocultar la ventana del menú principal.
    ventana_menu.withdraw()

    #  Frame principal.
    frame_principal = tk.Frame(ventana_viaje)
    frame_principal.pack(pady=20)

    #  Obtener datos de la base de datos.
    sucursales = ejecutar_query(conectar_db(), "SELECT id, nombre FROM Sucursal")
    transportistas = ejecutar_query(conectar_db(), "SELECT id, nombre FROM Transportista")
    colaboradores = ejecutar_query(conectar_db(), "SELECT id, nombre FROM Colaborador")

    #  Variables para almacenar las selecciones.
    sucursal_seleccionada = tk.StringVar(ventana_viaje)
    transportista_seleccionado = tk.StringVar(ventana_viaje)

    #  Campo para seleccionar sucursal.
    tk.Label(frame_principal, text="Sucursal:").pack(pady=5)
    sucursal_menu = tk.OptionMenu(frame_principal, sucursal_seleccionada, *[f"{s[0]} - {s[1]}" for s in sucursales])
    sucursal_menu.pack(pady=5)

    #  Campo para seleccionar transportista.
    tk.Label(frame_principal, text="Transportista:").pack(pady=5)
    transportista_menu = tk.OptionMenu(frame_principal, transportista_seleccionado,
                                       *[f"{t[0]} - {t[1]}" for t in transportistas])
    transportista_menu.pack(pady=5)

    #  Campo para seleccionar colaboradores (Listbox con selección múltiple).
    tk.Label(frame_principal, text="Colaboradores:").pack(pady=5)
    colaboradores_listbox = tk.Listbox(frame_principal, selectmode=tk.MULTIPLE)
    colaboradores_listbox.pack(pady=5)

    #  Label para mostrar la suma de distancias.
    distancia_label = tk.Label(frame_principal, text="Suma de distancias: 0 km")
    distancia_label.pack(pady=5)

    #  Label para mostrar la tarifa total.
    tarifa_label = tk.Label(frame_principal, text="Tarifa total: L.0.00")
    tarifa_label.pack(pady=5)

    #  Función para actualizar la lista de colaboradores según la sucursal seleccionada.
    def actualizar_colaboradores(*args):
        colaboradores_listbox.delete(0, tk.END)  # Limpiar la lista actual
        if sucursal_seleccionada.get():
            sucursal_id = int(sucursal_seleccionada.get().split(" - ")[0])
            colaboradores_asignados = ejecutar_query(conectar_db(), """
                SELECT c.id, c.nombre 
                FROM Colaborador c
                JOIN AsignacionSucursal a ON c.id = a.colaborador_id
                WHERE a.sucursal_id = ?
            """, (sucursal_id,))
            for colaborador in colaboradores_asignados:
                colaboradores_listbox.insert(tk.END, f"{colaborador[0]} - {colaborador[1]}")

    #  Vincular la función de actualización al cambio de selección de sucursal.
    sucursal_seleccionada.trace("w", actualizar_colaboradores)

    #  Llamar a la función para cargar los colaboradores inicialmente (si hay una sucursal seleccionada por defecto).
    actualizar_colaboradores()

    #  Función para registrar el viaje.
    def guardar_viaje():
        # Validar que se hayan seleccionado todos los campos.
        if not sucursal_seleccionada.get():
            messagebox.showerror("Error", "Debe seleccionar una sucursal.")
            return
        if not transportista_seleccionado.get():
            messagebox.showerror("Error", "Debe seleccionar un transportista.")
            return
        if not colaboradores_listbox.curselection():
            messagebox.showerror("Error", "Debe seleccionar al menos un colaborador.")
            return

        #  Extraer ID's de las selecciones.
        sucursal_id = int(sucursal_seleccionada.get().split(" - ")[0])
        transportista_id = int(transportista_seleccionado.get().split(" - ")[0])
        colaboradores_ids = [int(colaboradores_listbox.get(i).split(" - ")[0]) for i in
                             colaboradores_listbox.curselection()]

        #  Intentar registrar el viaje.
        try:
            if registrar_viaje(usuario[0], sucursal_id, transportista_id, colaboradores_ids):
                messagebox.showinfo("Éxito", "Viaje registrado correctamente.")
                ventana_viaje.destroy()
                ventana_menu.deiconify()  # Mostrar la ventana del menú principal.
            else:
                error_msg = "No se pudo registrar el viaje. Verifique los datos e intente nuevamente."
                messagebox.showerror("Error", error_msg)
                print(f"Error: {error_msg}")  # Imprimir en la terminal.
        except ValueError as e:
            # Capturar errores de validación lanzados por trips.py
            error_msg = str(e)  # Obtener el mensaje de error específico
            messagebox.showerror("Error", error_msg)  # Mostrar el mensaje específico al usuario.
            print(f"Error de validación: {error_msg}")  # Imprimir en la terminal.
        except Exception as e:
            # Capturar otros errores (por ejemplo, errores de la base de datos)
            error_msg = f"Ocurrió un problema al registrar el viaje: {str(e)}"
            messagebox.showerror("Error", error_msg)
            print(f"Error: {error_msg}")  # Imprimir en la terminal.

    tk.Label(frame_principal, text="").pack(pady=10)  # Etiqueta vacía para crear espacio (estética).

    #  Botón para guardar el viaje.
    tk.Button(
        frame_principal,
        text="Guardar Viaje",
        command=guardar_viaje,
        bg="green",
        fg="white"
    ).pack(side=tk.LEFT, padx=10)

    #  Botón para cancelar.
    def cancelar():
        ventana_viaje.destroy()
        ventana_menu.deiconify()  # Mostrar la ventana del menú principal.

    tk.Button(
        frame_principal,
        text="Cancelar",
        command=cancelar,
        bg="red",
        fg="white"
    ).pack(side=tk.LEFT, padx=10)

    #  Bloquear la ventana principal.
    ventana_viaje.grab_set()
    ventana_viaje.focus_set()
    ventana_viaje.wait_window()
