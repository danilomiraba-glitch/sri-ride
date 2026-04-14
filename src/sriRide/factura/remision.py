from __future__ import annotations

from lxml import etree

from .xml_utils import first_text, first_text_from, walk_path_nodes


def construir_remision_contexto(factura_root: etree._Element) -> dict:
    """
    Construye el bloque `remision` según `spec-remision.yml`.
    """
    return {
        "partida": first_text(factura_root, "factura.infoSustitutivaGuiaRemision.dirPartida"),
        "destinatario": first_text(factura_root, "factura.infoSustitutivaGuiaRemision.dirDestinatario"),
        "placa": first_text(factura_root, "factura.infoSustitutivaGuiaRemision.placa"),
        "transportista": first_text(factura_root, "factura.infoSustitutivaGuiaRemision.razonSocialTransportista"),
        "ruc_transportista": first_text(factura_root, "factura.infoSustitutivaGuiaRemision.rucTransportista"),
        "inicio_transporte": first_text(factura_root, "factura.infoSustitutivaGuiaRemision.fechaIniTransporte"),
        "fin_transporte": first_text(factura_root, "factura.infoSustitutivaGuiaRemision.fechaFinTransporte"),
    }


def construir_destino_contexto(factura_root: etree._Element) -> dict:
    """
    Construye el bloque `destino` (repetible) según `spec-remision.yml`.
    """
    destino_nodes = walk_path_nodes(factura_root, "factura.infoSustitutivaGuiaRemision.destinos.destino")
    items: list[dict] = []

    for idx, destino_node in enumerate(destino_nodes, start=1):
        doc_aduanero = first_text_from(destino_node, "docAduaneroUnico")
        if not doc_aduanero:
            doc_aduanero = "No Aplica"

        items.append(
            {
                "numero": str(idx),
                "motivo_traslado": first_text_from(destino_node, "motivoTraslado"),
                "doc_aduanero": doc_aduanero,
                "cod_establecimiento_destino": first_text_from(destino_node, "codEstabDestino"),
                "ruta_destino": first_text_from(destino_node, "ruta"),
            }
        )

    return {
        "items": items,
    }
