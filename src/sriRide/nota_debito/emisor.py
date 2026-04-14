from __future__ import annotations

from lxml import etree

from .xml_utils import first_text


def construir_emisor_contexto(nota_debito_root: etree._Element) -> dict:
    obligado_map = {
        "SI": "SI",
        "NO": "NO",
    }

    regimen = first_text(nota_debito_root, "notaDebito.infoTributaria.contribuyenteRimpe")
    if not regimen:
        regimen = "General"

    obligado_raw = first_text(nota_debito_root, "notaDebito.infoNotaDebito.obligadoContabilidad")
    obligado = obligado_map.get((obligado_raw or "").upper(), obligado_raw)

    return {
        "direccion": first_text(nota_debito_root, "notaDebito.infoTributaria.dirMatriz"),
        "direccion_estab": first_text(nota_debito_root, "notaDebito.infoNotaDebito.dirEstablecimiento"),
        "nombre_comercial": first_text(nota_debito_root, "notaDebito.infoTributaria.nombreComercial"),
        "razon_social": first_text(nota_debito_root, "notaDebito.infoTributaria.razonSocial"),
        "regimen": regimen,
        "obligado_contabilidad": obligado,
    }

