from __future__ import annotations

from lxml import etree

from .xml_utils import first_text, walk_path_nodes, walk_relative_nodes


def construir_documento_contexto(retencion_root: etree._Element) -> dict:
    tipo_documento_map = {
        "01": "FACTURA",
        "03": "LIQUIDACIÓN DE COMPRA",
        "04": "NOTA DE CRÉDITO",
        "05": "NOTA DE DÉBITO",
        "06": "GUÍA DE REMISIÓN",
        "07": "COMPROBANTE DE RETENCIÓN",
    }

    doc_sustento_nodes = walk_path_nodes(retencion_root, "comprobanteRetencion.docsSustento.docSustento")
    items: list[dict] = []

    for doc_node in doc_sustento_nodes:
        tipo_doc_codigo = first_text_from(doc_node, "codDocSustento")
        tipo_doc_label = tipo_documento_map.get(tipo_doc_codigo or "", tipo_doc_codigo)

        detalle_retenciones = _construir_detalle_retencion(doc_node)

        items.append(
            {
                "tipo_documento": tipo_doc_label,
                "numero_autorizacion": first_text_from(doc_node, "numAutDocSustento"),
                "fecha_emision_docsustento": first_text_from(doc_node, "fechaEmisionDocSustento"),
                "ejercicio_fiscal": first_text(
                    retencion_root, "comprobanteRetencion.infoCompRetencion.periodoFiscal"
                ),
                "detalle_retencion": detalle_retenciones,
            }
        )

    return {
        "items": items,
    }


def _construir_detalle_retencion(doc_node: etree._Element) -> list[dict]:
    retencion_nodes = walk_relative_nodes(doc_node, "retenciones.retencion")
    retenciones: list[dict] = []

    codigo_map = {
        "1": "RENTA",
        "2": "IVA",
        "6": "ISD",
        "01": "RENTA",
        "02": "IVA",
        "06": "ISD",
    }

    for retencion_node in retencion_nodes:
        codigo = first_text_from(retencion_node, "codigo")
        codigo_normalizado = (codigo or "").strip()
        if len(codigo_normalizado) == 1 and codigo_normalizado.isdigit():
            codigo_normalizado = codigo_normalizado.zfill(2)
        codigo_label = codigo_map.get(codigo_normalizado, codigo)

        retenciones.append(
            {
                "codigo": codigo_label,
                "base_imponible_retencion": first_text_from(retencion_node, "baseImponible"),
                "porcentaje_retencion": first_text_from(retencion_node, "porcentajeRetener"),
                "valor_retencion": first_text_from(retencion_node, "valorRetenido"),
            }
        )

    return retenciones


def extraer_retenciones_planas(documentos_ctx: dict) -> list[dict]:
    """Extrae una lista plana de todas las retenciones de todos los documentos."""
    retenciones_planas: list[dict] = []

    for doc in documentos_ctx.get("items", []):
        for retencion in doc.get("detalle_retencion", []):
            retenciones_planas.append(retencion)

    return retenciones_planas


def first_text_from(node: etree._Element, dot_path: str) -> str | None:
    parts = [p.strip() for p in dot_path.split(".") if p.strip()]
    if not parts:
        return None

    current: list[etree._Element] = [node]
    for part in parts:
        next_nodes: list[etree._Element] = []
        for current_node in current:
            matches = current_node.xpath(f"./*[local-name()='{part}']")
            next_nodes.extend(matches)
        current = next_nodes
        if not current:
            return None

    for current_node in current:
        text = (current_node.text or "").strip()
        if text:
            return text
    return None
