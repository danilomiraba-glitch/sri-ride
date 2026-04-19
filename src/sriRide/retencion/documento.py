from __future__ import annotations

def construir_documento_contexto(normalizado: dict) -> dict:
    return normalizado["documento"]


def extraer_retenciones_planas(documentos_ctx: dict) -> list[dict]:
    """Extrae una lista plana de todas las retenciones de todos los documentos."""
    retenciones_planas: list[dict] = []

    for doc in documentos_ctx.get("items", []):
        for retencion in doc.get("detalle_retencion", []):
            retenciones_planas.append(retencion)

    return retenciones_planas
