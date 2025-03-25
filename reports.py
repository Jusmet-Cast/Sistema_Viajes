
from db import ejecutar_query, conectar_db

#  Consulta para generar reportes.
"""
Aquí se combinan varias tablas para obtener la información completa:
Sucursal s -> Se une con Viaje mediante sucursal_id, para obtener el nombre de la sucursal.
Transportista t -> Se une con Viaje mediante transportista_id, para obtener el nombre del transportista.
ViajeColaborador vc -> Relaciona los viajes con los colaboradores, permitiendo saber qué colaboradores participaron en cada viaje.
Colaborador c -> Se une con ViajeColaborador para obtener el nombre de cada colaborador.
"""
def generar_reporte_viajes(fecha_inicio: str, fecha_fin: str, transportista_id: int):
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

#  Obtiene el calculo del pago al transportista.
def calcular_total_a_pagar(reporte: list, tarifa_por_km: float):
    total_km = sum(viaje[3] for viaje in reporte)  # Sumar las distancias totales.
    return total_km * tarifa_por_km
