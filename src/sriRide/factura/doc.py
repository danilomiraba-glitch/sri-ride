from __future__ import annotations

from lxml import etree

from .xml_utils import first_text, join_values


def construir_doc_contexto(factura_root: etree._Element) -> dict:
    """
    Construye el bloque `doc` según la intención de `spec-doc.yml`.
    No valida reglas fiscales; solo transforma XML -> contexto para Jinja2.
    """
    ambiente_map = {
        "2": "Producción",
        "1": "Pruebas",
    }
    tipo_emision_map = {
        "1": "Normal",
        "2": "Indisponibilidad del Sistema",
    }

    numero = join_values(
        [
            first_text(factura_root, "factura.infoTributaria.estab"),
            first_text(factura_root, "factura.infoTributaria.ptoEmi"),
            first_text(factura_root, "factura.infoTributaria.secuencial"),
        ],
        separator=" - ",
    )

    ambiente_codigo = first_text(factura_root, "factura.infoTributaria.ambiente")
    tipo_emision_codigo = first_text(factura_root, "factura.infoTributaria.tipoEmision")

    fecha_autorizacion = first_text(
        factura_root,
        "factura.extensions.extension.StringField",
        attr_name="name",
        attr_value="Fecha_autorizacion",
    )
    numero_autorizacion = first_text(
        factura_root,
        "factura.extensions.extension.StringField",
        attr_name="name",
        attr_value="Numero_autorizacion",
    )

    return {
        "ruc": first_text(factura_root, "factura.infoTributaria.ruc"),
        "numero": numero,
        "ambiente": ambiente_map.get(ambiente_codigo or "", ambiente_codigo),
        "tipo_emision": tipo_emision_map.get(tipo_emision_codigo or "", tipo_emision_codigo),
        "fecha_autorizacion": fecha_autorizacion,
        "numero_autorizacion": numero_autorizacion,
        "clave_acceso": first_text(factura_root, "factura.infoTributaria.claveAcceso"),
        "cntrbynte_esp": first_text(factura_root, "factura.infoFactura.contribuyenteEspecial"),
        "agent_retencn": first_text(factura_root, "factura.infoTributaria.agenteRetencion"),
    }
