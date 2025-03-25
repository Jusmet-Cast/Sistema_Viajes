
from tkcalendar import DateEntry
from tkinter import messagebox
import tkinter as tk

#  Librerias locales.
from assignment import asignar_sucursal_a_colaborador, existe_asignacion
from reports import generar_reporte_viajes, calcular_total_a_pagar
from auth import verificar_credenciales
from trips import registrar_viaje
from db import (
    conectar_db,
    ejecutar_query,
    obtener_distancia_sucursal_colaborador
)


#  Implementa la interfaz de login.
def mostrar_login():
    ventana = tk.Tk()
    ventana.title("Login")

    # Centrar la ventana en la pantalla.
    ancho_ventana = 300
    alto_ventana = 200
    x_pos = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y_pos = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

    # Frame principal para organizar los elementos.
    frame_principal = tk.Frame(ventana)
    frame_principal.pack(pady=20)

    # Frame para los campos de entrada.
    frame_campos = tk.Frame(frame_principal)
    frame_campos.pack()

    # Campo de email.
    tk.Label(frame_campos, text="Email:").pack(pady=5)
    email_entry = tk.Entry(frame_campos, width=30)
    email_entry.pack(pady=5)

    # Campo de contraseña.
    tk.Label(frame_campos, text="Password:").pack(pady=5)
    password_entry = tk.Entry(frame_campos, width=30, show="*")
    password_entry.pack(pady=5)

    # Frame para los botones.
    frame_botones = tk.Frame(frame_principal)
    frame_botones.pack(pady=10)

    # Función para verificar credenciales.
    def iniciar_sesion():
        email = email_entry.get().strip().lower()  # Elimina espacios y convierte a minúsculas.
        password = password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        usuario = verificar_credenciales(email, password)
        if usuario:
            messagebox.showinfo("Éxito", f"¡Bienvenido, {usuario[1]}! \n (Perfil: {usuario[4]})")
            ventana.destroy()
            mostrar_menu_principal(usuario)  # Redirigir al menú principal.
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    # Botón de iniciar sesión.
    tk.Button(
        frame_botones,
        text="Iniciar Sesión",
        command=iniciar_sesion,  # Llama a la función para verricar credenciales.
        bg="green",  # Fondo verde.
        fg="white"  # Texto white.
    ).pack(side=tk.LEFT, padx=10)

    # Función para cerrar la ventana y salir.
    def salir():
        ventana.destroy()

    # Botón de salir.
    tk.Button(
        frame_botones,
        text="Salir",
        command=salir,  # Llama a la función para salir.
        bg="red",  # Fondo rojo.
        fg="white"  # Texto blanco.
    ).pack(side=tk.LEFT, padx=10)

    ventana.mainloop()

