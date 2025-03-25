
import sqlite3
from db import conectar_db, ejecutar_query

# Válida que la distancia esté entre 1 y 50 km.
def validar_distancia(distancia_km):
    if not (1 <= distancia_km <= 50):
        raise ValueError("La distancia debe estar entre 1 y 50 km.")

# Verifica si un colaborador existe en la base de datos.
def existe_colaborador(colaborador_id):
    query = "SELECT 1 FROM Colaborador WHERE id = ?"
    resultados = ejecutar_query(conectar_db(), query, (colaborador_id,))
    return bool(resultados)

# Verifica si una sucursal existe en la base de datos.
def existe_sucursal(sucursal_id):
    query = "SELECT 1 FROM Sucursal WHERE id = ?"
    resultados = ejecutar_query(conectar_db(), query, (sucursal_id,))
    return bool(resultados)

# Verifica si ya existe una asignación para el colaborador y la sucursal.
def existe_asignacion(colaborador_id, sucursal_id):
    query = "SELECT 1 FROM AsignacionSucursal WHERE colaborador_id = ? AND sucursal_id = ?"
    resultados = ejecutar_query(conectar_db(), query, (colaborador_id, sucursal_id))
    return bool(resultados)

# Asigna una sucursal a un colaborador, validando la información.
def asignar_sucursal_a_colaborador(colaborador_id, sucursal_id, distancia_km):
    try:
        # Validar distancia.
        validar_distancia(distancia_km)

        # Verificar si el colaborador existe.
        if not existe_colaborador(colaborador_id):
            raise ValueError("El colaborador no existe.")

        # Verificar si la sucursal existe.
        if not existe_sucursal(sucursal_id):
            raise ValueError("La sucursal no existe.")

        # Verificar si ya existe la asignación.
        if existe_asignacion(colaborador_id, sucursal_id):
            raise ValueError("El colaborador ya tiene asignada esta sucursal.")

        # Insertar la asignación.
        query = "INSERT INTO AsignacionSucursal (colaborador_id, sucursal_id, distancia_km) VALUES (?, ?, ?)"
        filas_afectadas = ejecutar_query(conectar_db(), query, (colaborador_id, sucursal_id, distancia_km))

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

# Obtiene todas las sucursales asignadas a un colaborador.
def obtener_sucursales_colaborador(colaborador_id):
    query = """
    SELECT s.nombre, a.distancia_km 
    FROM Sucursal s 
    JOIN AsignacionSucursal a ON s.id = a.sucursal_id 
    WHERE a.colaborador_id = ?
    """
    resultados = ejecutar_query(conectar_db(), query, (colaborador_id,))
    return resultados if resultados else []
