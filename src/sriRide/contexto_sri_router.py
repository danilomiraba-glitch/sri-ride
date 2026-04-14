from __future__ import annotations

import asyncio
from typing import Callable

try:
    from src.sriRide.factura import construir_contexto_desde_xml
    from src.sriRide.guia_remision import construir_contexto_desde_xml as construir_contexto_guia_remision
    from src.sriRide.nota_debito.index import construir_contexto_desde_xml as construir_contexto_nota_debito
    from src.sriRide.nota_credito.index import construir_contexto_desde_xml as construir_contexto_nota_credito
    from src.sriRide.retencion.index import construir_contexto_desde_xml as construir_contexto_retencion
    from src.sriRide.preproceso.barcode_sri import generar_barcode_svg_b64
    from src.sriRide.preproceso.preproceso_sri import (
        SriPreprocesoResultado,
        preprocesar_xml_autorizado_sri,
        preprocesar_xml_autorizado_sri_async,
    )
except ModuleNotFoundError:  # Compatibilidad cuando PYTHONPATH=src
    from sriRide.factura import construir_contexto_desde_xml
    from sriRide.guia_remision import construir_contexto_desde_xml as construir_contexto_guia_remision
    from sriRide.nota_debito.index import construir_contexto_desde_xml as construir_contexto_nota_debito
    from sriRide.nota_credito.index import construir_contexto_desde_xml as construir_contexto_nota_credito
    from sriRide.retencion.index import construir_contexto_desde_xml as construir_contexto_retencion
    from sriRide.preproceso.barcode_sri import generar_barcode_svg_b64
    from sriRide.preproceso.preproceso_sri import (
        SriPreprocesoResultado,
        preprocesar_xml_autorizado_sri,
        preprocesar_xml_autorizado_sri_async,
    )


def construir_contexto_sri_autorizado(xml_input) -> tuple[dict, SriPreprocesoResultado]:
    """
    Router general de contexto por tipo de comprobante SRI.
    """
    pre = preprocesar_xml_autorizado_sri(xml_input)
    contexto = _construir_contexto_por_tipo(pre)
    clave_acceso = (contexto.get("doc", {}) or {}).get("clave_acceso")
    if clave_acceso:
        contexto.setdefault("assets", {})
        contexto["assets"]["barcode_svg_b64"] = generar_barcode_svg_b64(clave_acceso)
    return contexto, pre


async def construir_contexto_sri_autorizado_async(xml_input) -> tuple[dict, SriPreprocesoResultado]:
    pre = await preprocesar_xml_autorizado_sri_async(xml_input)
    contexto = await asyncio.to_thread(_construir_contexto_por_tipo, pre)
    clave_acceso = (contexto.get("doc", {}) or {}).get("clave_acceso")
    if clave_acceso:
        contexto.setdefault("assets", {})
        contexto["assets"]["barcode_svg_b64"] = await asyncio.to_thread(generar_barcode_svg_b64, clave_acceso)
    return contexto, pre


def _construir_contexto_por_tipo(pre: SriPreprocesoResultado) -> dict:
    def _build_factura() -> dict:
        if pre.factura_root is None:
            raise ValueError("Preproceso inconsistente: tipo=factura sin factura_root.")
        return construir_contexto_desde_xml(pre.factura_root)

    def _build_guia_remision() -> dict:
        if pre.tipo_comprobante != "guiaRemision":
            raise ValueError("Preproceso inconsistente: tipo distinto para guia de remision.")
        return construir_contexto_guia_remision(pre.comprobante_root)

    def _build_retencion() -> dict:
        if pre.tipo_comprobante != "comprobanteRetencion":
            raise ValueError("Preproceso inconsistente: tipo distinto para retencion.")
        return construir_contexto_retencion(pre.comprobante_root)

    def _build_nota_credito() -> dict:
        if pre.tipo_comprobante != "notaCredito":
            raise ValueError("Preproceso inconsistente: tipo distinto para nota de credito.")
        return construir_contexto_nota_credito(pre.comprobante_root)

    def _build_nota_debito() -> dict:
        if pre.tipo_comprobante != "notaDebito":
            raise ValueError("Preproceso inconsistente: tipo distinto para nota de debito.")
        return construir_contexto_nota_debito(pre.comprobante_root)

    builders: dict[str, Callable[[], dict]] = {
        "factura": _build_factura,
        "guiaRemision": _build_guia_remision,
        "comprobanteRetencion": _build_retencion,
        "notaCredito": _build_nota_credito,
        "notaDebito": _build_nota_debito,
    }

    builder = builders.get(pre.tipo_comprobante)
    if builder is None:
        raise NotImplementedError(
            f"Tipo de comprobante aun no soportado para contexto: {pre.tipo_comprobante}"
        )
    return builder()
