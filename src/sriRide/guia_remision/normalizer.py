from __future__ import annotations

from typing import Any


AMBIENTE_MAP = {
    "1": "Pruebas",
    "2": "Produccion",
}

TIPO_EMISION_MAP = {
    "1": "Normal",
    "2": "Indisponibilidad del Sistema",
}

TIPO_DOCUMENTO_MAP = {
    "01": "FACTURA",
    "03": "LIQUIDACION DE COMPRA",
    "04": "NOTA DE CREDITO",
    "05": "NOTA DE DEBITO",
    "06": "GUIA DE REMISION",
    "07": "COMPROBANTE DE RETENCION",
}


def normalizar_guia_remision(guia_obj: Any) -> dict:
    info_tributaria = _first_node(guia_obj, "infoTributaria")
    info_guia_remision = _first_node(guia_obj, "infoGuiaRemision")
    destinatarios = _walk_path_nodes(guia_obj, "destinatarios.destinatario")
    campos_adicionales = _walk_path_nodes(guia_obj, "infoAdicional.campoAdicional")
    string_fields = _walk_path_nodes(guia_obj, "extensions.extension.StringField")

    destinatario = _build_destinatario_context(destinatarios)
    producto = _build_producto_context(destinatarios)

    return {
        "doc": _build_doc_context(info_tributaria, info_guia_remision, string_fields),
        "emisor": _build_emisor_context(info_tributaria, info_guia_remision),
        "transportista": _build_transportista_context(info_guia_remision),
        "destinatario": destinatario,
        "producto": producto,
        "info_adicional": _build_info_adicional_context(campos_adicionales),
    }


def _build_doc_context(info_tributaria: Any, info_guia_remision: Any, string_fields: list[Any]) -> dict:
    numero = _join_values(
        [
            _first_text_from(info_tributaria, "estab"),
            _first_text_from(info_tributaria, "ptoEmi"),
            _first_text_from(info_tributaria, "secuencial"),
        ],
        separator="-",
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
        "cntrbynte_esp": _first_text_from(info_guia_remision, "contribuyenteEspecial"),
        "agent_retencn": _first_text_from(info_tributaria, "agenteRetencion"),
    }


def _build_emisor_context(info_tributaria: Any, info_guia_remision: Any) -> dict:
    regimen = _first_text_from(info_tributaria, "contribuyenteRimpe")
    if not regimen:
        regimen = "General"

    obligado_raw = _first_text_from(info_guia_remision, "obligadoContabilidad")
    obligado = (obligado_raw or "").upper() if obligado_raw else obligado_raw

    return {
        "nombre_comercial": _first_text_from(info_tributaria, "nombreComercial"),
        "direccion": _first_text_from(info_tributaria, "dirMatriz"),
        "direccion_estab": _first_text_from(info_guia_remision, "dirEstablecimiento"),
        "razon_social": _first_text_from(info_tributaria, "razonSocial"),
        "regimen": regimen,
        "obligado_contabilidad": obligado,
    }


def _build_transportista_context(info_guia_remision: Any) -> dict:
    direccion = _first_text_from(info_guia_remision, "dirPartida")
    if not direccion:
        direccion = "---"

    return {
        "razon_social": _first_text_from(info_guia_remision, "razonSocialTransportista"),
        "identificacion": _first_text_from(info_guia_remision, "rucTransportista"),
        "direccion": direccion,
        "fecha_fin": _first_text_from(info_guia_remision, "fechaFinTransporte"),
        "fecha_inicio": _first_text_from(info_guia_remision, "fechaIniTransporte"),
        "placa": _first_text_from(info_guia_remision, "placa"),
    }


def _build_destinatario_context(destinatarios: list[Any]) -> dict:
    items: list[dict] = []

    for destinatario_node in destinatarios:
        tipo_doc_codigo = _first_text_from(destinatario_node, "codDocSustento")
        tipo_doc_label = TIPO_DOCUMENTO_MAP.get(tipo_doc_codigo or "", tipo_doc_codigo)

        documento_aduanero = _first_text_from(destinatario_node, "docAduaneroUnico")
        if not documento_aduanero:
            documento_aduanero = "NO APLICA"

        cod_establecimiento_destino = _first_text_from(destinatario_node, "codEstabDestino") or ""
        detalles = _build_detalles_destinatario(destinatario_node)

        items.append(
            {
                "numero_documento": _first_text_from(destinatario_node, "numDocSustento"),
                "tipo_documento": tipo_doc_label,
                "fecha_emision": _first_text_from(destinatario_node, "fechaEmisionDocSustento"),
                "numero_autorizacion": _first_text_from(destinatario_node, "numAutDocSustento"),
                "motivo_traslado": _first_text_from(destinatario_node, "motivoTraslado"),
                "destino": _first_text_from(destinatario_node, "dirDestinatario"),
                "identificacion": _first_text_from(destinatario_node, "identificacionDestinatario"),
                "razon_social": _first_text_from(destinatario_node, "razonSocialDestinatario"),
                "documento_aduanero": documento_aduanero,
                "cod_establecimiento_destino": cod_establecimiento_destino,
                "ruta": _first_text_from(destinatario_node, "ruta"),
                "detalles": detalles,
            }
        )

    return {"items": items}


def _build_detalles_destinatario(destinatario_node: Any) -> list[dict]:
    detalle_nodes = _walk_relative_nodes(destinatario_node, "detalles.detalle")
    detalles: list[dict] = []

    for detalle_node in detalle_nodes:
        detalles.append(
            {
                "codigo": _first_text_from(detalle_node, "codigoInterno"),
                "descripcion": _first_text_from(detalle_node, "descripcion"),
                "codigo_secundario": _first_text_from(detalle_node, "codigoAdicional") or "",
                "cantidad": _first_text_from(detalle_node, "cantidad"),
                "detalle_adicional": _detalle_adicional_compuesto(detalle_node) or "",
            }
        )

    return detalles


def _build_producto_context(destinatarios: list[Any]) -> dict:
    items: list[dict] = []
    for destinatario_node in destinatarios:
        for detalle in _walk_relative_nodes(destinatario_node, "detalles.detalle"):
            items.append(
                {
                    "codigo": _first_text_from(detalle, "codigoInterno"),
                    "descripcion": _first_text_from(detalle, "descripcion"),
                    "codigo_secundario": _first_text_from(detalle, "codigoAdicional") or "",
                    "cantidad": _first_text_from(detalle, "cantidad"),
                    "detalle_adicional": _detalle_adicional_compuesto(detalle) or "",
                }
            )
    return {"items": items}


def _build_info_adicional_context(campos_adicionales: list[Any]) -> dict:
    campos: list[dict] = []
    for campo in campos_adicionales:
        valor = _node_text(campo)
        if not valor:
            valor = _first_text_from(campo, "valor")
        if valor:
            campos.append({"campo_adicional": valor})
    return {"campos": campos}


def _detalle_adicional_compuesto(detalle_node: Any) -> str | None:
    det_adicional_nodes = _walk_relative_nodes(detalle_node, "detallesAdicionales.detAdicional")
    if not det_adicional_nodes:
        return None

    partes: list[str] = []
    for node in det_adicional_nodes:
        nombre = _first_text_from(node, "nombre") or _first_text_from(node, "name")
        valor = _first_text_from(node, "valor") or _first_text_from(node, "value") or _node_text(node)

        if nombre and valor:
            partes.append(f"{nombre}: {valor}")
        elif valor:
            partes.append(valor)
        elif nombre:
            partes.append(nombre)

    if not partes:
        return None
    return ", ".join(partes)


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

    if isinstance(value, (int, float)):
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
