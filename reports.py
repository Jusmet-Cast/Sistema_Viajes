
from db import ejecutar_query, conectar_db

def generar_reporte_viajes(fecha_inicio: str, fecha_fin: str, transportista_id: int) -> list:
    """
    Genera un reporte de viajes realizados por un transportista en un rango de fechas.

    Args:
        fecha_inicio (str): Fecha de inicio en formato YYYY-MM-DD.
        fecha_fin (str): Fecha de fin en formato YYYY-MM-DD.
        transportista_id (int): ID del transportista.

    Returns:
        list: Lista de tuplas con los detalles de los viajes.
    """
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

def calcular_total_a_pagar(reporte: list, tarifa_por_km: float) -> float:
    total_km = sum(viaje[3] for viaje in reporte)  # Sumar las distancias totales.
    return total_km * tarifa_por_km
