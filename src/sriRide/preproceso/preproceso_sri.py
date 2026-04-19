from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Union
from xml.etree import ElementTree as ET

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig


from sriRide.dataclass.factura.factura_v2_1_0 import Factura # type: ignore
from sriRide.dataclass.guia_remision.guia_remision_v1_1_0 import GuiaRemision # type: ignore
from sriRide.dataclass.nota_credito.nota_credito_v1_1_0 import NotaCredito # type: ignore
from sriRide.dataclass.nota_debito.nota_debito_v1_0_0 import NotaDebito # type: ignore
from sriRide.dataclass.retencion.retencion_v2_0_0 import ComprobanteRetencion # type: ignore

XmlInput = Union[str, bytes, Path]

SRI_COMPROBANTE_TAGS = (
    "factura",
    "notaCredito",
    "notaDebito",
    "guiaRemision",
    "comprobanteRetencion",
)

DTO_BY_TIPO = {
    "factura": Factura,
    "guiaRemision": GuiaRemision,
    "notaCredito": NotaCredito,
    "notaDebito": NotaDebito,
    "comprobanteRetencion": ComprobanteRetencion,
}


@dataclass
class SriPreprocesoResultado:
    estado: str
    numero_autorizacion: str
    fecha_autorizacion: str
    tipo_comprobante: str
    comprobante_obj: Any
    comprobante_xml: str


def preprocesar_xml_autorizado_sri(xml_input: XmlInput) -> SriPreprocesoResultado:
    """
    Flujo estricto para XML AUTORIZADO SRI:
    1) Validar wrapper autorizado.
    2) Extraer numero/fecha de autorizacion.
    3) Extraer XML interno desde <comprobante>.
    4) Parsear DTO segun tipo de comprobante.
    """
    wrapper_root = _load_xml_root(xml_input)
    estado, numero_autorizacion, fecha_raw, comprobante_xml = _extraer_campos_wrapper(wrapper_root)

    if estado != "AUTORIZADO":
        raise ValueError(f"El XML no tiene estado AUTORIZADO (estado={estado!r}).")

    fecha_autorizacion = _formatear_fecha_autorizacion(fecha_raw)
    tipo_comprobante = _detectar_tipo_comprobante(comprobante_xml)
    comprobante_obj = _parsear_dto(comprobante_xml, tipo_comprobante)

    return SriPreprocesoResultado(
        estado=estado,
        numero_autorizacion=numero_autorizacion,
        fecha_autorizacion=fecha_autorizacion,
        tipo_comprobante=tipo_comprobante,
        comprobante_obj=comprobante_obj,
        comprobante_xml=comprobante_xml,
    )


async def preprocesar_xml_autorizado_sri_async(xml_input: XmlInput) -> SriPreprocesoResultado:
    return await asyncio.to_thread(preprocesar_xml_autorizado_sri, xml_input)


def _load_xml_root(xml_input: XmlInput) -> ET.Element:
    if isinstance(xml_input, Path):
        return ET.parse(str(xml_input)).getroot()

    if isinstance(xml_input, bytes):
        return ET.fromstring(xml_input)

    if isinstance(xml_input, str):
        if xml_input.lstrip().startswith("<"):
            return ET.fromstring(xml_input.encode("utf-8"))
        return ET.parse(xml_input).getroot()

    raise TypeError(f"Tipo de entrada XML no soportado: {type(xml_input)!r}")


def _extraer_campos_wrapper(root: ET.Element) -> tuple[str, str, str, str]:
    estado: str | None = None
    numero_autorizacion: str | None = None
    fecha_autorizacion: str | None = None
    comprobante_xml: str | None = None

    for node in root.iter():
        name = _local_name(node.tag)
        text = (node.text or "").strip()
        if not text:
            continue

        if estado is None and name == "estado":
            estado = text
        elif numero_autorizacion is None and name == "numeroAutorizacion":
            numero_autorizacion = text
        elif fecha_autorizacion is None and name == "fechaAutorizacion":
            fecha_autorizacion = text
        elif comprobante_xml is None and name == "comprobante":
            comprobante_xml = text

        if estado and numero_autorizacion and fecha_autorizacion and comprobante_xml:
            break

    if not estado:
        raise ValueError("No se encontro <estado> en XML autorizado.")
    if not numero_autorizacion:
        raise ValueError("No se encontro <numeroAutorizacion> en XML autorizado.")
    if not fecha_autorizacion:
        raise ValueError("No se encontro <fechaAutorizacion> en XML autorizado.")
    if not comprobante_xml:
        raise ValueError("No se encontro <comprobante> en XML autorizado.")

    return estado, numero_autorizacion, fecha_autorizacion, comprobante_xml


def _detectar_tipo_comprobante(comprobante_xml: str) -> str:
    payload = comprobante_xml.strip()
    if not payload:
        raise ValueError("El nodo <comprobante> esta vacio.")

    try:
        root = ET.fromstring(payload.encode("utf-8"))
    except ET.ParseError as exc:
        raise ValueError("No se pudo parsear el XML interno de <comprobante>.") from exc

    tipo = _local_name(root.tag)
    if tipo in SRI_COMPROBANTE_TAGS:
        return tipo

    raise ValueError(f"Tipo de comprobante no soportado en wrapper SRI: {tipo!r}.")


from xsdata.formats.dataclass.parsers.config import ParserConfig

def _parsear_dto(comprobante_xml: str, tipo_comprobante: str) -> Any:
    dto_class = DTO_BY_TIPO.get(tipo_comprobante)
    if dto_class is None:
        raise NotImplementedError(f"Tipo '{tipo_comprobante}' sin DTO.")

    config = ParserConfig(
        fail_on_unknown_properties=False,  # nodos extra en XML → ignorar
        fail_on_unknown_attributes=False,
    )
    parser = XmlParser(config=config)
    return parser.parse(BytesIO(comprobante_xml.encode("utf-8")), dto_class)


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
