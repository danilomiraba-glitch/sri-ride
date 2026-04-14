from __future__ import annotations

from lxml import etree

from .xml_utils import first_text


def construir_cliente_contexto(factura_root: etree._Element) -> dict:
    """
    Construye el bloque `cliente` según la intención de `spec-cliente.yml`.
    """
    direccion = first_text(factura_root, "factura.infoFactura.direccionComprador")
    if not direccion:
        direccion = "---"

    return {
        "razon_social": first_text(factura_root, "factura.infoFactura.razonSocialComprador"),
        "identificacion": first_text(factura_root, "factura.infoFactura.identificacionComprador"),
        "direccion": direccion,
        "fecha_emision": first_text(factura_root, "factura.infoFactura.fechaEmision"),
        # Se oculta en plantilla cuando no existe en XML.
        "guia_remision": first_text(factura_root, "factura.infoFactura.guiaRemision"),
        "placa": first_text(factura_root, "factura.infoFactura.placa") or "---",
    }
