from __future__ import annotations

from lxml import etree

from .xml_utils import first_text_from, walk_path_nodes, walk_relative_nodes


def construir_destinatario_contexto(guia_root: etree._Element) -> dict:
    tipo_documento_map = {
        "01": "FACTURA",
        "03": "LIQUIDACION DE COMPRA",
        "04": "NOTA DE CREDITO",
        "05": "NOTA DE DEBITO",
        "06": "GUIA DE REMISION",
        "07": "COMPROBANTE DE RETENCION",
    }

    destinatario_nodes = walk_path_nodes(guia_root, "guiaRemision.destinatarios.destinatario")
    items: list[dict] = []

    for destinatario_node in destinatario_nodes:
        tipo_doc_codigo = first_text_from(destinatario_node, "codDocSustento")
        tipo_doc_label = tipo_documento_map.get(tipo_doc_codigo or "", tipo_doc_codigo)

        documento_aduanero = first_text_from(destinatario_node, "docAduaneroUnico")
        if not documento_aduanero:
            documento_aduanero = "NO APLICA"

        cod_establecimiento_destino = first_text_from(destinatario_node, "codEstabDestino") or ""
        detalles = _construir_detalles_destinatario(destinatario_node)

        items.append(
            {
                "numero_documento": first_text_from(destinatario_node, "numDocSustento"),
                "tipo_documento": tipo_doc_label,
                "fecha_emision": first_text_from(destinatario_node, "fechaEmisionDocSustento"),
                "numero_autorizacion": first_text_from(destinatario_node, "numAutDocSustento"),
                "motivo_traslado": first_text_from(destinatario_node, "motivoTraslado"),
                "destino": first_text_from(destinatario_node, "dirDestinatario"),
                "identificacion": first_text_from(destinatario_node, "identificacionDestinatario"),
                "razon_social": first_text_from(destinatario_node, "razonSocialDestinatario"),
                "documento_aduanero": documento_aduanero,
                "cod_establecimiento_destino": cod_establecimiento_destino,
                "ruta": first_text_from(destinatario_node, "ruta"),
                "detalles": detalles,
            }
        )

    return {
        "items": items,
    }


def _construir_detalles_destinatario(destinatario_node: etree._Element) -> list[dict]:
    detalle_nodes = walk_relative_nodes(destinatario_node, "detalles.detalle")
    detalles: list[dict] = []

    for detalle_node in detalle_nodes:
        detalles.append(
            {
                "codigo": first_text_from(detalle_node, "codigoInterno"),
                "descripcion": first_text_from(detalle_node, "descripcion"),
                "codigo_secundario": first_text_from(detalle_node, "codigoAdicional") or "",
                "cantidad": first_text_from(detalle_node, "cantidad"),
                "detalle_adicional": _detalle_adicional_compuesto(detalle_node) or "",
            }
        )

    return detalles


def _detalle_adicional_compuesto(detalle_node: etree._Element) -> str | None:
    det_adicional_nodes = walk_relative_nodes(detalle_node, "detallesAdicionales.detAdicional")
    if not det_adicional_nodes:
        return None

    partes: list[str] = []
    for node in det_adicional_nodes:
        nombre = (node.get("nombre") or "").strip()
        valor = (node.get("valor") or "").strip()

        if not nombre:
            nombre = first_text_from(node, "nombre") or ""
        if not valor:
            valor = first_text_from(node, "valor") or (node.text or "").strip()

        if nombre and valor:
            partes.append(f"{nombre}: {valor}")
        elif valor:
            partes.append(valor)
        elif nombre:
            partes.append(nombre)

    if not partes:
        return None
    return ", ".join(partes)
