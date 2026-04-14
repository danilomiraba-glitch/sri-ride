from __future__ import annotations

from .documento import construir_documento_contexto, extraer_retenciones_planas
from .doc import construir_doc_contexto
from .emisor import construir_emisor_contexto
from .info_adicional import construir_info_adicional_contexto
from .sujeto_retenido import construir_sujeto_retenido_contexto
from .xml_utils import XmlInput, load_xml_root


def construir_contexto_desde_xml(xml_input: XmlInput) -> dict:
    retencion_root = load_xml_root(xml_input)

    documentos_ctx = construir_documento_contexto(retencion_root)

    return {
        "doc": construir_doc_contexto(retencion_root),
        "emisor": construir_emisor_contexto(retencion_root),
        "sujeto_retenido": construir_sujeto_retenido_contexto(retencion_root),
        "deatalle_documentos": documentos_ctx,
        "deatalle_retencion": {"items": extraer_retenciones_planas(documentos_ctx)},
        "info_adicional": construir_info_adicional_contexto(retencion_root),
    }
