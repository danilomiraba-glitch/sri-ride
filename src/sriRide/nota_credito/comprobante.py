from __future__ import annotations

from lxml import etree

from .xml_utils import first_text


def construir_comprobante_contexto(nota_credito_root: etree._Element) -> dict:
    tipo_comprobante_map = {
        "01": "FACTURA",
        "03": "LIQUIDACION COMPRA",
        "05": "NOTA DE DEBITO",
        "04": "NOTA DE CREDITO",
        "06": "GUIA DE REMISION",
        "07": "COMPROBANTE DE RETENCION",
    }

    tipo_comprobante_codigo = first_text(nota_credito_root, "notaCredito.infoNotaCredito.codDocModificado")
    tipo_comprobante_label = tipo_comprobante_map.get(tipo_comprobante_codigo or "", tipo_comprobante_codigo)

    return {
        "tipo_comprobante": tipo_comprobante_label,
        "numero_comprobante": first_text(nota_credito_root, "notaCredito.infoNotaCredito.numDocModificado"),
        "fecha_comprobante": first_text(nota_credito_root, "notaCredito.infoNotaCredito.fechaEmisionDocSustento"),
        "motivo": first_text(nota_credito_root, "notaCredito.infoNotaCredito.motivo"),
    }
