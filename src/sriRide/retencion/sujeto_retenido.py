from __future__ import annotations

from lxml import etree

from .xml_utils import first_text


def construir_sujeto_retenido_contexto(retencion_root: etree._Element) -> dict:
    return {
        "razon_social": first_text(retencion_root, "comprobanteRetencion.infoCompRetencion.razonSocialSujetoRetenido"),
        "identificacion": first_text(retencion_root, "comprobanteRetencion.infoCompRetencion.identificacionSujetoRetenido"),
        "fecha_emision": first_text(retencion_root, "comprobanteRetencion.infoCompRetencion.fechaEmision"),
    }
