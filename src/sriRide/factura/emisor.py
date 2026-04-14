from __future__ import annotations

from lxml import etree

from .xml_utils import first_text


def construir_emisor_contexto(factura_root: etree._Element) -> dict:
    """
    Construye el bloque `emisor` según la intención de `spec-emisor.yml`.
    """
    obligado_map = {
        "SI": "SI",
        "NO": "NO",
    }

    regimen = first_text(factura_root, "factura.infoTributaria.contribuyenteRimpe")
    if not regimen:
        regimen = "General"

    obligado_raw = first_text(factura_root, "factura.infoFactura.obligadoContabilidad")
    obligado = obligado_map.get((obligado_raw or "").upper(), obligado_raw)

    return {
        "direccion": first_text(factura_root, "factura.infoTributaria.dirMatriz"),
        "direccion_estab": first_text(factura_root, "factura.infoFactura.dirEstablecimiento"),
        "razon_social": first_text(factura_root, "factura.infoTributaria.razonSocial"),
        "regimen": regimen,
        "obligado_contabilidad": obligado,
    }
