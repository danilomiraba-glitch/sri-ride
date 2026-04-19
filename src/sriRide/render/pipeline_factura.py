from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .html_renderer import (
    DEFAULT_TEMPLATE_DIR,
    DEFAULT_TEMPLATE_NAME,
    GUIA_REMISION_TEMPLATE_DIR,
    GUIA_REMISION_TEMPLATE_NAME,
    NOTA_CREDITO_TEMPLATE_DIR,
    NOTA_CREDITO_TEMPLATE_NAME,
    NOTA_DEBITO_TEMPLATE_DIR,
    NOTA_DEBITO_TEMPLATE_NAME,
    RETENCION_TEMPLATE_DIR,
    RETENCION_TEMPLATE_NAME,
    render_html,
)
from .pdf_renderer import render_pdf_desde_html


ANEXO_TEMPLATE_BY_CODIGO = {
    "guiaRemision": "anexo_remision.html",
    "exportacion": "anexo_exportador.html",
    "reembolsos": "anexo_reembolso.html",
}


@dataclass
class RenderFacturaResultado:
    output_pdf: Path
    html: str
    contexto: dict[str, Any]
    preproceso: Any


@dataclass
class RenderHtmlParte:
    clave: str
    template_name: str
    html: str
    orden: int


@dataclass
class RenderHtmlSriResultado:
    html: str
    partes_html: list[RenderHtmlParte]
    contexto: dict[str, Any]
    preproceso: Any
    template_dir: Path
    template_name: str


async def render_html_desde_xml_sri(
    xml_input: str | bytes | Path,
    *,
    tipo_esperado: str | None = None,
    template_dir: str | Path | None = None,
    template_name: str | None = None,
    logo_input: str | bytes | Path | None = None,
) -> RenderHtmlSriResultado:
    from sriRide.contexto_sri_router import construir_contexto_sri_autorizado_async

    contexto, barcode_b64, pre = await construir_contexto_sri_autorizado_async(xml_input)

    if tipo_esperado is not None and pre.tipo_comprobante != tipo_esperado:
        raise ValueError(
            f"El XML corresponde a '{pre.tipo_comprobante}' y no a '{tipo_esperado}'."
        )

    if logo_input is not None:
        try:
            from sriRide.preproceso import procesar_logo_para_plantilla
        except ModuleNotFoundError:  # Compatibilidad cuando PYTHONPATH=src
            from sriRide.preproceso import procesar_logo_para_plantilla

        logo = await asyncio.to_thread(procesar_logo_para_plantilla, logo_input)
        contexto.setdefault("assets", {})
        contexto["assets"]["logo_png_b64"] = logo.data_uri.split(",", 1)[1]

    tpl_dir, tpl_name = _resolver_template(pre.tipo_comprobante, template_dir, template_name)
    partes_html = _render_html_partes(
        contexto=contexto,
        barcode_b64=barcode_b64 or "",
        tipo_comprobante=pre.tipo_comprobante,
        template_dir=tpl_dir,
        template_name=tpl_name,
    )

    if not partes_html:
        raise ValueError("No se pudo generar ningun HTML para el comprobante.")

    html = partes_html[0].html
    return RenderHtmlSriResultado(
        html=html,
        partes_html=partes_html,
        contexto=contexto,
        preproceso=pre,
        template_dir=tpl_dir,
        template_name=tpl_name,
    )


async def render_factura_pdf_desde_xml_sri(
    xml_input: str | bytes | Path,
    *,
    output_pdf: str | Path,
    template_dir: str | Path | None = None,
    template_name: str | None = None,
    logo_input: str | bytes | Path | None = None,
) -> RenderFacturaResultado:
    html_result = await render_html_desde_xml_sri(
        xml_input,
        template_dir=template_dir,
        template_name=template_name,
        logo_input=logo_input,
    )

    output_path = await render_pdf_desde_html(
        html_result.html,
        output_pdf=output_pdf,
        base_dir=html_result.template_dir,
        html_parts=html_result.partes_html,
    )

    return RenderFacturaResultado(
        output_pdf=output_path,
        html=html_result.html,
        contexto=html_result.contexto,
        preproceso=html_result.preproceso,
    )


def _resolver_template(
    tipo_comprobante: str,
    template_dir: str | Path | None,
    template_name: str | None,
) -> tuple[Path, str]:
    if template_dir is not None:
        resolved_dir = Path(template_dir)
        resolved_name = template_name or DEFAULT_TEMPLATE_NAME
        return resolved_dir, resolved_name

    if tipo_comprobante == "guiaRemision":
        return GUIA_REMISION_TEMPLATE_DIR, (template_name or GUIA_REMISION_TEMPLATE_NAME)

    if tipo_comprobante == "notaCredito":
        return NOTA_CREDITO_TEMPLATE_DIR, (template_name or NOTA_CREDITO_TEMPLATE_NAME)

    if tipo_comprobante == "notaDebito":
        return NOTA_DEBITO_TEMPLATE_DIR, (template_name or NOTA_DEBITO_TEMPLATE_NAME)

    if tipo_comprobante == "comprobanteRetencion":
        return RETENCION_TEMPLATE_DIR, (template_name or RETENCION_TEMPLATE_NAME)

    return DEFAULT_TEMPLATE_DIR, (template_name or DEFAULT_TEMPLATE_NAME)


def _render_html_partes(
    *,
    contexto: dict[str, Any],
    barcode_b64: str,
    tipo_comprobante: str,
    template_dir: Path,
    template_name: str,
) -> list[RenderHtmlParte]:
    if tipo_comprobante != "factura":
        html = render_html(
            contexto,
            barcode_b64,
            template_dir=template_dir,
            template_name=template_name,
        )
        return [
            RenderHtmlParte(
                clave="principal",
                template_name=template_name,
                html=html,
                orden=0,
            )
        ]

    anexos_ctx = contexto.get("anexos", {})
    if not isinstance(anexos_ctx, dict):
        anexos_ctx = {}

    anexos_partes = anexos_ctx.get("partes", [])
    if not isinstance(anexos_partes, list):
        anexos_partes = []

    total_anexos = int(anexos_ctx.get("cantidad", len(anexos_partes)))
    partes_html: list[RenderHtmlParte] = []

    contexto_principal = dict(contexto)
    contexto_principal["anexos_total"] = total_anexos
    html_principal = render_html(
        contexto_principal,
        barcode_b64,
        template_dir=template_dir,
        template_name=template_name,
    )
    partes_html.append(
        RenderHtmlParte(
            clave="principal",
            template_name=template_name,
            html=html_principal,
            orden=0,
        )
    )

    for anexo_info in anexos_partes:
        if not isinstance(anexo_info, dict):
            continue
        codigo = str(anexo_info.get("codigo", "")).strip()
        template_anexo = ANEXO_TEMPLATE_BY_CODIGO.get(codigo)
        if not template_anexo:
            continue

        indice = int(anexo_info.get("indice", 0) or 0)
        if indice <= 0:
            indice = len(partes_html)

        contexto_anexo = dict(contexto)
        contexto_anexo["anexo"] = {
            "code": codigo,
            "index": indice,
            "total": total_anexos,
        }
        contexto_anexo["anexos_total"] = total_anexos
        html_anexo = render_html(
            contexto_anexo,
            barcode_b64,
            template_dir=template_dir,
            template_name=template_anexo,
        )

        partes_html.append(
            RenderHtmlParte(
                clave=f"anexo_{codigo}",
                template_name=template_anexo,
                html=html_anexo,
                orden=10 + indice,
            )
        )

    return sorted(partes_html, key=lambda parte: parte.orden)
