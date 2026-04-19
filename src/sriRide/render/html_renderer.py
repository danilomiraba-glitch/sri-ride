from __future__ import annotations
from pathlib import Path
from jinja2 import Environment, ModuleLoader, select_autoescape

_FONTS_B64: str = (
    Path(__file__).resolve().parents[1] / "template" / "fonts" / "fonts.txt"
).read_text(encoding="ascii").strip()

DEFAULT_TEMPLATE_DIR        = Path(__file__).resolve().parents[1] / "template" / "factura"
DEFAULT_TEMPLATE_NAME       = "factura.html"

GUIA_REMISION_TEMPLATE_DIR  = Path(__file__).resolve().parents[1] / "template" / "guia-remision"
GUIA_REMISION_TEMPLATE_NAME = "guia-remision.html"

NOTA_CREDITO_TEMPLATE_DIR   = Path(__file__).resolve().parents[1] / "template" / "nota-credito"
NOTA_CREDITO_TEMPLATE_NAME  = "nota-credito.html"

NOTA_DEBITO_TEMPLATE_DIR    = Path(__file__).resolve().parents[1] / "template" / "nota_debito"
NOTA_DEBITO_TEMPLATE_NAME   = "nota-debito.html"

RETENCION_TEMPLATE_DIR      = Path(__file__).resolve().parents[1] / "template" / "retencion"
RETENCION_TEMPLATE_NAME     = "retencion.html"


def _make_env(template_path: Path) -> Environment:
    return Environment(
        loader=ModuleLoader(str(template_path)),
        autoescape=select_autoescape(["html", "xml"]),
    )


def _compose_html(body: str, barcode_b64: str, base_template: str) -> str:
    body = body.replace("__BARCODE__", barcode_b64)
    return (
        base_template
        .replace("__FONT-FACE__", _FONTS_B64)
        .replace("__BODY__", body)
    )


def render_html(
    contexto: dict,
    barcode_b64: str,
    *,
    template_dir: str | Path,
    template_name: str,
) -> str:
    template_path = Path(template_dir)
    base_name = template_name.removesuffix(".html") + "_base.html"
    base_template = (template_path / base_name).read_text(encoding="utf-8")

    env = _make_env(template_path)
    body = env.get_template(template_name).render(**contexto)

    return _compose_html(body, barcode_b64, base_template)


def render_factura_html(
    contexto: dict,
    barcode_b64: str,
    *,
    template_dir: str | Path | None = None,
    template_name: str = DEFAULT_TEMPLATE_NAME,
) -> str:
    template_path = Path(template_dir) if template_dir else DEFAULT_TEMPLATE_DIR
    return render_html(
        contexto,
        barcode_b64,
        template_dir=template_path,
        template_name=template_name,
    )