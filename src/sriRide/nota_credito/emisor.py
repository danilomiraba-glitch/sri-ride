from __future__ import annotations

from lxml import etree

from .xml_utils import first_text


def construir_emisor_contexto(nota_credito_root: etree._Element) -> dict:
    obligado_map = {
        "SI": "SI",
        "NO": "NO",
    }

    regimen = first_text(nota_credito_root, "notaCredito.infoTributaria.contribuyenteRimpe")
    if not regimen:
        regimen = "General"

    obligado_raw = first_text(nota_credito_root, "notaCredito.infoNotaCredito.obligadoContabilidad")
    obligado = obligado_map.get((obligado_raw or "").upper(), obligado_raw)

    return {
        "direccion": first_text(nota_credito_root, "notaCredito.infoTributaria.dirMatriz"),
        "direccion_estab": first_text(nota_credito_root, "notaCredito.infoNotaCredito.dirEstablecimiento"),
        "nombre_comercial": first_text(nota_credito_root, "notaCredito.infoTributaria.nombreComercial"),
        "razon_social": first_text(nota_credito_root, "notaCredito.infoTributaria.razonSocial"),
        "regimen": regimen,
        "obligado_contabilidad": obligado,
    }
