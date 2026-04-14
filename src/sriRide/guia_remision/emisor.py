from __future__ import annotations

from lxml import etree

from .xml_utils import first_text


def construir_emisor_contexto(guia_root: etree._Element) -> dict:
    obligado_map = {
        "SI": "SI",
        "NO": "NO",
    }

    regimen = first_text(guia_root, "guiaRemision.infoTributaria.contribuyenteRimpe")
    if not regimen:
        regimen = "General"

    obligado_raw = first_text(guia_root, "guiaRemision.infoGuiaRemision.obligadoContabilidad")
    obligado = obligado_map.get((obligado_raw or "").upper(), obligado_raw)

    return {
        "nombre_comercial": first_text(guia_root, "guiaRemision.infoTributaria.nombreComercial"),
        "direccion": first_text(guia_root, "guiaRemision.infoTributaria.dirMatriz"),
        "direccion_estab": first_text(guia_root, "guiaRemision.infoGuiaRemision.dirEstablecimiento"),
        "razon_social": first_text(guia_root, "guiaRemision.infoTributaria.razonSocial"),
        "regimen": regimen,
        "obligado_contabilidad": obligado,
    }
