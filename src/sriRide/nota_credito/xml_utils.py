from __future__ import annotations

from typing import Any

# Alias de compatibilidad con codigo externo que todavia importe XmlInput.
XmlInput = Any


def load_xml_root(xml_input: XmlInput) -> XmlInput:
    """
    Compatibilidad temporal.
    En la ruta de baja latencia se espera que `xml_input` ya sea el objeto NotaCredito.
    """
    return xml_input
