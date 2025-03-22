
import sqlite3
from datetime import datetime
from db import (
    conectar_db,
    ejecutar_query,
    asignar_sucursal_a_colaborador_db,
    existe_colaborador_db,
    existe_sucursal_db,
    existe_asignacion_db,
    es_gerente_de_tienda_db,
    colaborador_tiene_viaje_en_fecha_db,
    obtener_distancia_sucursal_colaborador_db,
    registrar_viaje_db,
    asociar_colaboradores_a_viaje_db,
    generar_reporte_viajes_db,
)


# Válida que la distancia esté entre 1 y 50 km.
def validar_distancia(distancia_km):
    if not (1 <= distancia_km <= 50):
        raise ValueError("La distancia debe estar entre 1 y 50 km.")


# Asigna una sucursal a un colaborador, validando la información.
def asignar_sucursal_a_colaborador(colaborador_id, sucursal_id, distancia_km):
    try:
        # Validar distancia
        validar_distancia(distancia_km)

        # Verificar si el colaborador existe
        if not existe_colaborador_db(colaborador_id):
            raise ValueError("El colaborador no existe.")

        # Verificar si la sucursal existe
        if not existe_sucursal_db(sucursal_id):
            raise ValueError("La sucursal no existe.")

        # Verificar si ya existe la asignación
        if existe_asignacion_db(colaborador_id, sucursal_id):
            raise ValueError("El colaborador ya tiene asignada esta sucursal.")

        # Insertar la asignación
        filas_afectadas = asignar_sucursal_a_colaborador_db(colaborador_id, sucursal_id, distancia_km)

        if filas_afectadas:
            print("Sucursal asignada correctamente.")
            return True
        else:
            print("Error: No se pudo asignar la sucursal.")
            return False

    except ValueError as e:
        print(f"Error de validación: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        return False


# Registra un viaje, validando todas las restricciones.
def registrar_viaje(usuario_id, sucursal_id, transportista_id, colaboradores_ids):
    try:
        # Verificar si el usuario es gerente de tienda
        if not es_gerente_de_tienda_db(usuario_id):
            raise ValueError("Solo los gerentes de tienda pueden registrar viajes.")

        # Obtener la fecha actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        # Verificar que los colaboradores no tengan un viaje en la fecha actual
        for colaborador_id in colaboradores_ids:
            if colaborador_tiene_viaje_en_fecha_db(colaborador_id, fecha_actual):
                raise ValueError(f"El colaborador {colaborador_id} ya tiene un viaje registrado para hoy.")

        # Calcular la distancia total del viaje
        distancia_total = 0
        for colaborador_id in colaboradores_ids:
            distancia = obtener_distancia_sucursal_colaborador_db(colaborador_id, sucursal_id)
            if distancia:
                distancia_total += distancia
            else:
                raise ValueError(f"El colaborador {colaborador_id} no tiene asignada la sucursal {sucursal_id}.")

        # Validar que la distancia total no supere los 100 km
        if distancia_total > 100:
            raise ValueError("La distancia total del viaje no puede superar los 100 km.")

        # Insertar el viaje
        filas_afectadas = registrar_viaje_db(fecha_actual, sucursal_id, transportista_id, usuario_id, distancia_total)

        if filas_afectadas:
            # Obtener el ID del viaje recién insertado
            viaje_id = ejecutar_query(conectar_db(), "SELECT last_insert_rowid()")[0][0]

            # Asociar colaboradores al viaje
            asociar_colaboradores_a_viaje_db(viaje_id, colaboradores_ids)

            print("Viaje registrado correctamente.")
            return True
        else:
            print("Error: No se pudo registrar el viaje.")
            return False

    except ValueError as e:
        print(f"Error de validación: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        return False


# Genera un reporte de viajes por rango de fechas y transportista.
def generar_reporte_viajes(fecha_inicio, fecha_fin, transportista_id):
    return generar_reporte_viajes_db(fecha_inicio, fecha_fin, transportista_id)
