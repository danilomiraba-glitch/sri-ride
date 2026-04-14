from __future__ import annotations

from lxml import etree

from .xml_utils import first_text


def construir_transportista_contexto(guia_root: etree._Element) -> dict:
    direccion = first_text(guia_root, "guiaRemision.infoGuiaRemision.dirPartida")
    if not direccion:
        direccion = "---"

    return {
        "razon_social": first_text(guia_root, "guiaRemision.infoGuiaRemision.razonSocialTransportista"),
        "identificacion": first_text(guia_root, "guiaRemision.infoGuiaRemision.rucTransportista"),
        "direccion": direccion,
        "fecha_fin": first_text(guia_root, "guiaRemision.infoGuiaRemision.fechaFinTransporte"),
        "fecha_inicio": first_text(guia_root, "guiaRemision.infoGuiaRemision.fechaIniTransporte"),
        "placa": first_text(guia_root, "guiaRemision.infoGuiaRemision.placa"),
    }
