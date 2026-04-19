from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any


Q2 = Decimal("0.01")

FORMA_PAGO_MAP = {
    "01": "Sin utilización del sistema financiero",
    "15": "Compensación de deudas",
    "16": "Tarjeta de débito",
    "17": "Dinero electrónico",
    "18": "Tarjeta prepago",
    "19": "Tarjeta de crédito",
    "20": "Otros con utilización del sistema financiero",
    "21": "Endoso de títulos",
}

AMBIENTE_MAP = {
    "1": "Pruebas",
    "2": "Producción",
}

TIPO_EMISION_MAP = {
    "1": "Normal",
    "2": "Indisponibilidad del Sistema",
}

TIPO_COMPROBANTE_MAP = {
    "01": "FACTURA",
    "03": "LIQUIDACION COMPRA",
    "05": "NOTA DE DEBITO",
    "04": "NOTA DE CREDITO",
    "06": "GUIA DE REMISION",
    "07": "COMPROBANTE DE RETENCION",
}


def normalizar_nota_debito(nota_debito_obj: Any) -> dict:
    info_tributaria = _first_node(nota_debito_obj, "infoTributaria")
    info_nota_debito = _first_node(nota_debito_obj, "infoNotaDebito")
    motivos = _walk_path_nodes(nota_debito_obj, "motivos.motivo")
    campos_adicionales = _walk_path_nodes(nota_debito_obj, "infoAdicional.campoAdicional")
    impuestos = _walk_path_nodes(nota_debito_obj, "infoNotaDebito.impuestos.impuesto")
    pagos = _extract_pago_nodes(info_nota_debito)
    string_fields = _walk_path_nodes(nota_debito_obj, "extensions.extension.StringField")

    return {
        "doc": _build_doc_context(info_tributaria, info_nota_debito, string_fields),
        "emisor": _build_emisor_context(info_tributaria, info_nota_debito),
        "cliente": _build_cliente_context(info_nota_debito),
        "producto": _build_producto_context(motivos),
        "pago": _build_pago_context(pagos),
        "info_adicional": _build_info_adicional_context(campos_adicionales),
        "totales": _build_totales_context(info_nota_debito, impuestos),
        "comprobante": _build_comprobante_context(info_nota_debito),
    }


def _build_doc_context(info_tributaria: Any, info_nota_debito: Any, string_fields: list[Any]) -> dict:
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
        "cntrbynte_esp": _first_text_from(info_nota_debito, "contribuyenteEspecial"),
        "agent_retencn": _first_text_from(info_tributaria, "agenteRetencion"),
    }


def _build_emisor_context(info_tributaria: Any, info_nota_debito: Any) -> dict:
    regimen = _first_text_from(info_tributaria, "contribuyenteRimpe")
    if not regimen:
        regimen = "General"

    obligado_raw = _first_text_from(info_nota_debito, "obligadoContabilidad")
    obligado = (obligado_raw or "").upper() if obligado_raw else obligado_raw

    return {
        "direccion": _first_text_from(info_tributaria, "dirMatriz"),
        "direccion_estab": _first_text_from(info_nota_debito, "dirEstablecimiento"),
        "nombre_comercial": _first_text_from(info_tributaria, "nombreComercial"),
        "razon_social": _first_text_from(info_tributaria, "razonSocial"),
        "regimen": regimen,
        "obligado_contabilidad": obligado,
    }


def _build_cliente_context(info_nota_debito: Any) -> dict:
    return {
        "razon_social": _first_text_from(info_nota_debito, "razonSocialComprador"),
        "identificacion": _first_text_from(info_nota_debito, "identificacionComprador"),
        "fecha_emision": _first_text_from(info_nota_debito, "fechaEmision"),
    }


def _build_producto_context(motivos: list[Any]) -> dict:
    items: list[dict] = []
    for motivo_node in motivos:
        items.append(
            {
                "motivo": _first_text_from(motivo_node, "razon"),
                "valor": _first_text_from(motivo_node, "valor"),
            }
        )
    return {"items": items}


def _build_pago_context(pagos: list[Any]) -> dict:
    formas: list[dict] = []
    for pago_node in pagos:
        forma_codigo = _first_text_from(pago_node, "formaPago")
        forma_label = FORMA_PAGO_MAP.get(forma_codigo or "", forma_codigo)

        plazo = _first_text_from(pago_node, "plazo")
        unidad_tiempo = _first_text_from(pago_node, "unidadTiempo")

        formas.append(
            {
                "forma_pago": forma_label,
                "valor_pago": _first_text_from(pago_node, "total"),
                "plazo": plazo if plazo else "---",
                "unidad_tiempo": unidad_tiempo if unidad_tiempo else "---",
            }
        )

    return {"formas": formas}


