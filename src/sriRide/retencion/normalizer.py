from __future__ import annotations

from decimal import Decimal
from typing import Any


AMBIENTE_MAP = {
    "1": "Pruebas",
    "2": "Producción",
}

TIPO_EMISION_MAP = {
    "1": "Normal",
    "2": "Indisponibilidad del Sistema",
}

TIPO_DOCUMENTO_MAP = {
    "01": "FACTURA",
    "03": "LIQUIDACIÓN DE COMPRA",
    "04": "NOTA DE CRÉDITO",
    "05": "NOTA DE DÉBITO",
    "06": "GUÍA DE REMISIÓN",
    "07": "COMPROBANTE DE RETENCIÓN",
}

CODIGO_RETENCION_MAP = {
    "1": "RENTA",
    "2": "IVA",
    "6": "ISD",
    "01": "RENTA",
    "02": "IVA",
    "06": "ISD",
}


def normalizar_retencion(retencion_obj: Any) -> dict:
    info_tributaria = _first_node(retencion_obj, "infoTributaria")
    info_comp_retencion = _first_node(retencion_obj, "infoCompRetencion")
    docs_sustento = _walk_path_nodes(retencion_obj, "docsSustento.docSustento")
    campos_adicionales = _walk_path_nodes(retencion_obj, "infoAdicional.campoAdicional")
    string_fields = _walk_path_nodes(retencion_obj, "extensions.extension.StringField")

    return {
        "doc": _build_doc_context(info_tributaria, info_comp_retencion, string_fields),
        "emisor": _build_emisor_context(info_tributaria, info_comp_retencion),
        "sujeto_retenido": _build_sujeto_retenido_context(info_comp_retencion),
        "documento": _build_documento_context(docs_sustento, info_comp_retencion),
        "info_adicional": _build_info_adicional_context(campos_adicionales),
    }


def _build_doc_context(info_tributaria: Any, info_comp_retencion: Any, string_fields: list[Any]) -> dict:
    numero = _join_values(
        [
            _first_text_from(info_tributaria, "estab"),
            _first_text_from(info_tributaria, "ptoEmi"),
            _first_text_from(info_tributaria, "secuencial"),
        ],
        separator=" - ",
    )

    ambiente_codigo = _first_text_from(info_tributaria, "ambiente")
    tipo_emision_codigo = _first_text_from(info_tributaria, "tipoEmision")

    return {
        "ruc": _first_text_from(info_tributaria, "ruc"),
        "numero": numero,
        "ambiente": AMBIENTE_MAP.get(ambiente_codigo or "", ambiente_codigo),
        "tipo_emision": TIPO_EMISION_MAP.get(tipo_emision_codigo or "", tipo_emision_codigo),
        "fecha_autorizacion": _string_field_value(string_fields, "Fecha_autorizacion"),
        "numero_autorizacion": _string_field_value(string_fields, "Numero_autorizacion"),
        "clave_acceso": _first_text_from(info_tributaria, "claveAcceso"),
        "cntrbynte_esp": _first_text_from(info_comp_retencion, "contribuyenteEspecial"),
        "agent_retencn": _first_text_from(info_tributaria, "agenteRetencion"),
    }


def _build_emisor_context(info_tributaria: Any, info_comp_retencion: Any) -> dict:
    regimen = _first_text_from(info_tributaria, "contribuyenteRimpe")
    if not regimen:
        regimen = "General"

    obligado_raw = _first_text_from(info_comp_retencion, "obligadoContabilidad")
    obligado = (obligado_raw or "").upper() if obligado_raw else obligado_raw

    return {
        "nombre_comercial": _first_text_from(info_tributaria, "nombreComercial"),
        "direccion": _first_text_from(info_tributaria, "dirMatriz"),
        "direccion_estab": _first_text_from(info_comp_retencion, "dirEstablecimiento"),
        "razon_social": _first_text_from(info_tributaria, "razonSocial"),
        "regimen": regimen,
        "obligado_contabilidad": obligado,
    }


def _build_sujeto_retenido_context(info_comp_retencion: Any) -> dict:
    return {
        "razon_social": _first_text_from(info_comp_retencion, "razonSocialSujetoRetenido"),
        "identificacion": _first_text_from(info_comp_retencion, "identificacionSujetoRetenido"),
        "fecha_emision": _first_text_from(info_comp_retencion, "fechaEmision"),
    }


