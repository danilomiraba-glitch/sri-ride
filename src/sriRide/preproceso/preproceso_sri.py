from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Union

from lxml import etree

XmlInput = Union[str, bytes, Path, etree._Element, etree._ElementTree]
SRI_COMPROBANTE_TAGS = (
    "factura",
    "notaCredito",
    "notaDebito",
    "guiaRemision",
    "comprobanteRetencion",
    "liquidacionCompra",
)


@dataclass
class SriPreprocesoResultado:
    estado: str
    numero_autorizacion: str
    fecha_autorizacion: str
    xml_legible: str
    comprobante_root: etree._Element
    tipo_comprobante: str
    factura_root: etree._Element | None = None


def preprocesar_xml_autorizado_sri(xml_input: XmlInput) -> SriPreprocesoResultado:
    """
    Flujo de preproceso para XML autorizado SRI:
    1) Valida estado AUTORIZADO.
    2) Extrae numero/fecha de autorizacion.
    3) Obtiene el XML del comprobante desde <comprobante>.
    4) Formatea fecha a dd/mm/yyyy HH:MM:SS.
    5) Inyecta nodo de autorizacion dentro del comprobante.
    6) Retorna XML legible (pretty print) y metadatos.
    """
    root = _load_xml_root(xml_input)

    normalizado = _extraer_comprobante_normalizado(root)
    if normalizado is not None:
        return _preproceso_passthrough_comprobante(normalizado)

    estado = _find_text(root, "estado")
    if estado != "AUTORIZADO":
        raise ValueError("El XML no tiene estado AUTORIZADO.")

    numero_autorizacion = _require_text(root, "numeroAutorizacion")
    fecha_original = _require_text(root, "fechaAutorizacion")
    fecha_formateada = _formatear_fecha_autorizacion(fecha_original)

    comprobante = _require_text(root, "comprobante")
    comprobante_root = _parse_inner_comprobante(comprobante)
    tipo_comprobante = _local_name(comprobante_root.tag)

    _inyectar_autorizacion(
        comprobante_root,
        numero_autorizacion=numero_autorizacion,
        fecha_autorizacion=fecha_formateada,
    )

    xml_legible = etree.tostring(
        comprobante_root,
        encoding="utf-8",
        xml_declaration=True,
        pretty_print=True,
    ).decode("utf-8")

    return SriPreprocesoResultado(
        estado=estado,
        numero_autorizacion=numero_autorizacion,
        fecha_autorizacion=fecha_formateada,
        xml_legible=xml_legible,
        comprobante_root=comprobante_root,
        tipo_comprobante=tipo_comprobante,
        factura_root=comprobante_root if tipo_comprobante == "factura" else None,
    )


async def preprocesar_xml_autorizado_sri_async(xml_input: XmlInput) -> SriPreprocesoResultado:
    return await asyncio.to_thread(preprocesar_xml_autorizado_sri, xml_input)


def _extraer_comprobante_normalizado(root: etree._Element) -> etree._Element | None:
    root_name = _local_name(root.tag)
    if root_name in SRI_COMPROBANTE_TAGS:
        return root

    wrapper_nodes = root.xpath(".//*[local-name()='comprobante']")

    if wrapper_nodes:
        return None

    for tag in SRI_COMPROBANTE_TAGS:
        nodes = root.xpath(f".//*[local-name()='{tag}']")
        if nodes:
            return nodes[0]
    return None


def _preproceso_passthrough_comprobante(comprobante_root: etree._Element) -> SriPreprocesoResultado:
    tipo_comprobante = _local_name(comprobante_root.tag)
    numero_autorizacion = _extraer_o_default_string_field(
        comprobante_root,
        "Numero_autorizacion",
        default="PRUEBA-SIN-AUTORIZACION",
    )
    fecha_autorizacion = _extraer_o_default_string_field(
        comprobante_root,
        "Fecha_autorizacion",
        default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    )

    xml_legible = etree.tostring(
        comprobante_root,
        encoding="utf-8",
        xml_declaration=True,
        pretty_print=True,
    ).decode("utf-8")

    return SriPreprocesoResultado(
        estado="DESARROLLO",
        numero_autorizacion=numero_autorizacion,
        fecha_autorizacion=fecha_autorizacion,
        xml_legible=xml_legible,
        comprobante_root=comprobante_root,
        tipo_comprobante=tipo_comprobante,
        factura_root=comprobante_root if tipo_comprobante == "factura" else None,
    )


