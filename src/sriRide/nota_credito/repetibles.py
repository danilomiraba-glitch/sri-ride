from __future__ import annotations

from lxml import etree

from .xml_utils import first_text_from, walk_path_nodes


def construir_info_adicional_contexto(nota_credito_root: etree._Element) -> dict:
    campo_nodes = walk_path_nodes(nota_credito_root, "notaCredito.infoAdicional.campoAdicional")
    campos: list[dict] = []

    for campo_node in campo_nodes:
        valor = (campo_node.text or "").strip()
        if not valor:
            valor = first_text_from(campo_node, "valor") or ""
        if valor:
            campos.append({"campo_adicional": valor})

    return {
        "campos": campos,
    }
