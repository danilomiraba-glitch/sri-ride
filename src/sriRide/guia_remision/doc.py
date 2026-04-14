from __future__ import annotations

from lxml import etree

from .xml_utils import first_text, join_values


def construir_doc_contexto(guia_root: etree._Element) -> dict:
    ambiente_map = {
        "1": "Pruebas",
        "2": "Produccion",
    }
    tipo_emision_map = {
        "1": "Normal",
        "2": "Indisponibilidad del Sistema",
    }

    numero = join_values(
        [
            first_text(guia_root, "guiaRemision.infoTributaria.estab"),
            first_text(guia_root, "guiaRemision.infoTributaria.ptoEmi"),
            first_text(guia_root, "guiaRemision.infoTributaria.secuencial"),
        ],
        separator="-",
    )

    ambiente_codigo = first_text(guia_root, "guiaRemision.infoTributaria.ambiente")
    tipo_emision_codigo = first_text(guia_root, "guiaRemision.infoTributaria.tipoEmision")

    fecha_autorizacion = first_text(
        guia_root,
        "guiaRemision.extensions.extension.StringField",
        attr_name="name",
        attr_value="Fecha_autorizacion",
    )
    numero_autorizacion = first_text(
        guia_root,
        "guiaRemision.extensions.extension.StringField",
        attr_name="name",
        attr_value="Numero_autorizacion",
    )

    return {
        "ruc": first_text(guia_root, "guiaRemision.infoTributaria.ruc"),
        "numero": numero,
        "ambiente": ambiente_map.get(ambiente_codigo or "", ambiente_codigo),
        "tipo_emision": tipo_emision_map.get(tipo_emision_codigo or "", tipo_emision_codigo),
        "fecha_autorizacion": fecha_autorizacion,
        "numero_autorizacion": numero_autorizacion,
        "clave_acceso": first_text(guia_root, "guiaRemision.infoTributaria.claveAcceso"),
        "cntrbynte_esp": first_text(guia_root, "guiaRemision.infoGuiaRemision.contribuyenteEspecial"),
        "agent_retencn": first_text(guia_root, "guiaRemision.infoTributaria.agenteRetencion"),
    }
