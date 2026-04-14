from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Iterable, Union

from lxml import etree

XmlInput = Union[str, bytes, Path, etree._Element, etree._ElementTree]


def load_any_xml_root(xml_input: XmlInput) -> etree._Element:
    """Carga XML desde texto/bytes/path/elemento y devuelve la raiz."""
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


async def load_any_xml_root_async(xml_input: XmlInput) -> etree._Element:
    return await asyncio.to_thread(load_any_xml_root, xml_input)


def extract_document_root(root: etree._Element, *, root_tag: str) -> etree._Element | None:
    """Extrae el comprobante objetivo desde XML directo o XML autorizado SRI."""
    if local_name(root.tag) == root_tag:
        return root

    comprobante_nodes = root.xpath(".//*[local-name()='comprobante']")
    for node in comprobante_nodes:
        payload = (node.text or "").strip()
        if not payload:
            continue
        if f"<{root_tag}" not in payload:
            continue
        try:
            inner_root = etree.fromstring(payload.encode("utf-8"))
        except etree.XMLSyntaxError:
            continue
        if local_name(inner_root.tag) == root_tag:
            return inner_root

    nodes = root.xpath(f".//*[local-name()='{root_tag}']")
    if nodes:
        return nodes[0]
    return None


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def walk_path_nodes(root: etree._Element, dot_path: str) -> list[etree._Element]:
    """
    Recorre rutas como 'factura.infoTributaria.ruc' ignorando namespaces.
    Devuelve todos los nodos que coincidan con el ultimo segmento.
    """
    parts = [p.strip() for p in dot_path.split(".") if p.strip()]
    if not parts:
        return []

    current: list[etree._Element] = [root]
    if parts and local_name(root.tag) == parts[0]:
        parts = parts[1:]

    for part in parts:
        next_nodes: list[etree._Element] = []
        for node in current:
            matches = node.xpath(f"./*[local-name()='{part}']")
            next_nodes.extend(matches)
        current = next_nodes
        if not current:
            break
    return current


def walk_relative_nodes(node: etree._Element, dot_path: str) -> list[etree._Element]:
    """
    Recorre una ruta relativa desde `node`, ignorando namespaces.
    Ej: 'detallesAdicionales.detAdicional'
    """
    parts = [p.strip() for p in dot_path.split(".") if p.strip()]
    if not parts:
        return []

    current: list[etree._Element] = [node]
    for part in parts:
        next_nodes: list[etree._Element] = []
        for current_node in current:
            matches = current_node.xpath(f"./*[local-name()='{part}']")
            next_nodes.extend(matches)
        current = next_nodes
        if not current:
            break
    return current


def first_text(
    root: etree._Element,
    dot_path: str,
    *,
    attr_name: str | None = None,
    attr_value: str | None = None,
) -> str | None:
    nodes = walk_path_nodes(root, dot_path)
    if attr_name is not None:
        nodes = [n for n in nodes if n.get(attr_name) == (attr_value or "")]
    for node in nodes:
        text = (node.text or "").strip()
        if text:
            return text
    return None


def first_text_from(node: etree._Element, dot_path: str) -> str | None:
    nodes = walk_relative_nodes(node, dot_path)
    for current_node in nodes:
        text = (current_node.text or "").strip()
        if text:
            return text
    return None


def join_values(values: Iterable[str | None], separator: str = " - ") -> str | None:
    clean = [v.strip() for v in values if v and v.strip()]
    if not clean:
        return None
    return separator.join(clean)