#  Implementa la interfaz del menu principal.
def mostrar_menu_principal(usuario):
    ventana_menu = tk.Tk()
    ventana_menu.title("Menú Principal")

    # Centrar la ventana en la pantalla.
    ancho_ventana = 300
    alto_ventana = 325
    x_pos = (ventana_menu.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y_pos = (ventana_menu.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana_menu.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

    # Mostrar información del usuario.
    tk.Label(ventana_menu, text=f"¡Bienvenido, {usuario[1]}! \n ¿Qué deseas realizar?").pack(pady=10)
    tk.Label(ventana_menu, text="").pack(pady=7)  # Etiqueta vacía para crear espacio (estética).

    # Botones para las opciones del menú.
    if usuario[4] == "Gerente de tienda":  # Validación de usuario con rol/perfil "Gerente de tienda".
        tk.Button(ventana_menu, text="Registrar Viaje", command=lambda: mostrar_registrar_viaje(usuario, ventana_menu)).pack(pady=5)
        tk.Button(ventana_menu, text="Asignar Sucursal", command=lambda: mostrar_asignar_sucursal(ventana_menu)).pack(pady=5)
        tk.Button(ventana_menu, text="Generar Reportes", command=lambda: mostrar_reporte_viajes(ventana_menu)).pack(pady=5)
    else:  # Opciones para otros usuarios.
        tk.Button(ventana_menu, text="Asignar Sucursal", command=lambda: mostrar_asignar_sucursal(ventana_menu)).pack(pady=5)
        tk.Button(ventana_menu, text="Generar Reportes", command=lambda: mostrar_reporte_viajes(ventana_menu)).pack(pady=5)
        tk.Label(ventana_menu, text="").pack(pady=7)  # Etiqueta vacía para crear espacio (estética).

    tk.Label(ventana_menu, text="").pack(pady=10)  # Etiqueta vacía para crear espacio (estética).

    # Frame para agrupar los botones de salida.
    frame_botones_salida = tk.Frame(ventana_menu)
    frame_botones_salida.pack(pady=10)

    # Función para regresar al login.
    def regresar_al_login():
        ventana_menu.destroy()
        mostrar_login()

    # Función para salir del programa.
    def salir():
        ventana_menu.destroy()

    # Botón para regresar al login.
    tk.Button(
        frame_botones_salida,
        text="Regresar al Login",
        command=regresar_al_login,  # Llama a la función para redirigir al login.
        bg="orange",
        fg="white"
    ).pack(side=tk.LEFT, padx=10)  # Alineación horizontal con espacio entre botones.

    # Botón de salir.
    tk.Button(
        frame_botones_salida,
        text="Salir",
        command=salir,  # Llama a la funcion para cerrar la ventana.
        bg="red",
        fg="white"
    ).pack(side=tk.LEFT, padx=10)  # Alineación horizontal con espacio entre botones.

    ventana_menu.mainloop()

#  Implementa la interfaz de la ventana para registrar viajes.
def mostrar_registrar_viaje(usuario, ventana_menu):
    if usuario[4] == "Gerente de tienda":  # Re-validación de usuario.
        ventana_viaje = tk.Toplevel()  # Usar Toplevel para ventanas secundarias.
        ventana_viaje.title("Registrar Viaje")

        #  Centrar la ventana en la pantalla.
        ancho_ventana = 300
        alto_ventana = 520  # Aumentamos la altura para acomodar los nuevos Labels.
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
        transportistas = ejecutar_query(conectar_db(), "SELECT id, nombre, tarifa_por_km FROM Transportista")

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
            colaboradores_listbox.delete(0, tk.END)  # Limpiar la lista actual.
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
            actualizar_info()  # Actualizar la información al cambiar la sucursal.

        #  Función para calcular la suma de distancias y la tarifa total.
        def actualizar_info(*args):
            if not sucursal_seleccionada.get() or not transportista_seleccionado.get():
                return

            #  Obtener la tarifa del transportista seleccionado.
            transportista_id = int(transportista_seleccionado.get().split(" - ")[0])
            transportista = next(t for t in transportistas if t[0] == transportista_id)
            tarifa_por_km = transportista[2]

            #  Calcular la suma de las distancias de los colaboradores seleccionados.
            distancia_total = 0
            for i in colaboradores_listbox.curselection():
                colaborador_id = int(colaboradores_listbox.get(i).split(" - ")[0])
                distancia = obtener_distancia_sucursal_colaborador(colaborador_id,
                                                                   int(sucursal_seleccionada.get().split(" - ")[0]))
                if distancia:
                    distancia_total += distancia

            tarifa_total = distancia_total * tarifa_por_km  # Calcular la tarifa total.

            #  Actualizar los Labels con la información.
            distancia_label.config(text=f"Suma de distancias: {distancia_total} km")
            tarifa_label.config(text=f"Tarifa total: L.{tarifa_total:.2f}")

        #  Vincular la función de actualización al cambio de selección de sucursal y transportista.
        sucursal_seleccionada.trace("w", actualizar_colaboradores)
        transportista_seleccionado.trace("w", actualizar_info)
        colaboradores_listbox.bind("<<ListboxSelect>>", actualizar_info)

        #  Función para registrar el viaje.
        def guardar_viaje():
            #  Validar que se hayan seleccionado todos los campos.
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
                #  Capturar errores de validación lanzados por trips.py.
                error_msg = str(e)  # Obtener el mensaje de error específico
                messagebox.showerror("Error", error_msg)  # Mostrar el mensaje específico al usuario.
                print(f"Error de validación: {error_msg}")  # Imprimir en la terminal.
            except Exception as e:
                #  Capturar otros errores (errores de la base de datos)
                error_msg = f"Ocurrió un problema al registrar el viaje: {str(e)}"
                messagebox.showerror("Error", error_msg)
                print(f"Error: {error_msg}")  # Imprimir en la terminal.

        tk.Label(frame_principal, text="").pack(pady=10)  # Etiqueta vacía para crear espacio (estética).

        #  Botón para guardar el viaje.
        tk.Button(
            frame_principal,
            text="Guardar Viaje",
            command=guardar_viaje,
            bg="blue",
            fg="white"
        ).pack(side=tk.LEFT, padx=15)

        #  Botón para cancelar.
        def cancelar():
            ventana_viaje.destroy()
            ventana_menu.deiconify()  # Mostrar la ventana del menú principal.

        tk.Button(
            frame_principal,
            text="Cancelar",
            command=cancelar,
            bg="orange",
            fg="white"
        ).pack(side=tk.LEFT, padx=10)

        #  Bloquear la ventana principal.
        ventana_viaje.grab_set()
        ventana_viaje.focus_set()
        ventana_viaje.wait_window()
    else:
        messagebox.showerror("Error", "Usuario no autorizado.")

#  Implementa la interfaz de la ventana para asignar sucursales.
def mostrar_asignar_sucursal(ventana_menu):
    ventana_asignar = tk.Toplevel()  # Usar Toplevel para ventanas secundarias.
    ventana_asignar.title("Asignar Sucursal")

    #  Centrar la ventana en la pantalla.
    ancho_ventana = 300
    alto_ventana = 350
    x_pos = (ventana_asignar.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y_pos = (ventana_asignar.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana_asignar.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

    #  Ocultar la ventana del menú principal.
    ventana_menu.withdraw()

    #  Frame principal.
    frame_principal = tk.Frame(ventana_asignar)
    frame_principal.pack(pady=20)

    #  Obtener datos de la base de datos.
    colaboradores = ejecutar_query(conectar_db(), "SELECT id, nombre FROM Colaborador")
    sucursales = ejecutar_query(conectar_db(), "SELECT id, nombre FROM Sucursal")

    #  Variables para almacenar las selecciones.
    colaborador_seleccionado = tk.StringVar(ventana_asignar)
    sucursal_seleccionada = tk.StringVar(ventana_asignar)

    #  Campo para seleccionar colaborador.
    tk.Label(frame_principal, text="Colaborador:").pack(pady=5)
    colaborador_menu = tk.OptionMenu(frame_principal, colaborador_seleccionado, *[f"{c[0]} - {c[1]}" for c in colaboradores])
    colaborador_menu.pack(pady=5)

    #  Campo para seleccionar sucursal.
    tk.Label(frame_principal, text="Sucursal:").pack(pady=5)
    sucursal_menu = tk.OptionMenu(frame_principal, sucursal_seleccionada, *[f"{s[0]} - {s[1]}" for s in sucursales])
    sucursal_menu.pack(pady=5)

    #  Campo para ingresar la distancia.
    tk.Label(frame_principal, text="Distancia (km):").pack(pady=5)
    distancia_entry = tk.Entry(frame_principal, width=10)
    distancia_entry.pack(pady=5)

    #  Función para asignar la sucursal al colaborador.
    def guardar_asignacion():

        if not colaborador_seleccionado.get():
            messagebox.showerror("Error", "Debe seleccionar un colaborador.")
            return
        if not sucursal_seleccionada.get():
            messagebox.showerror("Error", "Debe seleccionar una sucursal.")
            return
        if not distancia_entry.get():
            messagebox.showerror("Error", "Debe ingresar una distancia.")
            return

        try:
            # Obtener los valores seleccionados.
            colaborador_id = int(colaborador_seleccionado.get().split(" - ")[0])
            sucursal_id = int(sucursal_seleccionada.get().split(" - ")[0])
            distancia_km = float(distancia_entry.get())

            # Validar que la distancia esté entre 1 y 50 km.
            if not (1 <= distancia_km <= 50):
                raise ValueError("La distancia debe estar entre 1 y 50 km.")

            # Verificar si el colaborador ya tiene asignada esta sucursal.
            if existe_asignacion(colaborador_id, sucursal_id):
                raise ValueError("El colaborador ya tiene asignada esta sucursal.")

            # Intentar asignar la sucursal al colaborador.
            if asignar_sucursal_a_colaborador(colaborador_id, sucursal_id, distancia_km):
                messagebox.showinfo("Éxito", "Sucursal asignada correctamente.")
                ventana_asignar.destroy()
                ventana_menu.deiconify()  # Mostrar la ventana del menú principal.
            else:
                messagebox.showerror("Error", "No se pudo asignar la sucursal.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema: {str(e)}")

    tk.Label(frame_principal, text="").pack(pady=25)  # Etiqueta vacía para crear espacio (estética).

    #  Botón para guardar la asignación.
    tk.Button(
        frame_principal,
        text="Guardar Asignación",
        command=guardar_asignacion,
        bg="blue",
        fg="white"
    ).pack(side=tk.LEFT, padx=15)

    #  Botón para cancelar.
    def cancelar():
        ventana_asignar.destroy()
        ventana_menu.deiconify()  # Mostrar la ventana del menú principal.

    tk.Button(
        frame_principal,
        text="Cancelar",
        command=cancelar,
        bg="orange",
        fg="white"
    ).pack(side=tk.LEFT, padx=10)

    #  Bloquear la ventana principal.
    ventana_asignar.grab_set()
    ventana_asignar.focus_set()
    ventana_asignar.wait_window()


#  Implementa la interfaz de la ventana para generar reportes.
def mostrar_reporte_viajes(ventana_menu):
    ventana_reporte = tk.Toplevel()  # Usar Toplevel para ventanas secundarias.
    ventana_reporte.title("Generar Reporte de Viajes")

    #  Centrar la ventana en la pantalla.
    ancho_ventana = 400
    alto_ventana = 300
    x_pos = (ventana_reporte.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y_pos = (ventana_reporte.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana_reporte.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

    #  Ocultar la ventana del menú principal.
    ventana_menu.withdraw()

    #  Frame principal.
    frame_principal = tk.Frame(ventana_reporte)
    frame_principal.pack(pady=20)

    #  Obtener datos de la base de datos.
    transportistas = ejecutar_query(conectar_db(), "SELECT id, nombre FROM Transportista")

    #  Variables para almacenar las selecciones.
    fecha_inicio = tk.StringVar(ventana_reporte)
    fecha_fin = tk.StringVar(ventana_reporte)
    transportista_seleccionado = tk.StringVar(ventana_reporte)

    #  Campo para seleccionar fecha de inicio.
    tk.Label(frame_principal, text="Fecha de Inicio:").pack(pady=5)
    fecha_inicio_entry = DateEntry(frame_principal, textvariable=fecha_inicio, date_pattern="yyyy-mm-dd", width=12)
    fecha_inicio_entry.pack(pady=5)

    #  Campo para seleccionar fecha de fin.
    tk.Label(frame_principal, text="Fecha de Fin:").pack(pady=5)
    fecha_fin_entry = DateEntry(frame_principal, textvariable=fecha_fin, date_pattern="yyyy-mm-dd", width=12)
    fecha_fin_entry.pack(pady=5)

    #  Campo para seleccionar transportista.
    tk.Label(frame_principal, text="Transportista:").pack(pady=5)
    transportista_menu = tk.OptionMenu(frame_principal, transportista_seleccionado, *[f"{t[0]} - {t[1]}" for t in transportistas])
    transportista_menu.pack(pady=5)

    #  Función para generar el reporte.
    def generar_reporte(ventana_menu):
        ventana_reporte.destroy()
        try:
            # Validar que se hayan ingresado las fechas y seleccionado un transportista.
            if not fecha_inicio.get() or not fecha_fin.get():
                messagebox.showerror("Error", "Debe ingresar ambas fechas.")
                return
            if not transportista_seleccionado.get():
                messagebox.showerror("Error", "Debe seleccionar un transportista.")
                return

            # Obtener los valores seleccionados.
            transportista_id = int(transportista_seleccionado.get().split(" - ")[0])

            # Obtener la tarifa por kilómetro del transportista.
            query_tarifa = "SELECT tarifa_por_km FROM Transportista WHERE id = ?"
            tarifa_por_km = ejecutar_query(conectar_db(), query_tarifa, (transportista_id,))[0][0]

            # Generar el reporte.
            reporte = generar_reporte_viajes(fecha_inicio.get(), fecha_fin.get(), transportista_id)

            if reporte:
                # Crear una nueva ventana para mostrar el reporte.
                ventana_resultados = tk.Toplevel()
                ventana_resultados.title("Resultados del Reporte")

                # Frame principal para organizar los elementos.
                frame_resultados = tk.Frame(ventana_resultados)
                frame_resultados.pack(pady=20, padx=20)

                # Mostrar los detalles del reporte.
                tk.Label(frame_resultados, text="Detalles del Reporte", font=("Arial", 16, "bold")).pack(pady=10)

                tk.Label(frame_resultados, text="").pack(pady=7)  # Etiqueta vacía para crear espacio (estética).

                # Mostrar cada viaje.
                for viaje in reporte:
                    fecha, sucursal, transportista, distancia_total, colaboradores = viaje
                    tk.Label(frame_resultados, text=f"Fecha: {fecha}, Sucursal: {sucursal}, Transportista: {transportista}, Distancia: {distancia_total} km, Colaboradores: {colaboradores}").pack()

                tk.Label(frame_resultados, text="").pack(pady=7)  # Etiqueta vacía para crear espacio (estética).

                # Calcular el total de kilómetros recorridos.
                total_km = sum(viaje[3] for viaje in reporte)

                # Mostrar el total de kilómetros recorridos.
                tk.Label(frame_resultados, text=f"Total de kilómetros recorridos: {total_km} km", font=("Arial", 10)).pack(pady=10)

                # Mostrar la tarifa por kilómetro.
                tk.Label(frame_resultados, text=f"Tarifa por kilómetro: L.{tarifa_por_km:.2f}", font=("Arial", 10, )).pack(pady=5)

                # Calcular el total a pagar usando la función de reports.py.
                total_a_pagar = calcular_total_a_pagar(reporte, tarifa_por_km)
                tk.Label(frame_resultados, text=f"Total a pagar: L.{total_a_pagar:.2f}", font=("Arial", 12, "bold")).pack(pady=10)

                tk.Label(frame_resultados, text="").pack(pady=10)  # Etiqueta vacía para crear espacio (estética).

                # Botón para volver al menú principal.
                def volver_al_menu():
                    ventana_resultados.destroy()
                    ventana_menu.deiconify()  # Mostrar la ventana del menú principal.

                tk.Button(
                    frame_resultados,
                    text="Volver al Menú Principal",
                    command=volver_al_menu,
                    bg="green",
                    fg="white"
                ).pack(pady=10)

                # Ajustar el tamaño de la ventana de resultados dinámicamente.
                ventana_resultados.update_idletasks()
                ancho_ventana_resultados = ventana_resultados.winfo_width()
                alto_ventana_resultados = ventana_resultados.winfo_height()
                x_pos = (ventana_resultados.winfo_screenwidth() // 2) - (ancho_ventana_resultados // 2)
                y_pos = (ventana_resultados.winfo_screenheight() // 2) - (alto_ventana_resultados // 2)
                ventana_resultados.geometry(f"+{x_pos}+{y_pos}")

            else:
                messagebox.showinfo("Información", "No hay viajes registrados en el rango de fechas seleccionado.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema al generar el reporte: {str(e)}")

    tk.Label(frame_principal, text="").pack(pady=10)  # Etiqueta vacía para crear espacio (estética).

    #  Botón para generar el reporte.
    tk.Button(
        frame_principal,
        text="Generar Reporte",
        command=lambda: generar_reporte(ventana_menu),
        bg="blue",
        fg="white"
    ).pack(side=tk.LEFT, padx=15)

    #  Botón para cancelar.
    def cancelar():
        ventana_reporte.destroy()
        ventana_menu.deiconify()  # Mostrar la ventana del menú principal.

    tk.Button(
        frame_principal,
        text="Cancelar",
        command=cancelar,
        bg="orange",
        fg="white"
    ).pack(side=tk.LEFT, padx=10)

    #  Bloquear la ventana principal.
    ventana_reporte.grab_set()
    ventana_reporte.focus_set()
    ventana_reporte.wait_window()
