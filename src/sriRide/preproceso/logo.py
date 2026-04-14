from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Union
import base64

LogoInput = Union[str, bytes, Path]

CM_TO_PX_96_DPI = 96.0 / 2.54
DEFAULT_MAX_WIDTH_CM = 5.5
DEFAULT_MAX_HEIGHT_CM = 3.5
DEFAULT_MAX_INPUT_BYTES = 1 * 1024 * 1024  # 1 MB
DEFAULT_MAX_INPUT_WIDTH_PX = 1024
DEFAULT_MAX_INPUT_HEIGHT_PX = 1024


@dataclass
class LogoProcesadoResultado:
    content_type: str
    image_bytes: bytes
    data_uri: str
    width_px: int
    height_px: int
    input_bytes: int
    output_bytes: int


def procesar_logo_para_plantilla(
    logo_input: LogoInput,
    *,
    max_width_cm: float = DEFAULT_MAX_WIDTH_CM,
    max_height_cm: float = DEFAULT_MAX_HEIGHT_CM,
    max_input_bytes: int = DEFAULT_MAX_INPUT_BYTES,
    max_input_width_px: int = DEFAULT_MAX_INPUT_WIDTH_PX,
    max_input_height_px: int = DEFAULT_MAX_INPUT_HEIGHT_PX,
) -> LogoProcesadoResultado:
    """
    Normaliza logo (JPG/PNG/SVG) a PNG optimizado y ajustado a caja maxima.

    - Caja maxima por defecto: 5.5 cm x 3.5 cm (a 96 DPI CSS).
    - Mantiene proporcion; nunca estira.
    - Conserva transparencia cuando aplica.
    - Compresion PNG sin perdida (optimize + compress_level=9).
    """
    raw = _leer_input(logo_input)
    if len(raw) > max_input_bytes:
        raise ValueError(
            f"Logo excede el maximo permitido ({len(raw)} bytes > {max_input_bytes} bytes)."
        )

    max_w_px = max(1, int(round(max_width_cm * CM_TO_PX_96_DPI)))
    max_h_px = max(1, int(round(max_height_cm * CM_TO_PX_96_DPI)))

    if _parece_svg(raw, logo_input):
        image = _abrir_svg_como_imagen(raw)
    else:
        image = _abrir_raster(raw)

    _validar_resolucion_input(
        image,
        max_input_width_px=max_input_width_px,
        max_input_height_px=max_input_height_px,
    )
    image = _ajustar_a_caja(image, max_w_px=max_w_px, max_h_px=max_h_px)
    png_bytes = _codificar_png_optimo(image)

    b64 = base64.b64encode(png_bytes).decode("ascii")
    data_uri = f"data:image/png;base64,{b64}"

    return LogoProcesadoResultado(
        content_type="image/png",
        image_bytes=png_bytes,
        data_uri=data_uri,
        width_px=image.width,
        height_px=image.height,
        input_bytes=len(raw),
        output_bytes=len(png_bytes),
    )


def _leer_input(logo_input: LogoInput) -> bytes:
    if isinstance(logo_input, bytes):
        return logo_input
    if isinstance(logo_input, Path):
        return logo_input.read_bytes()
    if isinstance(logo_input, str):
        text = logo_input.strip()
        path = Path(text)
        if path.exists():
            return path.read_bytes()

        if text.startswith("data:"):
            header, sep, payload = text.partition(",")
            if not sep or ";base64" not in header.lower():
                raise ValueError("Data URI invalida para logo: se esperaba contenido base64.")
            return _decodificar_base64(payload)

        if text.lower().startswith("base64,"):
            return _decodificar_base64(text.split(",", 1)[1])

        if _parece_base64_texto(text):
            return _decodificar_base64(text)

        return text.encode("utf-8")
    raise TypeError(f"Tipo de logo_input no soportado: {type(logo_input)!r}")


def _parece_svg(raw: bytes, logo_input: LogoInput) -> bool:
    head = raw[:512].lstrip().lower()
    if b"<svg" in head or head.startswith(b"<?xml"):
        return True
    if isinstance(logo_input, (str, Path)):
        return Path(str(logo_input)).suffix.lower() == ".svg"
    return False


def _parece_base64_texto(value: str) -> bool:
    clean = "".join(value.split())
    if len(clean) < 32 or len(clean) % 4 != 0:
        return False
    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")
    return all(ch in allowed for ch in clean)


def _decodificar_base64(payload: str) -> bytes:
    clean = "".join(payload.split())
    try:
        decoded = base64.b64decode(clean, validate=True)
    except Exception as exc:
        raise ValueError("Contenido base64 de logo invalido.") from exc
    if not decoded:
        raise ValueError("Contenido base64 de logo vacio.")
    return decoded


def _abrir_svg_como_imagen(raw_svg: bytes):
    try:
        import cairosvg
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Para soportar SVG instala cairosvg: pip install cairosvg"
        ) from exc

    png = cairosvg.svg2png(bytestring=raw_svg)
    return _abrir_raster(png)


def _abrir_raster(raw: bytes):
    try:
        from PIL import Image
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Para procesar logos raster instala Pillow: pip install pillow"
        ) from exc

    image = Image.open(BytesIO(raw))
    image.load()
    return image


def _validar_resolucion_input(image, *, max_input_width_px: int, max_input_height_px: int) -> None:
    if image.width > max_input_width_px or image.height > max_input_height_px:
        raise ValueError(
            "Resolucion de logo excede el maximo permitido "
            f"({image.width}x{image.height} > {max_input_width_px}x{max_input_height_px})."
        )


def _ajustar_a_caja(image, *, max_w_px: int, max_h_px: int):
    from PIL import Image

    if image.mode not in ("RGB", "RGBA"):
        if "A" in image.getbands() or image.mode in ("LA", "PA"):
            image = image.convert("RGBA")
        else:
            image = image.convert("RGB")

    if image.width <= max_w_px and image.height <= max_h_px:
        return image

    resized = image.copy()
    resized.thumbnail((max_w_px, max_h_px), Image.Resampling.LANCZOS)
    return resized


def _codificar_png_optimo(image) -> bytes:
    out = BytesIO()
    image.save(
        out,
        format="PNG",
        optimize=True,
        compress_level=9,
    )
    return out.getvalue()
