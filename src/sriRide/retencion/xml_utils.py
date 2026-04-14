from __future__ import annotations

from lxml import etree

from ..core.xml_utils import (
    XmlInput,
    extract_document_root,
    first_text,
    first_text_from,
    join_values,
    local_name,
    load_any_xml_root,
    walk_path_nodes,
    walk_relative_nodes,
)


def load_xml_root(xml_input: XmlInput) -> etree._Element:
    """Carga XML desde texto/bytes/path/elemento y devuelve la raiz util."""
    root = load_any_xml_root(xml_input)
    retencion = extract_document_root(root, root_tag="comprobanteRetencion")
    return retencion if retencion is not None else root

