from __future__ import annotations

def construir_pago_contexto(normalizado: dict) -> dict:
    return normalizado["pago"]


def construir_info_adicional_contexto(normalizado: dict) -> dict:
    return normalizado["info_adicional"]