def _load_xml_root(xml_input: XmlInput) -> etree._Element:
    if isinstance(xml_input, etree._Element):
        return xml_input
    if isinstance(xml_input, etree._ElementTree):
        return xml_input.getroot()
    if isinstance(xml_input, Path):
        return etree.parse(str(xml_input)).getroot()
    if isinstance(xml_input, bytes):
        return etree.fromstring(xml_input)
    if isinstance(xml_input, str):
        if xml_input.lstrip().startswith("<"):
            return etree.fromstring(xml_input.encode("utf-8"))
        return etree.parse(xml_input).getroot()
    raise TypeError(f"Tipo de entrada XML no soportado: {type(xml_input)!r}")


def _find_text(root: etree._Element, local_tag: str) -> str | None:
    nodes = root.xpath(f".//*[local-name()='{local_tag}']")
    for node in nodes:
        text = (node.text or "").strip()
        if text:
            return text
    return None


def _require_text(root: etree._Element, local_tag: str) -> str:
    text = _find_text(root, local_tag)
    if not text:
        raise ValueError(f"No se encontro valor en <{local_tag}>.")
    return text


def _parse_inner_comprobante(comprobante_text: str) -> etree._Element:
    payload = comprobante_text.strip()
    if not payload:
        raise ValueError("El nodo <comprobante> esta vacio.")
    try:
        comprobante_root = etree.fromstring(payload.encode("utf-8"))
    except etree.XMLSyntaxError as exc:
        raise ValueError("No se pudo parsear el XML interno de <comprobante>.") from exc

    if _local_name(comprobante_root.tag) in SRI_COMPROBANTE_TAGS:
        return comprobante_root

    for tag in SRI_COMPROBANTE_TAGS:
        nodes = comprobante_root.xpath(f".//*[local-name()='{tag}']")
        if nodes:
            return nodes[0]

    raise ValueError("El XML interno no contiene un comprobante SRI soportado.")


def _inyectar_autorizacion(
    comprobante_root: etree._Element,
    *,
    numero_autorizacion: str,
    fecha_autorizacion: str,
) -> None:
    """
    Crea/actualiza nodo:
      comprobante/extensions/extension/StringField[@name='Numero_autorizacion']
      comprobante/extensions/extension/StringField[@name='Fecha_autorizacion']
    """
    extensions = _find_or_create_child(comprobante_root, "extensions")
    extension = _find_or_create_child(extensions, "extension")

    _set_string_field(extension, "Numero_autorizacion", numero_autorizacion)
    _set_string_field(extension, "Fecha_autorizacion", fecha_autorizacion)


def _set_string_field(extension_node: etree._Element, name: str, value: str) -> None:
    candidates = extension_node.xpath("./*[local-name()='StringField']")
    target = None
    for node in candidates:
        if (node.get("name") or "").strip() == name:
            target = node
            break

    if target is None:
        target = etree.SubElement(extension_node, "StringField")
        target.set("name", name)
    target.text = value


def _extraer_o_default_string_field(comprobante_root: etree._Element, name: str, *, default: str) -> str:
    nodes = comprobante_root.xpath(
        ".//*[local-name()='extensions']/*[local-name()='extension']/*[local-name()='StringField']"
    )
    for node in nodes:
        if (node.get("name") or "").strip() != name:
            continue
        value = (node.text or "").strip()
        if value:
            return value
    return default


def _find_or_create_child(parent: etree._Element, local_tag: str) -> etree._Element:
    nodes = parent.xpath(f"./*[local-name()='{local_tag}']")
    if nodes:
        return nodes[0]
    return etree.SubElement(parent, local_tag)


def _local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def _formatear_fecha_autorizacion(raw: str) -> str:
    text = raw.strip()
    if not text:
        return text

    iso_candidate = text.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(iso_candidate)
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        pass

    formatos = [
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
    ]
    for fmt in formatos:
        try:
            dt = datetime.strptime(text, fmt)
            return dt.strftime("%d/%m/%Y %H:%M:%S")
        except ValueError:
            continue

    return text
