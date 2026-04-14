from __future__ import annotations

import base64
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

DEFAULT_TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "template" / "factura"
DEFAULT_TEMPLATE_NAME = "factura.html"
GUIA_REMISION_TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "template" / "guia-remision"
GUIA_REMISION_TEMPLATE_NAME = "guia-remision.html"
NOTA_CREDITO_TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "template" / "nota-credito"
NOTA_CREDITO_TEMPLATE_NAME = "nota-credito.html"
NOTA_DEBITO_TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "template" / "nota_debito"
NOTA_DEBITO_TEMPLATE_NAME = "nota-debito.html"
RETENCION_TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "template" / "retencion"
RETENCION_TEMPLATE_NAME = "retencion.html"


def render_html(
    contexto: dict,
    *,
    template_dir: str | Path,
    template_name: str,
) -> str:
    template_path = Path(template_dir)
    env = Environment(
        loader=FileSystemLoader(str(template_path)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_name)
    html = template.render(**contexto)
    return _incrustar_fuentes_en_html(html, template_path=template_path)


def render_factura_html(
    contexto: dict,
    *,
    template_dir: str | Path | None = None,
    template_name: str = DEFAULT_TEMPLATE_NAME,
) -> str:
    template_path = Path(template_dir) if template_dir else DEFAULT_TEMPLATE_DIR
    return render_html(
        contexto,
        template_dir=template_path,
        template_name=template_name,
    )


def _incrustar_fuentes_en_html(html: str, *, template_path: Path) -> str:
    font_url_re = re.compile(
        r"url\((['\"]?)((?:\.\./)*fonts/[^)'\"]+\.(?:woff2|woff|ttf|otf))\1\)"
    )
    font_rel_paths = {m.group(2) for m in font_url_re.finditer(html)}
    if not font_rel_paths:
        return html

    for rel_path in sorted(font_rel_paths):
        font_file = template_path / rel_path
        if not font_file.exists():
            continue

        font_bytes = font_file.read_bytes()
        mime = "font/woff2"
        css_format = "woff2"

        b64 = base64.b64encode(font_bytes).decode("ascii")
        data_uri = f"data:{mime};base64,{b64}"

        # Alinea el descriptor CSS con el formato incrustado para esta fuente.
        rel_path_escaped = re.escape(rel_path)
        pattern = re.compile(
            rf"url\((['\"]?){rel_path_escaped}\1\)\s*format\((['\"])[^'\"]+\2\)"
        )
        html = pattern.sub(
            lambda m: f"url('{data_uri}') format('{css_format}')",
            html,
        )
        html = html.replace(f"url('{rel_path}')", f"url('{data_uri}')")
        html = html.replace(f'url("{rel_path}")', f'url("{data_uri}")')
        html = html.replace(f"url({rel_path})", f"url({data_uri})")

        html = html.replace(f"href=\"{rel_path}\"", f"href=\"{data_uri}\"")
        html = html.replace(f"href='{rel_path}'", f"href='{data_uri}'")

    preload_font_re = re.compile(
        r"<link\b[^>]*rel=(['\"])preload\1[^>]*as=(['\"])font\2[^>]*>",
        re.IGNORECASE,
    )
    html = preload_font_re.sub("", html)

    return html
