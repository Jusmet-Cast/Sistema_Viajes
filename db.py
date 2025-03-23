
import sqlite3

# Conecta a la base de datos data.db.
def conectar_db():
    try:
        conexion = sqlite3.connect('db/data.db')
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Ejecuta el esquema de la base de datos.
def ejecutar_esquema(conexion):
    try:
        with open('db/schema.sql', 'r') as archivo_sql:
            esquema = archivo_sql.read()
            with conexion:
                cursor = conexion.cursor()
                cursor.executescript(esquema)
        print("Esquema ejecutado correctamente.")
    except FileNotFoundError:
        print("Error: El archivo schema.sql no existe.")
    except sqlite3.Error as e:
        print(f"Error al ejecutar el esquema: {e}")

# Ejecuta una consulta SQL.
def ejecutar_query(conexion, query, parametros=()):
    try:
        with conexion:
            cursor = conexion.cursor()
            cursor.execute(query, parametros)
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()  # Devuelve los resultados para consultas SELECT
            else:
                return cursor.rowcount  # Devuelve el número de filas afectadas para INSERT, UPDATE, DELETE
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None


# ----- Funciones para travels.py -----

# Asigna una sucursal a un colaborador en la DB.
def asignar_sucursal_a_colaborador_db(colaborador_id, sucursal_id, distancia_km):
    query = "INSERT INTO AsignacionSucursal (colaborador_id, sucursal_id, distancia_km) VALUES (?, ?, ?)"
    return ejecutar_query(conectar_db(), query, (colaborador_id, sucursal_id, distancia_km))

# Verifica si un colaborador existe en la DB.
def existe_colaborador_db(colaborador_id):
    query = "SELECT 1 FROM Colaborador WHERE id = ?"
    return bool(ejecutar_query(conectar_db(), query, (colaborador_id,)))

# Verifica si una sucursal existe en la DB.
def existe_sucursal_db(sucursal_id):
    query = "SELECT 1 FROM Sucursal WHERE id = ?"
    return bool(ejecutar_query(conectar_db(), query, (sucursal_id,)))

# Verifica si ya existe una asignación para el colaborador y la sucursal.
def existe_asignacion_db(colaborador_id, sucursal_id):
    query = "SELECT 1 FROM AsignacionSucursal WHERE colaborador_id = ? AND sucursal_id = ?"
    return bool(ejecutar_query(conectar_db(), query, (colaborador_id, sucursal_id)))

# Verifica si un usuario tiene el perfil 'Gerente de tienda'.
def es_gerente_de_tienda_db(usuario_id):
    query = "SELECT 1 FROM Usuario WHERE id = ? AND rol = 'Gerente de tienda'"
    return bool(ejecutar_query(conectar_db(), query, (usuario_id,)))

# Verifica si un colaborador ya tiene un viaje registrado para la fecha actual.
def colaborador_tiene_viaje_en_fecha_db(colaborador_id, fecha):
    query = """
    SELECT 1 
    FROM ViajeColaborador vc
    JOIN Viaje v ON vc.viaje_id = v.id
    WHERE vc.colaborador_id = ? AND v.fecha = ?
    """
    return bool(ejecutar_query(conectar_db(), query, (colaborador_id, fecha)))

# Obtiene la distancia de una sucursal asignada a un colaborador.
def obtener_distancia_sucursal_colaborador_db(colaborador_id, sucursal_id):
    query = "SELECT distancia_km FROM AsignacionSucursal WHERE colaborador_id = ? AND sucursal_id = ?"
    resultado = ejecutar_query(conectar_db(), query, (colaborador_id, sucursal_id))
    return resultado[0][0] if resultado else None

# Registra un viaje en la DB.
def registrar_viaje_db(fecha, sucursal_id, transportista_id, usuario_registro_id, distancia_total):
    query = "INSERT INTO Viaje (fecha, sucursal_id, transportista_id, usuario_registro_id, distancia_total) VALUES (?, ?, ?, ?, ?)"
    return ejecutar_query(conectar_db(), query, (fecha, sucursal_id, transportista_id, usuario_registro_id, distancia_total))

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


# Genera un reporte de viajes por rango de fechas y transportista.
def generar_reporte_viajes_db(fecha_inicio, fecha_fin, transportista_id):
    query = """
    SELECT v.fecha, s.nombre AS sucursal, t.nombre AS transportista, v.distancia_total, GROUP_CONCAT(c.nombre, ', ') AS colaboradores
    FROM Viaje v
    JOIN Sucursal s ON v.sucursal_id = s.id
    JOIN Transportista t ON v.transportista_id = t.id
    JOIN ViajeColaborador vc ON v.id = vc.viaje_id
    JOIN Colaborador c ON vc.colaborador_id = c.id
    WHERE v.fecha BETWEEN ? AND ? AND v.transportista_id = ?
    GROUP BY v.id
    """
    return ejecutar_query(conectar_db(), query, (fecha_inicio, fecha_fin, transportista_id))
