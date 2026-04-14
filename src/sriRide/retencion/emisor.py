from __future__ import annotations

from lxml import etree

from .xml_utils import first_text


def construir_emisor_contexto(retencion_root: etree._Element) -> dict:
    obligado_map = {
        "SI": "SI",
        "NO": "NO",
    }

    regimen = first_text(retencion_root, "comprobanteRetencion.infoTributaria.contribuyenteRimpe")
    if not regimen:
        regimen = "General"

    obligado_raw = first_text(retencion_root, "comprobanteRetencion.infoCompRetencion.obligadoContabilidad")
    obligado = obligado_map.get((obligado_raw or "").upper(), obligado_raw)

    return {
        "nombre_comercial": first_text(retencion_root, "comprobanteRetencion.infoTributaria.nombreComercial"),
        "direccion": first_text(retencion_root, "comprobanteRetencion.infoTributaria.dirMatriz"),
        "direccion_estab": first_text(retencion_root, "comprobanteRetencion.infoCompRetencion.dirEstablecimiento"),
        "razon_social": first_text(retencion_root, "comprobanteRetencion.infoTributaria.razonSocial"),
        "regimen": regimen,
        "obligado_contabilidad": obligado,
    }