def _build_info_adicional_context(campos_adicionales: list[Any]) -> dict:
    campos: list[dict] = []
    for campo in campos_adicionales:
        valor = _node_text(campo)
        if not valor:
            valor = _first_text_from(campo, "valor")
        if valor:
            campos.append({"campo_adicional": valor})
    return {"campos": campos}


def _build_totales_context(info_nota_debito: Any, impuestos: list[Any]) -> dict:
    subtotal_iva_0 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="0", field="baseImponible")
    subtotal_iva_5 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="5", field="baseImponible")
    subtotal_iva_15 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="4", field="baseImponible")
    subtotal_objeto_exento = _sum_impuesto_field(
        impuestos,
        codigo="2",
        codigo_porcentaje_in={"6", "7"},
        field="baseImponible",
    )

    total_iva_5 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="0", field="valor")
    total_iva_15 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="4", field="valor")
    total_ice = _sum_impuesto_field(impuestos, codigo="3", field="valor")

    return {
        "subtotal_iva_0": _fmt_or_default(subtotal_iva_0, "0.00"),
        "subtotal_iva_5": _fmt_nonzero_decimal(subtotal_iva_5),
        "subtotal_iva_15": _fmt_or_default(subtotal_iva_15, "0.00"),
        "subtotal_objeto_exento": _fmt_or_default(subtotal_objeto_exento, "0.00"),
        "subtotal_general": _first_text_from(info_nota_debito, "totalSinImpuestos"),
        "total_iva_5": _fmt_nonzero_decimal(total_iva_5),
        "total_iva_15": _fmt_nonzero_decimal(total_iva_15),
        "total_ice": _fmt_nonzero_decimal(total_ice),
        "total": _first_text_from(info_nota_debito, "valorTotal"),
    }


def _build_comprobante_context(info_nota_debito: Any) -> dict:
    tipo_comprobante_codigo = _first_text_from(info_nota_debito, "codDocModificado")
    tipo_comprobante_label = TIPO_COMPROBANTE_MAP.get(tipo_comprobante_codigo or "", tipo_comprobante_codigo)

    return {
        "tipo_comprobante": tipo_comprobante_label,
        "numero_comprobante": _first_text_from(info_nota_debito, "numDocModificado"),
        "fecha_comprobante": _first_text_from(info_nota_debito, "fechaEmisionDocSustento"),
    }


def _extract_pago_nodes(info_nota_debito: Any) -> list[Any]:
    pagos_directos = _walk_relative_nodes(info_nota_debito, "pagos.pago")
    if pagos_directos:
        return pagos_directos

    pagos_wrappers = _walk_relative_nodes(info_nota_debito, "pagos")
    if not pagos_wrappers:
        return []

    nodes: list[Any] = []
    for wrapper in pagos_wrappers:
        pago = _get_child(wrapper, "pago")
        if pago is None:
            continue
        if isinstance(pago, (list, tuple)):
            nodes.extend(item for item in pago if item is not None)
        else:
            nodes.append(pago)
    return nodes


def _sum_impuesto_field(
    impuesto_nodes: list[Any],
    *,
    codigo: str,
    field: str,
    codigo_porcentaje: str | None = None,
    codigo_porcentaje_in: set[str] | None = None,
) -> Decimal | None:
    total = Decimal("0")
    found = False

    for node in impuesto_nodes:
        codigo_val = _first_text_from(node, "codigo")
        if codigo_val != codigo:
            continue

        if codigo_porcentaje is not None or codigo_porcentaje_in is not None:
            cp_val = _first_text_from(node, "codigoPorcentaje")
            if codigo_porcentaje is not None and cp_val != codigo_porcentaje:
                continue
            if codigo_porcentaje_in is not None and cp_val not in codigo_porcentaje_in:
                continue

        dec = _to_decimal(_first_text_from(node, field))
        if dec is None:
            continue
        total += dec
        found = True

    if not found:
        return None
    return total


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


def _to_decimal(value: str | None) -> Decimal | None:
    if value is None:
        return None
    clean = value.strip().replace(",", "")
    if not clean:
        return None
    try:
        return Decimal(clean)
    except (InvalidOperation, ValueError):
        return None


def _fmt_nonzero_decimal(value: Decimal | None) -> str | None:
    if value is None:
        return None
    quantized = value.quantize(Q2, rounding=ROUND_HALF_UP)
    if quantized == Decimal("0.00"):
        return None
    return str(quantized)


def _fmt_or_default(value: Decimal | None, default: str) -> str:
    if value is None:
        return default
    return str(value.quantize(Q2, rounding=ROUND_HALF_UP))
