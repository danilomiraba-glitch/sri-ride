from __future__ import annotations

from lxml import etree

from .xml_utils import first_text, join_values


def construir_doc_contexto(retencion_root: etree._Element) -> dict:
    ambiente_map = {
        "1": "Pruebas",
        "2": "Producción",
    }
    tipo_emision_map = {
        "1": "Normal",
        "2": "Indisponibilidad del Sistema",
    }

    numero = join_values(
        [
            first_text(retencion_root, "comprobanteRetencion.infoTributaria.estab"),
            first_text(retencion_root, "comprobanteRetencion.infoTributaria.ptoEmi"),
            first_text(retencion_root, "comprobanteRetencion.infoTributaria.secuencial"),
        ],
        separator=" - ",
    )

    ambiente_codigo = first_text(retencion_root, "comprobanteRetencion.infoTributaria.ambiente")
    tipo_emision_codigo = first_text(retencion_root, "comprobanteRetencion.infoTributaria.tipoEmision")

    fecha_autorizacion = first_text(
        retencion_root,
        "comprobanteRetencion.extensions.extension.StringField",
        attr_name="name",
        attr_value="Fecha_autorizacion",
    )
    numero_autorizacion = first_text(
        retencion_root,
        "comprobanteRetencion.extensions.extension.StringField",
        attr_name="name",
        attr_value="Numero_autorizacion",
    )

    return {
        "ruc": first_text(retencion_root, "comprobanteRetencion.infoTributaria.ruc"),
        "numero": numero,
        "ambiente": ambiente_map.get(ambiente_codigo or "", ambiente_codigo),
        "tipo_emision": tipo_emision_map.get(tipo_emision_codigo or "", tipo_emision_codigo),
        "fecha_autorizacion": fecha_autorizacion,
        "numero_autorizacion": numero_autorizacion,
        "clave_acceso": first_text(retencion_root, "comprobanteRetencion.infoTributaria.claveAcceso"),
        "cntrbynte_esp": first_text(retencion_root, "comprobanteRetencion.infoCompRetencion.contribuyenteEspecial"),
        "agent_retencn": first_text(retencion_root, "comprobanteRetencion.infoTributaria.agenteRetencion"),
    }
