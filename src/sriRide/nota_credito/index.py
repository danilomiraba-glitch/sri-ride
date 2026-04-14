from __future__ import annotations

from .cliente import construir_cliente_contexto
from .comprobante import construir_comprobante_contexto
from .doc import construir_doc_contexto
from .emisor import construir_emisor_contexto
from .producto import construir_producto_contexto
from .repetibles import construir_info_adicional_contexto
from .totales import construir_totales_contexto
from .xml_utils import XmlInput, load_xml_root


def construir_contexto_desde_xml(xml_input: XmlInput) -> dict:
    nota_credito_root = load_xml_root(xml_input)
    producto_ctx = construir_producto_contexto(nota_credito_root)
    producto_items = producto_ctx.get("items", [])
    page_size = "A4" if len(producto_items) >= 10 else "auto"

    return {
        "doc": construir_doc_contexto(nota_credito_root),
        "emisor": construir_emisor_contexto(nota_credito_root),
        "cliente": construir_cliente_contexto(nota_credito_root),
        "producto": producto_ctx,
        "layout": {
            "page_size": page_size,
        },
        "info_adicional": construir_info_adicional_contexto(nota_credito_root),
        "totales": construir_totales_contexto(nota_credito_root),
        "comprobante": construir_comprobante_contexto(nota_credito_root),
    }
