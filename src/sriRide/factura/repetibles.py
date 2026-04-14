from __future__ import annotations

from lxml import etree

from .xml_utils import first_text_from, walk_path_nodes


def construir_pago_contexto(factura_root: etree._Element) -> dict:
    """
    Construye el bloque `pago` según `spec-pagos.yml`.
    Repetible: factura.infoFactura.pagos.pago
    """
    forma_pago_map = {
        "01": "Sin utilización del sistema financiero",
        "15": "Compensación de deudas",
        "16": "Tarjeta de débito",
        "17": "Dinero electrónico",
        "18": "Tarjeta prepago",
        "19": "Tarjeta de crédito",
        "20": "Otros con utilización del sistema financiero",
        "21": "Endoso de títulos",
    }

    pago_nodes = walk_path_nodes(factura_root, "factura.infoFactura.pagos.pago")
    formas: list[dict] = []

    for pago_node in pago_nodes:
        forma_codigo = first_text_from(pago_node, "formaPago")
        forma_label = forma_pago_map.get(forma_codigo or "", forma_codigo)

        plazo = first_text_from(pago_node, "plazo")
        unidad_tiempo = first_text_from(pago_node, "unidadTiempo")

        formas.append(
            {
                "forma_pago": forma_label,
                "valor_pago": first_text_from(pago_node, "total"),
                "plazo": plazo if plazo else "---",
                "unidad_tiempo": unidad_tiempo if unidad_tiempo else "---",
            }
        )

    return {
        "formas": formas,
    }


def construir_info_adicional_contexto(factura_root: etree._Element) -> dict:
    """
    Construye `info_adicional` según `spec-info_adicional.yml`.
    Repetible: factura.infoAdicional.campoAdicional, tomando solo #text.
    """
    campo_nodes = walk_path_nodes(factura_root, "factura.infoAdicional.campoAdicional")
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
