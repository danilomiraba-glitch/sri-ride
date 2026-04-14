from __future__ import annotations

import base64
from io import BytesIO

from lxml import etree

SVG_WIDTH = "221"
SVG_HEIGHT = "80"


def generar_barcode_svg_b64(clave_acceso: str) -> str:
    """
    Genera un Code128 en SVG (base64) para la clave de acceso.
    Requiere `python-barcode` instalado.
    """
    if not clave_acceso or not clave_acceso.strip():
        raise ValueError("La clave de acceso es requerida para generar el codigo de barras.")

    svg_bytes = generar_barcode_svg_bytes(clave_acceso.strip())
    return base64.b64encode(svg_bytes).decode("ascii")


def generar_barcode_svg_bytes(clave_acceso: str) -> bytes:
    code128, svg_writer = _load_barcode_deps()
    barcode = code128(clave_acceso, writer=svg_writer())

    buffer = BytesIO()
    barcode.write(
        buffer,
        options={
            "write_text": False,
            "quiet_zone": 0,
            "module_height": 15.0,
        },
    )
    raw_svg = buffer.getvalue()
    return _normalizar_dimensiones_svg(raw_svg)


def _normalizar_dimensiones_svg(svg_bytes: bytes) -> bytes:
    root = etree.fromstring(svg_bytes)
    root.set("width", SVG_WIDTH)
    root.set("height", SVG_HEIGHT)

    if not root.get("viewBox"):
        width = root.get("width", SVG_WIDTH)
        height = root.get("height", SVG_HEIGHT)
        root.set("viewBox", f"0 0 {width} {height}")

    return etree.tostring(root, encoding="utf-8", xml_declaration=False)


def _load_barcode_deps():
    try:
        from barcode import Code128  # type: ignore
        from barcode.writer import SVGWriter  # type: ignore
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Falta dependencia para barcode. Instala con: pip install python-barcode"
        ) from exc
    return Code128, SVGWriter

