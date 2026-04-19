from __future__ import annotations

from .anexos import construir_anexos_contexto
from .cliente import construir_cliente_contexto
from .doc import construir_doc_contexto
from .emisor import construir_emisor_contexto
from .exportador import construir_exportador_contexto
from .normalizer import normalizar_factura
from .producto import construir_producto_contexto
from .reembolso import construir_reembolso_contexto
from .repetibles import construir_info_adicional_contexto, construir_pago_contexto
from .remision import construir_destino_contexto, construir_remision_contexto
from .totales import construir_totales_contexto


def construir_contexto_desde_xml(factura_obj) -> dict:
    """
    Punto de entrada llamable para pipeline externo con objeto Factura (xsdata).
    Normaliza en una sola pasada y luego arma el contexto para Jinja2.
    """
    normalizado = normalizar_factura(factura_obj)

    remision_activa = normalizado["flags"]["remision_activa"]
    exportador_activo = normalizado["flags"]["exportador_activo"]
    reembolso_activo = normalizado["flags"]["reembolso_activo"]

    remision_ctx = construir_remision_contexto(normalizado) if remision_activa else None
    destino_ctx = construir_destino_contexto(normalizado) if remision_activa else {"items": []}
    exportador_ctx = construir_exportador_contexto(normalizado) if exportador_activo else None
    reembolso_ctx = construir_reembolso_contexto(normalizado) if reembolso_activo else {"items": []}

    producto_ctx = construir_producto_contexto(normalizado)
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
        "doc": construir_doc_contexto(normalizado),
        "emisor": construir_emisor_contexto(normalizado),
        "cliente": construir_cliente_contexto(normalizado),
        "producto": producto_ctx,
        "layout": {
            "page_size": page_size,
        },
        "pago": construir_pago_contexto(normalizado),
        "anexos": anexos_ctx,
        "info_adicional": construir_info_adicional_contexto(normalizado),
        "totales": construir_totales_contexto(normalizado),
        "remision": remision_ctx,
        "destino": destino_ctx,
        "exportador": exportador_ctx,
        "reembolso": reembolso_ctx,
    }


def _gastos_exportacion_items(exportador_ctx: dict | None) -> list[dict]:
    if not exportador_ctx:
        return []
    return [
        {"etiqueta": "Flete Internacional", "valor": exportador_ctx.get("flete_internacional")},
        {"etiqueta": "Seguro Internacional", "valor": exportador_ctx.get("seguro_internacional")},
        {"etiqueta": "Gastos Aduaneros", "valor": exportador_ctx.get("gastos_aduaneros")},
        {"etiqueta": "Gastos de Transporte", "valor": exportador_ctx.get("gastos_transporte_otros")},
    ]
