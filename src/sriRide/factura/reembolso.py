from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from lxml import etree

from .xml_utils import first_text, first_text_from, join_values, walk_path_nodes, walk_relative_nodes


Q2 = Decimal("0.01")


def construir_reembolso_contexto(factura_root: etree._Element) -> dict:
    """
    Construye el bloque `reembolso` según `spec-reembolso.yml`.
    Incluye ítems repetibles y agregados.
    """
    detalle_nodes = walk_path_nodes(factura_root, "factura.reembolsos.reembolsoDetalle")
    items: list[dict] = []

    subtotal_reembolso_sum = Decimal("0")
    total_impuestos_sum = Decimal("0")

    for detalle_node in detalle_nodes:
        numero_comprobante = join_values(
            [
                first_text_from(detalle_node, "estabDocReembolso"),
                first_text_from(detalle_node, "ptoEmiDocReembolso"),
                first_text_from(detalle_node, "secuencialDocReembolso"),
            ],
            separator="-",
        )

        subtotal_item = _sum_relative_path(
            detalle_node,
            "detalleImpuestos.detalleImpuesto.baseImponibleReembolso",
        )
        impuestos_item = _sum_relative_path(
            detalle_node,
            "detalleImpuestos.detalleImpuesto.impuestoReembolso",
        )
        total_item = (subtotal_item or Decimal("0")) + (impuestos_item or Decimal("0"))

        if subtotal_item is not None:
            subtotal_reembolso_sum += subtotal_item
        if impuestos_item is not None:
            total_impuestos_sum += impuestos_item

        items.append(
            {
                "ruc_reembolso": first_text_from(detalle_node, "identificacionProveedorReembolso"),
                "fecha_emision": first_text_from(detalle_node, "fechaEmisionDocReembolso"),
                "numero_autorizacion": first_text_from(detalle_node, "numeroautorizacionDocReembolso"),
                "numero_comprobante": numero_comprobante,
                "subtotal_reembolso": _fmt_decimal(subtotal_item),
                "total_impuestos": _fmt_decimal(impuestos_item),
                "total_reembolso": _fmt_decimal(total_item),
            }
        )

    total_comprobantes = len(detalle_nodes)
    subtotal_reembolso = _fmt_decimal(subtotal_reembolso_sum if detalle_nodes else None)
    total_impuestos = _fmt_decimal(total_impuestos_sum if detalle_nodes else None)
    total_reembolso = _fmt_decimal((subtotal_reembolso_sum + total_impuestos_sum) if detalle_nodes else None)

    return {
        "items": items,
        "ruc_reembolso": items[0]["ruc_reembolso"] if items else None,
        "fecha_emision": items[0]["fecha_emision"] if items else None,
        "numero_autorizacion": items[0]["numero_autorizacion"] if items else None,
        "numero_comprobante": items[0]["numero_comprobante"] if items else None,
        "total_base_reembolsos": first_text(factura_root, "factura.infoFactura.totalBaseImponibleReembolso"),
        "total_impuestos_reembolsos": first_text(factura_root, "factura.infoFactura.totalImpuestoReembolso"),
        "total_todos_reembolsos": first_text(factura_root, "factura.infoFactura.totalComprobantesReembolso"),
        "total_comprobantes": str(total_comprobantes) if detalle_nodes else None,
        "subtotal_reembolso": subtotal_reembolso,
        "total_impuestos": total_impuestos,
        "total_reembolso": total_reembolso,
    }


def _sum_relative_path(node: etree._Element, dot_path: str) -> Decimal | None:
    nodes = walk_relative_nodes(node, dot_path)
    total = Decimal("0")
    found = False

    for current_node in nodes:
        value = _to_decimal((current_node.text or "").strip())
        if value is None:
            continue
        total += value
        found = True

    if not found:
        return None
    return total


def _to_decimal(value: str | None) -> Decimal | None:
    if value is None:
        return None
    clean = value.strip().replace(",", "")
    if not clean:
        return None
    try:
        return Decimal(clean)
    except (InvalidOperation, ValueError):
        return None


def _fmt_decimal(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return str(value.quantize(Q2, rounding=ROUND_HALF_UP))
