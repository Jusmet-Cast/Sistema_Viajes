
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
def ejecutar_esquema():
    try:
        with conectar_db() as conexion:  # Usar 'with' para manejar la conexión automáticamente.
            if conexion:
                with open('db/schema.sql', 'r') as archivo_sql:
                    esquema = archivo_sql.read()
                    cursor = conexion.cursor()
                    cursor.executescript(esquema)
                print("Esquema ejecutado correctamente.")
    except FileNotFoundError:
        print("Error: El archivo schema.sql no existe.")
    except sqlite3.Error as e:
        print(f"Error al ejecutar el esquema: {e}")

# Ejecuta una consulta SQL.
def ejecutar_query(conexion, query: str, parametros=()) -> list | int | None:
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
            viaje_id = cursor.lastrowid  # Obtener el ID del viaje recién insertado
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
