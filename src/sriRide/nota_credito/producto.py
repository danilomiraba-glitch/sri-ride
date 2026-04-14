from __future__ import annotations

from lxml import etree

from .xml_utils import first_text_from, walk_path_nodes, walk_relative_nodes


def construir_producto_contexto(nota_credito_root: etree._Element) -> dict:
    detalle_nodes = walk_path_nodes(nota_credito_root, "notaCredito.detalles.detalle")
    items: list[dict] = []

    for detalle in detalle_nodes:
        adiciones = _detalle_adicional_compuesto(detalle)
        items.append(
            {
                "codigo": first_text_from(detalle, "codigoInterno"),
                "descripcion": first_text_from(detalle, "descripcion"),
                "detalle_adicional": adiciones,
                "cantidad": first_text_from(detalle, "cantidad"),
                "precio_unitario": first_text_from(detalle, "precioUnitario"),
                "descuento": first_text_from(detalle, "descuento"),
                "precio_total": first_text_from(detalle, "precioTotalSinImpuesto"),
            }
        )

    return {
        "items": items,
    }


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
