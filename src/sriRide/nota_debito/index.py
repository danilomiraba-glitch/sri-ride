from __future__ import annotations

from .cliente import construir_cliente_contexto
from .comprobante import construir_comprobante_contexto
from .doc import construir_doc_contexto
from .emisor import construir_emisor_contexto
from .normalizer import normalizar_nota_debito
from .producto import construir_producto_contexto
from .repetibles import construir_info_adicional_contexto, construir_pago_contexto
from .totales import construir_totales_contexto
from .xml_utils import XmlInput


def construir_contexto_desde_xml(xml_input: XmlInput) -> dict:
    normalizado = normalizar_nota_debito(xml_input)

    return {
        "doc": construir_doc_contexto(normalizado),
        "emisor": construir_emisor_contexto(normalizado),
        "cliente": construir_cliente_contexto(normalizado),
        "producto": construir_producto_contexto(normalizado),
        "pago": construir_pago_contexto(normalizado),
        "info_adicional": construir_info_adicional_contexto(normalizado),
        "totales": construir_totales_contexto(normalizado),
        "comprobante": construir_comprobante_contexto(normalizado),
    }
