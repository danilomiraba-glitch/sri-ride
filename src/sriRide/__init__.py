import asyncio
import base64
from pathlib import Path
from tempfile import TemporaryDirectory

from .preproceso.preproceso_sri import (
    SriPreprocesoResultado,
    preprocesar_xml_autorizado_sri,
)
from .render.pdf_renderer import render_pdf_desde_html
from .render.pipeline_factura import render_html_desde_xml_sri


class SriRide:
    def __init__(self, mode="html", page=None, page_provider=None):
        if mode not in ("html", "pdf"):
            raise ValueError("mode must be 'html' or 'pdf'")
        if page is not None and page_provider is not None:
            raise ValueError("Usa `page` o `page_provider`, no ambos.")
        self.mode = mode
        self.page = page
        self.page_provider = page_provider

    async def factura(self, xml, logo=None, template_dir=None, template_name=None):
        result = await render_html_desde_xml_sri(
            xml,
            tipo_esperado="factura",
            template_dir=template_dir,
            template_name=template_name,
            logo_input=logo,
        )

        if self.mode == "html":
            return _serializar_partes_html(result.partes_html)
        return await _render_pdf_b64_from_html(
            result.html,
            base_dir=result.template_dir,
            page=self.page,
            page_provider=self.page_provider,
            html_parts=result.partes_html,
        )

    async def guiaremision(self, xml, logo=None, template_dir=None, template_name=None):
        result = await render_html_desde_xml_sri(
            xml,
            tipo_esperado="guiaRemision",
            template_dir=template_dir,
            template_name=template_name,
            logo_input=logo,
        )

        if self.mode == "html":
            return _serializar_partes_html(result.partes_html)
        return await _render_pdf_b64_from_html(
            result.html,
            base_dir=result.template_dir,
            page=self.page,
            page_provider=self.page_provider,
            html_parts=result.partes_html,
        )

    async def retencion(self, xml, logo=None, template_dir=None, template_name=None):
        result = await render_html_desde_xml_sri(
            xml,
            tipo_esperado="comprobanteRetencion",
            template_dir=template_dir,
            template_name=template_name,
            logo_input=logo,
        )

        if self.mode == "html":
            return _serializar_partes_html(result.partes_html)
        return await _render_pdf_b64_from_html(
            result.html,
            base_dir=result.template_dir,
            page=self.page,
            page_provider=self.page_provider,
            html_parts=result.partes_html,
        )

    async def notacredito(self, xml, logo=None, template_dir=None, template_name=None):
        result = await render_html_desde_xml_sri(
            xml,
            tipo_esperado="notaCredito",
            template_dir=template_dir,
            template_name=template_name,
            logo_input=logo,
        )

        if self.mode == "html":
            return _serializar_partes_html(result.partes_html)
        return await _render_pdf_b64_from_html(
            result.html,
            base_dir=result.template_dir,
            page=self.page,
            page_provider=self.page_provider,
            html_parts=result.partes_html,
        )

    async def nota_credito(self, xml, logo=None, template_dir=None, template_name=None):
        return await self.notacredito(
            xml=xml,
            logo=logo,
            template_dir=template_dir,
            template_name=template_name,
        )

    async def notadebito(self, xml, logo=None, template_dir=None, template_name=None):
        result = await render_html_desde_xml_sri(
            xml,
            tipo_esperado="notaDebito",
            template_dir=template_dir,
            template_name=template_name,
            logo_input=logo,
        )

        if self.mode == "html":
            return _serializar_partes_html(result.partes_html)
        return await _render_pdf_b64_from_html(
            result.html,
            base_dir=result.template_dir,
            page=self.page,
            page_provider=self.page_provider,
            html_parts=result.partes_html,
        )

    async def nota_debito(self, xml, logo=None, template_dir=None, template_name=None):
        return await self.notadebito(
            xml=xml,
            logo=logo,
            template_dir=template_dir,
            template_name=template_name,
        )


async def _render_pdf_b64_from_html(
    html: str,
    *,
    base_dir: str | Path,
    page=None,
    page_provider=None,
    html_parts=None,
) -> str:
    with TemporaryDirectory(prefix="sriRide_pdf_") as tmp_dir:
        tmp_pdf = Path(tmp_dir) / "out.pdf"
        output_path = await render_pdf_desde_html(
            html,
            output_pdf=tmp_pdf,
            base_dir=base_dir,
            page=page,
            page_provider=page_provider,
            html_parts=html_parts,
        )
        pdf_bytes = await asyncio.to_thread(Path(output_path).read_bytes)
    return base64.b64encode(pdf_bytes).decode("ascii")


def _serializar_partes_html(partes_html) -> list[dict]:
    return [
        {
            "clave": parte.clave,
            "orden": parte.orden,
            "template_name": parte.template_name,
            "html": parte.html,
        }
        for parte in sorted(partes_html, key=lambda p: p.orden)
    ]


__all__ = [
    "SriRide",
    "SriPreprocesoResultado",
    "preprocesar_xml_autorizado_sri",
]
