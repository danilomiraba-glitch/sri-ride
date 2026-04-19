from __future__ import annotations

def construir_remision_contexto(normalizado: dict) -> dict:
    return normalizado["remision"]


def construir_destino_contexto(normalizado: dict) -> dict:
    return normalizado["destino"]
