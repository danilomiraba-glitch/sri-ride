from __future__ import annotations

from .cliente import construir_cliente_contexto
from .comprobante import construir_comprobante_contexto
from .doc import construir_doc_contexto
from .emisor import construir_emisor_contexto
from .producto import construir_producto_contexto
from .repetibles import construir_info_adicional_contexto, construir_pago_contexto
from .totales import construir_totales_contexto
from .xml_utils import XmlInput, load_xml_root


def construir_contexto_desde_xml(xml_input: XmlInput) -> dict:
    nota_debito_root = load_xml_root(xml_input)

    return {
        "doc": construir_doc_contexto(nota_debito_root),
        "emisor": construir_emisor_contexto(nota_debito_root),
        "cliente": construir_cliente_contexto(nota_debito_root),
        "producto": construir_producto_contexto(nota_debito_root),
        "pago": construir_pago_contexto(nota_debito_root),
        "info_adicional": construir_info_adicional_contexto(nota_debito_root),
        "totales": construir_totales_contexto(nota_debito_root),
        "comprobante": construir_comprobante_contexto(nota_debito_root),
    }

