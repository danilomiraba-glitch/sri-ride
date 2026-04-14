from __future__ import annotations

from lxml import etree

from .xml_utils import first_text_from, walk_path_nodes


def construir_producto_contexto(nota_debito_root: etree._Element) -> dict:
    motivo_nodes = walk_path_nodes(nota_debito_root, "notaDebito.motivos.motivo")
    items: list[dict] = []

    for motivo_node in motivo_nodes:
        items.append(
            {
                "motivo": first_text_from(motivo_node, "razon"),
                "valor": first_text_from(motivo_node, "valor"),
            }
        )

    return {
        "items": items,
    }

