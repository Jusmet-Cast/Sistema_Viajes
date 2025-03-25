
import sqlite3
from datetime import datetime
from db import (
    conectar_db,
    ejecutar_query
)

# Obtiene la distancia de una sucursal asignada a un colaborador.
def obtener_distancia_sucursal_colaborador(colaborador_id, sucursal_id):
    query = "SELECT distancia_km FROM AsignacionSucursal WHERE colaborador_id = ? AND sucursal_id = ?"
    resultado = ejecutar_query(conectar_db(), query, (colaborador_id, sucursal_id))
    return resultado[0][0] if resultado else None

# Registra un viaje en la DB.
def registrar_viaje_db(fecha, sucursal_id, transportista_id, usuario_registro_id, distancia_total):
    try:
        conexion = conectar_db()
        with conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO Viaje (fecha, sucursal_id, transportista_id, usuario_registro_id, distancia_total) VALUES (?, ?, ?, ?, ?)",
                (fecha, sucursal_id, transportista_id, usuario_registro_id, distancia_total)
            )
            viaje_id = cursor.lastrowid  # Obtener el ID del viaje recién insertado.
            return viaje_id
    except sqlite3.Error as e:
        print(f"Error al registrar el viaje: {e}")
        return None

# Asocia colaboradores a un viaje en la DB.
def asociar_colaboradores_a_viaje_db(viaje_id, colaboradores_ids):
    try:
        conexion = conectar_db()
        with conexion:
            cursor = conexion.cursor()
            for colaborador_id in colaboradores_ids:
                cursor.execute(
                    "INSERT INTO ViajeColaborador (viaje_id, colaborador_id) VALUES (?, ?)",
                    (viaje_id, colaborador_id)
                )
        print("Colaboradores asociados al viaje correctamente.")
    except sqlite3.Error as e:
        print(f"Error al asociar colaboradores al viaje: {e}")
        raise e

# Verifica si un colaborador ya tiene un viaje registrado para la fecha actual.
def colaborador_tiene_viaje_en_fecha(colaborador_id, fecha):
    query = """
    SELECT 1 
    FROM ViajeColaborador vc
    JOIN Viaje v ON vc.viaje_id = v.id
    WHERE vc.colaborador_id = ? AND v.fecha = ?
    """
    resultados = ejecutar_query(conectar_db(), query, (colaborador_id, fecha))
    return bool(resultados)

# Verifica si un usuario tiene el perfil 'Gerente de tienda'.
def es_gerente_de_tienda(usuario_id):
    query = "SELECT 1 FROM Usuario WHERE id = ? AND rol = 'Gerente de tienda'"
    return bool(ejecutar_query(conectar_db(), query, (usuario_id,)))

# Registra un viaje, validando todas las restricciones.
def registrar_viaje(usuario_id, sucursal_id, transportista_id, colaboradores_ids):
    try:
        # Verificar si el usuario es gerente de tienda.
        if not es_gerente_de_tienda(usuario_id):
            raise ValueError("Solo los gerentes de tienda pueden registrar viajes.")

        # Obtener la fecha actual.
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        # Verificar que los colaboradores no tengan un viaje en la fecha actual.
        for colaborador_id in colaboradores_ids:
            if colaborador_tiene_viaje_en_fecha(colaborador_id, fecha_actual):
                raise ValueError(f"El colaborador {colaborador_id} ya tiene un viaje registrado para hoy.")

        # Calcular la distancia total del viaje.
        distancia_total = 0
        for colaborador_id in colaboradores_ids:
            distancia = obtener_distancia_sucursal_colaborador(colaborador_id, sucursal_id)
            if distancia:
                distancia_total += distancia
            else:
                raise ValueError(f"El colaborador {colaborador_id} no tiene asignada la sucursal {sucursal_id}.")

        # Validar que la distancia total no supere los 100 km.
        if distancia_total > 100:
            raise ValueError("La distancia total del viaje no puede superar los 100 km.")

        # Insertar el viaje en la base de datos.
        viaje_id = registrar_viaje_db(fecha_actual, sucursal_id, transportista_id, usuario_id, distancia_total)

        if viaje_id:
            # Asociar colaboradores al viaje.
            asociar_colaboradores_a_viaje_db(viaje_id, colaboradores_ids)

            print("Viaje registrado correctamente.")
            return True
        else:
            print("Error: No se pudo registrar el viaje.")
            return False

    except ValueError as e:
        print(f"Error de validación: {e}")
        raise e  # Relanzar la excepción para que la interfaz la capture.
    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        raise Exception(f"Error en la base de datos: {e}")  # Relanzar la excepción para que la interfaz la capture.
