from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from lxml import etree

from .xml_utils import first_text, walk_path_nodes


Q2 = Decimal("0.01")


def construir_totales_contexto(nota_credito_root: etree._Element) -> dict:
    impuestos = walk_path_nodes(nota_credito_root, "notaCredito.infoNotaCredito.totalConImpuestos.totalImpuesto")

    subtotal_iva_0 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="0", field="baseImponible")
    subtotal_iva_5 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="5", field="baseImponible")
    subtotal_iva_15 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="4", field="baseImponible")
    subtotal_objeto_exento = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje_in={"6", "7"}, field="baseImponible")

    total_iva_5 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="5", field="valor")
    total_iva_15 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="4", field="valor")

    total_ice = _sum_impuesto_field(impuestos, codigo="3", field="valor")

    return {
        "subtotal_iva_0": _fmt_or_default(subtotal_iva_0, "0.00"),
        "subtotal_iva_5": _fmt_nonzero_decimal(subtotal_iva_5),
        "subtotal_iva_15": _fmt_or_default(subtotal_iva_15, "0.00"),
        "subtotal_objeto_exento": _fmt_or_default(subtotal_objeto_exento, "0.00"),
        "subtotal_general": first_text(nota_credito_root, "notaCredito.infoNotaCredito.totalSinImpuestos"),
        "total_descuento": first_text(nota_credito_root, "notaCredito.infoNotaCredito.totalDescuento"),
        "total_iva_5": _fmt_nonzero_decimal(total_iva_5),
        "total_iva_15": _fmt_nonzero_decimal(total_iva_15),
        "total_ice": _fmt_nonzero_decimal(total_ice),
        "total": first_text(nota_credito_root, "notaCredito.infoNotaCredito.valorModificacion"),
    }


def _sum_impuesto_field(
    impuesto_nodes: list[etree._Element],
    *,
    codigo: str,
    field: str,
    codigo_porcentaje: str | None = None,
    codigo_porcentaje_in: set[str] | None = None,
) -> Decimal | None:
    total = Decimal("0")
    found = False

    for node in impuesto_nodes:
        codigo_nodes = node.xpath("./*[local-name()='codigo']")
        codigo_val = ((codigo_nodes[0].text if codigo_nodes else "") or "").strip()
        if codigo_val != codigo:
            continue

        if codigo_porcentaje is not None or codigo_porcentaje_in is not None:
            cp_nodes = node.xpath("./*[local-name()='codigoPorcentaje']")
            cp_val = ((cp_nodes[0].text if cp_nodes else "") or "").strip()
            if codigo_porcentaje is not None and cp_val != codigo_porcentaje:
                continue
            if codigo_porcentaje_in is not None and cp_val not in codigo_porcentaje_in:
                continue

        field_nodes = node.xpath(f"./*[local-name()='{field}']")
        field_val = ((field_nodes[0].text if field_nodes else "") or "").strip()
        dec = _to_decimal(field_val)
        if dec is None:
            continue
        total += dec
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


def _fmt_nonzero_decimal(value: Decimal | None) -> str | None:
    if value is None:
        return None
    quantized = value.quantize(Q2, rounding=ROUND_HALF_UP)
    if quantized == Decimal("0.00"):
        return None
    return str(quantized)


def _fmt_or_default(value: Decimal | None, default: str) -> str:
    if value is None:
        return default
    return str(value.quantize(Q2, rounding=ROUND_HALF_UP))
