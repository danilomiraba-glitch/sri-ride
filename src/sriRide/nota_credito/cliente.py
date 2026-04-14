from __future__ import annotations

from lxml import etree

from .xml_utils import first_text


def construir_cliente_contexto(nota_credito_root: etree._Element) -> dict:
    return {
        "razon_social": first_text(nota_credito_root, "notaCredito.infoNotaCredito.razonSocialComprador"),
        "identificacion": first_text(nota_credito_root, "notaCredito.infoNotaCredito.identificacionComprador"),
        "fecha_emision": first_text(nota_credito_root, "notaCredito.infoNotaCredito.fechaEmision"),
    }