def _build_documento_context(docs_sustento: list[Any], info_comp_retencion: Any) -> dict:
    items: list[dict] = []
    ejercicio_fiscal = _first_text_from(info_comp_retencion, "periodoFiscal")

    for doc_node in docs_sustento:
        tipo_doc_codigo = _first_text_from(doc_node, "codDocSustento")
        tipo_doc_label = TIPO_DOCUMENTO_MAP.get(tipo_doc_codigo or "", tipo_doc_codigo)

        items.append(
            {
                "tipo_documento": tipo_doc_label,
                "numero_autorizacion": _first_text_from(doc_node, "numAutDocSustento"),
                "fecha_emision_docsustento": _first_text_from(doc_node, "fechaEmisionDocSustento"),
                "ejercicio_fiscal": ejercicio_fiscal,
                "detalle_retencion": _build_detalle_retencion(doc_node),
            }
        )

    return {"items": items}


def _build_detalle_retencion(doc_node: Any) -> list[dict]:
    retencion_nodes = _walk_relative_nodes(doc_node, "retenciones.retencion")
    retenciones: list[dict] = []

    for retencion_node in retencion_nodes:
        codigo = _first_text_from(retencion_node, "codigo")
        codigo_normalizado = (codigo or "").strip()
        if len(codigo_normalizado) == 1 and codigo_normalizado.isdigit():
            codigo_normalizado = codigo_normalizado.zfill(2)
        codigo_label = CODIGO_RETENCION_MAP.get(codigo_normalizado, codigo)

        retenciones.append(
            {
                "codigo": codigo_label,
                "base_imponible_retencion": _first_text_from(retencion_node, "baseImponible"),
                "porcentaje_retencion": _first_text_from(retencion_node, "porcentajeRetener"),
                "valor_retencion": _first_text_from(retencion_node, "valorRetenido"),
            }
        )

    return retenciones


def _build_info_adicional_context(campos_adicionales: list[Any]) -> dict:
    campos: list[dict] = []
    for campo in campos_adicionales:
        valor = _node_text(campo)
        if not valor:
            valor = _first_text_from(campo, "valor")
        if valor:
            campos.append({"campo_adicional": valor})
    return {"campos": campos}


def _string_field_value(string_fields: list[Any], field_name: str) -> str | None:
    for field in string_fields:
        name = _first_text_from(field, "name") or _first_text_from(field, "nombre")
        if name != field_name:
            continue
        value = _first_text_from(field, "value")
        if value:
            return value
        return _node_text(field)
    return None


def _walk_relative_nodes(node: Any, dot_path: str) -> list[Any]:
    return _walk_path_nodes(node, dot_path)


def _walk_path_nodes(root: Any, dot_path: str) -> list[Any]:
    nodes: list[Any] = [root]
    for segment in dot_path.split("."):
        next_nodes: list[Any] = []
        for node in nodes:
            child = _get_child(node, segment)
            if child is None:
                continue
            if isinstance(child, (list, tuple)):
                next_nodes.extend(item for item in child if item is not None)
            else:
                next_nodes.append(child)
        nodes = next_nodes
        if not nodes:
            break
    return nodes


def _first_node(root: Any, dot_path: str) -> Any | None:
    nodes = _walk_path_nodes(root, dot_path)
    if not nodes:
        return None
    return nodes[0]


def _first_text_from(node: Any, attr_name: str) -> str | None:
    return _node_text(_get_child(node, attr_name))


def _node_text(value: Any) -> str | None:
    if value is None:
        return None

    if isinstance(value, str):
        clean = value.strip()
        return clean or None

    if isinstance(value, (int, float, Decimal)):
        return str(value)

    if isinstance(value, (list, tuple)):
        for item in value:
            text = _node_text(item)
            if text:
                return text
        return None

    nested = _get_child(value, "value")
    if nested is not None and nested is not value:
        nested_text = _node_text(nested)
        if nested_text is not None:
            return nested_text

    text = str(value).strip()
    return text or None


def _join_values(values: list[str | None], separator: str = " - ") -> str | None:
    clean = [value.strip() for value in values if value and value.strip()]
    if not clean:
        return None
    return separator.join(clean)


def _get_child(obj: Any, name: str) -> Any | None:
    if obj is None:
        return None

    keys = _candidate_names(name)

    if isinstance(obj, dict):
        for key in keys:
            if key in obj:
                return obj[key]
        return None

    for key in keys:
        if hasattr(obj, key):
            return getattr(obj, key)
    return None


def _candidate_names(name: str) -> list[str]:
    snake = _camel_to_snake(name)
    camel = _snake_to_camel(name)
    candidates = [name, snake, camel]
    return list(dict.fromkeys(candidates))


def _camel_to_snake(name: str) -> str:
    if not name:
        return name

    chars: list[str] = []
    for index, char in enumerate(name):
        if char.isupper() and index > 0 and name[index - 1] != "_":
            chars.append("_")
        chars.append(char.lower())
    return "".join(chars)


def _snake_to_camel(name: str) -> str:
    if "_" not in name:
        return name
    head, *tail = name.split("_")
    return head + "".join(chunk.capitalize() for chunk in tail)
