from __future__ import annotations

from .documento import construir_documento_contexto, extraer_retenciones_planas
from .doc import construir_doc_contexto
from .emisor import construir_emisor_contexto
from .info_adicional import construir_info_adicional_contexto
from .normalizer import normalizar_retencion
from .sujeto_retenido import construir_sujeto_retenido_contexto
from .xml_utils import XmlInput


def construir_contexto_desde_xml(xml_input: XmlInput) -> dict:
    normalizado = normalizar_retencion(xml_input)
    documentos_ctx = construir_documento_contexto(normalizado)

    return {
        "doc": construir_doc_contexto(normalizado),
        "emisor": construir_emisor_contexto(normalizado),
        "sujeto_retenido": construir_sujeto_retenido_contexto(normalizado),
        "deatalle_documentos": documentos_ctx,
        "deatalle_retencion": {"items": extraer_retenciones_planas(documentos_ctx)},
        "info_adicional": construir_info_adicional_contexto(normalizado),
    }
