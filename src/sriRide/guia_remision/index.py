from __future__ import annotations

from .destinatario import construir_destinatario_contexto
from .doc import construir_doc_contexto
from .emisor import construir_emisor_contexto
from .normalizer import normalizar_guia_remision
from .producto import construir_producto_contexto
from .repetibles import construir_info_adicional_contexto
from .transportista import construir_transportista_contexto
from .xml_utils import XmlInput


def construir_contexto_desde_xml(xml_input: XmlInput) -> dict:
    normalizado = normalizar_guia_remision(xml_input)
    transportista_ctx = construir_transportista_contexto(normalizado)
    producto_ctx = construir_producto_contexto(normalizado)
    destinatario_ctx = construir_destinatario_contexto(normalizado)

    total_destinatarios = len(destinatario_ctx.get("items", []))
    total_productos = len(producto_ctx.get("items", []))

    if total_destinatarios >= 3:
        page_size = "A4"
    elif total_productos >= 10:
        page_size = "A4"
    else:
        page_size = "auto"

    return {
        "doc": construir_doc_contexto(normalizado),
        "emisor": construir_emisor_contexto(normalizado),
        "transportista": transportista_ctx,
        "trasportista": transportista_ctx,
        "detalle_producto": producto_ctx,
        "deatalle_producto": producto_ctx,
        "layout": {
            "page_size": page_size,
        },
        "info_adicional": construir_info_adicional_contexto(normalizado),
        "destinatario": destinatario_ctx,
    }
