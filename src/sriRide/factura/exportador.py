from __future__ import annotations

from lxml import etree

from .xml_utils import first_text


def construir_exportador_contexto(factura_root: etree._Element) -> dict:
    """
    Construye el bloque `exportador` según `spec-exportador.yml`.
    """
    return {
        "incoterm": first_text(factura_root, "factura.infoFactura.incoTermFactura"),
        "lugar_incoterm": first_text(factura_root, "factura.infoFactura.lugarIncoTerm"),
        "incoterm_total": first_text(factura_root, "factura.infoFactura.incoTermTotalSinImpuestos"),
        "pais_origen": first_text(factura_root, "factura.infoFactura.paisOrigen"),
        "puerto_embarque": first_text(factura_root, "factura.infoFactura.puertoEmbarque"),
        "puerto_destino": first_text(factura_root, "factura.infoFactura.puertoDestino"),
        "pais_destino": first_text(factura_root, "factura.infoFactura.paisDestino"),
        "pais_adquisicion": first_text(factura_root, "factura.infoFactura.paisAdquisicion"),
        "flete_internacional": first_text(factura_root, "factura.infoFactura.fleteInternacional"),
        "seguro_internacional": first_text(factura_root, "factura.infoFactura.seguroInternacional"),
        "gastos_aduaneros": first_text(factura_root, "factura.infoFactura.gastosAduaneros"),
        "gastos_transporte_otros": first_text(factura_root, "factura.infoFactura.gastosTransporteOtros"),
    }
