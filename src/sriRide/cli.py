from __future__ import annotations

import argparse
import asyncio
import base64
import json
import re
import sys
from importlib import metadata, resources
from pathlib import Path

from . import SriRide


DOC_METHOD_MAP = {
    "factura": "factura",
    "guiaremision": "guiaremision",
    "guia_remision": "guiaremision",
    "retencion": "retencion",
    "notacredito": "notacredito",
    "nota_credito": "notacredito",
    "notadebito": "notadebito",
    "nota_debito": "notadebito",
}


def main(argv: list[str] | None = None) -> int:
    args_list = list(argv) if argv is not None else sys.argv[1:]

    if "--help-ia" in args_list:
        print(json.dumps(_help_ia_payload(), ensure_ascii=False, indent=2))
        return 0
    
    if "--help" in args_list or "-h" in args_list:
        print(_load_help_text())
        return 0

    parser = _build_parser()
    args = parser.parse_args(args_list)

    try:
        if args.command == "render":
            return _cmd_render(args)
        parser.error("Subcomando no soportado.")
        return 2
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sri-ride",
        description="CLI para renderizar comprobantes SRI con la librería sriRide.",
        add_help=False,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"sri-ride { _get_version() }",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    render_parser = subparsers.add_parser("render", help="Renderiza un XML a HTML o PDF.")
    render_parser.add_argument("--doc", required=True, help="Tipo de comprobante (ej: factura, notadebito).")
    render_parser.add_argument("--xml", required=True, help="Ruta del XML de entrada.")
    render_parser.add_argument(
        "--mode",
        default="html",
        choices=["html", "pdf"],
        help="Modo de salida (default: html).",
    )
    render_parser.add_argument("--logo", help="Ruta de imagen logo opcional.")
    render_parser.add_argument(
        "--out",
        required=True,
        help="Salida obligatoria. En html: carpeta destino. En pdf: archivo .pdf destino.",
    )
    render_parser.add_argument("--template-dir", help="Directorio de plantilla personalizado.")
    render_parser.add_argument("--template-name", help="Nombre de plantilla personalizado.")

    return parser


def _cmd_render(args: argparse.Namespace) -> int:
    method_name = _resolver_doc_method(args.doc)
    sri = SriRide(mode=args.mode)
    method = getattr(sri, method_name)
    xml_input = _resolver_xml_input(args.xml)
    resultado = asyncio.run(
        method(
            xml=xml_input,
            logo=args.logo,
            template_dir=args.template_dir,
            template_name=args.template_name,
        )
    )

    if args.mode == "html":
        if not isinstance(resultado, list):
            raise TypeError("En mode=html se esperaba una lista de partes HTML.")

        out_dir = _resolver_out_dir_html(args.out)
        for parte in _normalizar_partes_salida(resultado):
            out_path = out_dir / f"{parte['orden']:02d}_{parte['clave']}.html"
            out_path.write_text(parte["html"], encoding="utf-8")
        return 0

    out_path = _resolver_out_file_pdf(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(resultado))
    return 0


def _resolver_doc_method(doc_raw: str) -> str:
    key = (doc_raw or "").strip().lower().replace("-", "_")
    method = DOC_METHOD_MAP.get(key)
    if method is None:
        soportados = ", ".join(sorted(set(DOC_METHOD_MAP.keys())))
        raise ValueError(f"--doc no soportado: '{doc_raw}'. Valores válidos: {soportados}")
    return method


def _resolver_xml_input(xml_arg: str) -> str | bytes:
    raw = (xml_arg or "").strip()
    if not raw:
        raise ValueError("--xml es requerido.")

    candidate = Path(raw).expanduser()
    if candidate.is_file():
        return candidate.read_bytes()
    return xml_arg


def _resolver_out_dir_html(out_arg: str) -> Path:
    out_raw = (out_arg or "").strip()
    if not out_raw:
        raise ValueError("--out es requerido y debe ser una carpeta en mode=html.")

    out_dir = Path(out_raw).expanduser().resolve()
    if out_dir.exists() and not out_dir.is_dir():
        raise ValueError("--out en mode=html debe apuntar a una carpeta, no a un archivo.")

    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def _resolver_out_file_pdf(out_arg: str) -> Path:
    out_raw = (out_arg or "").strip()
    if not out_raw:
        raise ValueError("--out es requerido y debe incluir un nombre de archivo .pdf en mode=pdf.")

    if out_raw.endswith("/") or out_raw.endswith("\\"):
        raise ValueError("--out en mode=pdf debe incluir un nombre de archivo .pdf, no solo carpeta.")

    out_path = Path(out_raw).expanduser().resolve()
    if out_path.exists() and out_path.is_dir():
        raise ValueError("--out en mode=pdf debe incluir un nombre de archivo .pdf, no solo carpeta.")

    if out_path.suffix.lower() != ".pdf":
        raise ValueError("--out en mode=pdf debe terminar en .pdf.")

    return out_path


def _get_version() -> str:
    try:
        return metadata.version("sri-ride")
    except metadata.PackageNotFoundError:
        return "0.1.0"


def _help_ia_payload() -> dict:
    payload_text = (
        resources.files(__package__)
        .joinpath("help_ia_payload.json")
        .read_text(encoding="utf-8")
    )
    payload = json.loads(payload_text)
    payload["version"] = _get_version()

    for subcommand in payload.get("subcommands", []):
        if subcommand.get("name") == "render":
            subcommand["doc_values"] = sorted(set(DOC_METHOD_MAP.keys()))

    return payload

def _load_help_text() -> str:
    return (
        resources.files(__package__)
        .joinpath("help.txt")
        .read_text(encoding="utf-8")
    )


def _normalizar_partes_salida(resultado: list) -> list[dict]:
    partes: list[dict] = []
    for i, parte in enumerate(resultado):
        if not isinstance(parte, dict):
            continue

        html = parte.get("html")
        if not isinstance(html, str):
            continue

        clave_raw = str(parte.get("clave", f"parte_{i}"))
        orden_raw = parte.get("orden", i)
        template_name = str(parte.get("template_name", ""))

        try:
            orden = int(orden_raw)
        except (TypeError, ValueError):
            orden = i

        partes.append(
            {
                "clave": _slug_archivo(clave_raw),
                "orden": orden,
                "template_name": template_name,
                "html": html,
            }
        )

    if not partes:
        raise ValueError("No hay partes HTML validas para escribir.")
    return sorted(partes, key=lambda p: p["orden"])


def _slug_archivo(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return cleaned or "parte"


if __name__ == "__main__":
    raise SystemExit(main())
