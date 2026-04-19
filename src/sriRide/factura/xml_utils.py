from __future__ import annotations

from typing import Any

# Alias de compatibilidad con código externo que todavía importe XmlInput.
XmlInput = Any


def load_xml_root(xml_input: XmlInput) -> XmlInput:
    """
    Compatibilidad temporal.
    En la ruta de baja latencia se espera que `xml_input` ya sea el objeto Factura.
    """
    return xml_input
