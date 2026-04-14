from __future__ import annotations

from .anexos import construir_anexos_contexto
from .cliente import construir_cliente_contexto
from .doc import construir_doc_contexto
from .emisor import construir_emisor_contexto
from .exportador import construir_exportador_contexto
from .producto import construir_producto_contexto
from .reembolso import construir_reembolso_contexto
from .repetibles import construir_info_adicional_contexto, construir_pago_contexto
from .remision import construir_destino_contexto, construir_remision_contexto
from .totales import construir_totales_contexto
from .xml_utils import XmlInput, load_xml_root, walk_path_nodes


def construir_contexto_desde_xml(xml_input: XmlInput) -> dict:
    """
    Punto de entrada llamable para pipeline externo.
    Orquesta módulos y condiciones de activación desde el índice.
    """
    factura_root = load_xml_root(xml_input)

    remision_activa = _exists_path(factura_root, "factura.infoSustitutivaGuiaRemision")
    exportador_activo = _exists_path(factura_root, "factura.infoFactura.comercioExterior")
    reembolso_activo = _exists_path(factura_root, "factura.infoFactura.codDocReembolso")

    remision_ctx = construir_remision_contexto(factura_root) if remision_activa else None
    destino_ctx = construir_destino_contexto(factura_root) if remision_activa else {"items": []}
    exportador_ctx = construir_exportador_contexto(factura_root) if exportador_activo else None
    reembolso_ctx = construir_reembolso_contexto(factura_root) if reembolso_activo else {"items": []}

    producto_ctx = construir_producto_contexto(factura_root)
    producto_items = producto_ctx.get("items", [])
    page_size = "A4" if len(producto_items) >= 10 else "auto"

    anexos_ctx = construir_anexos_contexto(
        remision_activa=remision_activa,
        exportador_activo=exportador_activo,
        reembolso_activo=reembolso_activo,
        destino_items=destino_ctx.get("items", []),
        gastos_exportacion_items=_gastos_exportacion_items(exportador_ctx),
        reembolso_items=reembolso_ctx.get("items", []),
    )

    return {
        "doc": construir_doc_contexto(factura_root),
        "emisor": construir_emisor_contexto(factura_root),
        "cliente": construir_cliente_contexto(factura_root),
        "producto": producto_ctx,
        "layout": {
            "page_size": page_size,
        },
        "pago": construir_pago_contexto(factura_root),
        "anexos": anexos_ctx,
        "info_adicional": construir_info_adicional_contexto(factura_root),
        "totales": construir_totales_contexto(factura_root),
        "remision": remision_ctx,
        "destino": destino_ctx,
        "exportador": exportador_ctx,
        "reembolso": reembolso_ctx,
    }


def _exists_path(factura_root, dot_path: str) -> bool:
    return bool(walk_path_nodes(factura_root, dot_path))


def _gastos_exportacion_items(exportador_ctx: dict | None) -> list[dict]:
    if not exportador_ctx:
        return []
    return [
        {"etiqueta": "Flete Internacional", "valor": exportador_ctx.get("flete_internacional")},
        {"etiqueta": "Seguro Internacional", "valor": exportador_ctx.get("seguro_internacional")},
        {"etiqueta": "Gastos Aduaneros", "valor": exportador_ctx.get("gastos_aduaneros")},
        {"etiqueta": "Gastos de Transporte", "valor": exportador_ctx.get("gastos_transporte_otros")},
    ]
