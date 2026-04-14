from __future__ import annotations


def construir_anexos_contexto(
    *,
    remision_activa: bool,
    exportador_activo: bool,
    reembolso_activo: bool,
    destino_items: list[dict],
    gastos_exportacion_items: list[dict],
    reembolso_items: list[dict],
) -> dict:
    """
    Construye el contexto de anexos para render principal y plantillas separadas.
    """
    activos: list[str] = []
    if remision_activa:
        activos.append("guiaRemision")
    if exportador_activo:
        activos.append("exportacion")
    if reembolso_activo:
        activos.append("reembolsos")

    cantidad = len(activos)
    partes = [
        {
            "codigo": nombre,
            "indice": i,
            "total": cantidad,
        }
        for i, nombre in enumerate(activos, start=1)
    ]

    if cantidad > 0:
        info = f"Este documento incluye {cantidad} Anexo(s) - mantengalos juntos"
    else:
        info = "Este documento no incluye Anexos"

    anexos = {
        "info": info,
        "length": cantidad,
        "cantidad": cantidad,
        "has_anexos": cantidad > 0,
        "activados": activos,
        "partes": partes,
        "guiaRemision": {"destinos": destino_items} if remision_activa else None,
        "exportacion": {"gastos": gastos_exportacion_items} if exportador_activo else None,
        "reembolsos": {"items": reembolso_items} if reembolso_activo else None,
    }
    return anexos
