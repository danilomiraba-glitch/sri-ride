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
    "2": "Producción",
    "1": "Pruebas",
}

TIPO_EMISION_MAP = {
    "1": "Normal",
    "2": "Indisponibilidad del Sistema",
}


def normalizar_factura(factura_obj: Any) -> dict:
    info_tributaria = _first_node(factura_obj, "infoTributaria")
    info_factura = _first_node(factura_obj, "infoFactura")
    info_sustitutiva = _first_node(factura_obj, "infoSustitutivaGuiaRemision")
    detalles = _walk_path_nodes(factura_obj, "detalles.detalle")
    pagos = _walk_path_nodes(factura_obj, "infoFactura.pagos.pago")
    campos_adicionales = _walk_path_nodes(factura_obj, "infoAdicional.campoAdicional")
    impuestos = _walk_path_nodes(factura_obj, "infoFactura.totalConImpuestos.totalImpuesto")
    destinos = _walk_path_nodes(factura_obj, "infoSustitutivaGuiaRemision.destinos.destino")
    reembolso_detalles = _walk_path_nodes(factura_obj, "reembolsos.reembolsoDetalle")
    string_fields = _walk_path_nodes(factura_obj, "extensions.extension.StringField")

    doc = _build_doc_context(info_tributaria, info_factura, string_fields)
    emisor = _build_emisor_context(info_tributaria, info_factura)
    cliente = _build_cliente_context(info_factura)
    producto = _build_producto_context(detalles)
    pago = _build_pago_context(pagos)
    info_adicional = _build_info_adicional_context(campos_adicionales)
    totales = _build_totales_context(info_factura, impuestos)
    remision = _build_remision_context(info_sustitutiva)
    destino = _build_destino_context(destinos)
    exportador = _build_exportador_context(info_factura)
    reembolso = _build_reembolso_context(info_factura, reembolso_detalles)

    return {
        "doc": doc,
        "emisor": emisor,
        "cliente": cliente,
        "producto": producto,
        "pago": pago,
        "info_adicional": info_adicional,
        "totales": totales,
        "remision": remision,
        "destino": destino,
        "exportador": exportador,
        "reembolso": reembolso,
        "flags": {
            "remision_activa": bool(_walk_path_nodes(factura_obj, "infoSustitutivaGuiaRemision")),
            "exportador_activo": bool(_walk_path_nodes(factura_obj, "infoFactura.comercioExterior")),
            "reembolso_activo": bool(_walk_path_nodes(factura_obj, "infoFactura.codDocReembolso")),
        },
    }


def _build_doc_context(info_tributaria: Any, info_factura: Any, string_fields: list[Any]) -> dict:
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
        "cntrbynte_esp": _first_text_from(info_factura, "contribuyenteEspecial"),
        "agent_retencn": _first_text_from(info_tributaria, "agenteRetencion"),
    }


def _build_emisor_context(info_tributaria: Any, info_factura: Any) -> dict:
    regimen = _first_text_from(info_tributaria, "contribuyenteRimpe")
    if not regimen:
        regimen = "General"

    obligado_raw = _first_text_from(info_factura, "obligadoContabilidad")
    obligado = (obligado_raw or "").upper() if obligado_raw else obligado_raw

    return {
        "direccion": _first_text_from(info_tributaria, "dirMatriz"),
        "direccion_estab": _first_text_from(info_factura, "dirEstablecimiento"),
        "razon_social": _first_text_from(info_tributaria, "razonSocial"),
        "regimen": regimen,
        "obligado_contabilidad": obligado,
    }


def _build_cliente_context(info_factura: Any) -> dict:
    direccion = _first_text_from(info_factura, "direccionComprador")
    if not direccion:
        direccion = "---"

    return {
        "razon_social": _first_text_from(info_factura, "razonSocialComprador"),
        "identificacion": _first_text_from(info_factura, "identificacionComprador"),
        "direccion": direccion,
        "fecha_emision": _first_text_from(info_factura, "fechaEmision"),
        "guia_remision": _first_text_from(info_factura, "guiaRemision"),
        "placa": _first_text_from(info_factura, "placa") or "---",
    }


def _build_producto_context(detalles: list[Any]) -> dict:
    items: list[dict] = []
    for detalle in detalles:
        items.append(
            {
                "codigo": _first_text_from(detalle, "codigoPrincipal"),
                "descripcion": _first_text_from(detalle, "descripcion"),
                "detalle_adicional": _detalle_adicional_compuesto(detalle),
                "unidad_medida": _first_text_from(detalle, "unidadMedida") or "---",
                "cantidad": _first_text_from(detalle, "cantidad"),
                "precio_unitario": _first_text_from(detalle, "precioUnitario"),
                "descuento": _first_text_from(detalle, "descuento"),
                "precio_total": _first_text_from(detalle, "precioTotalSinImpuesto"),
            }
        )
    return {"items": items}


def _build_pago_context(pagos: list[Any]) -> dict:
    formas: list[dict] = []
    for pago in pagos:
        forma_codigo = _first_text_from(pago, "formaPago")
        plazo = _first_text_from(pago, "plazo")
        unidad_tiempo = _first_text_from(pago, "unidadTiempo")
        formas.append(
            {
                "forma_pago": FORMA_PAGO_MAP.get(forma_codigo or "", forma_codigo),
                "valor_pago": _first_text_from(pago, "total"),
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


def _build_totales_context(info_factura: Any, impuestos: list[Any]) -> dict:
    subtotal_iva_0 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="0", field="baseImponible")
    subtotal_iva_5 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="5", field="baseImponible")
    subtotal_iva_15 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="4", field="baseImponible")
    subtotal_objeto_exento = _sum_impuesto_field(
        impuestos,
        codigo="2",
        codigo_porcentaje_in={"6", "7"},
        field="baseImponible",
    )

    total_iva_5 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="5", field="valor")
    total_iva_15 = _sum_impuesto_field(impuestos, codigo="2", codigo_porcentaje="4", field="valor")
    total_ice = _sum_impuesto_field(impuestos, codigo="3", field="valor")

    propina = _to_decimal(_first_text_from(info_factura, "propina"))
    if propina is not None and propina <= 0:
        propina = None

    gastos_exportacion = _sum_values(
        [
            _first_text_from(info_factura, "fleteInternacional"),
            _first_text_from(info_factura, "seguroInternacional"),
            _first_text_from(info_factura, "gastosAduaneros"),
            _first_text_from(info_factura, "gastosTransporteOtros"),
        ]
    )

    return {
        "subtotal_iva_0": _fmt_or_default(subtotal_iva_0, "0.00"),
        "subtotal_iva_5": _fmt_nonzero_decimal(subtotal_iva_5),
        "subtotal_iva_15": _fmt_or_default(subtotal_iva_15, "0.00"),
        "subtotal_objeto_exento": _fmt_or_default(subtotal_objeto_exento, "0.00"),
        "subtotal_general": _first_text_from(info_factura, "totalSinImpuestos"),
        "total_descuento": _first_text_from(info_factura, "totalDescuento"),
        "total_iva_5": _fmt_nonzero_decimal(total_iva_5),
        "total_iva_15": _fmt_nonzero_decimal(total_iva_15),
        "total_ice": _fmt_nonzero_decimal(total_ice),
        "propina": _fmt_nonzero_decimal(propina),
        "gastos_exportacion": _fmt_nonzero_decimal(gastos_exportacion),
        "total": _first_text_from(info_factura, "importeTotal"),
    }


def _build_remision_context(info_sustitutiva: Any) -> dict:
    return {
        "partida": _first_text_from(info_sustitutiva, "dirPartida"),
        "destinatario": _first_text_from(info_sustitutiva, "dirDestinatario"),
        "placa": _first_text_from(info_sustitutiva, "placa"),
        "transportista": _first_text_from(info_sustitutiva, "razonSocialTransportista"),
        "ruc_transportista": _first_text_from(info_sustitutiva, "rucTransportista"),
        "inicio_transporte": _first_text_from(info_sustitutiva, "fechaIniTransporte"),
        "fin_transporte": _first_text_from(info_sustitutiva, "fechaFinTransporte"),
    }


def _build_destino_context(destinos: list[Any]) -> dict:
    items: list[dict] = []
    for idx, destino in enumerate(destinos, start=1):
        doc_aduanero = _first_text_from(destino, "docAduaneroUnico")
        if not doc_aduanero:
            doc_aduanero = "No Aplica"

        items.append(
            {
                "numero": str(idx),
                "motivo_traslado": _first_text_from(destino, "motivoTraslado"),
                "doc_aduanero": doc_aduanero,
                "cod_establecimiento_destino": _first_text_from(destino, "codEstabDestino"),
                "ruta_destino": _first_text_from(destino, "ruta"),
            }
        )
    return {"items": items}


def _build_exportador_context(info_factura: Any) -> dict:
    return {
        "incoterm": _first_text_from(info_factura, "incoTermFactura"),
        "lugar_incoterm": _first_text_from(info_factura, "lugarIncoTerm"),
        "incoterm_total": _first_text_from(info_factura, "incoTermTotalSinImpuestos"),
        "pais_origen": _first_text_from(info_factura, "paisOrigen"),
        "puerto_embarque": _first_text_from(info_factura, "puertoEmbarque"),
        "puerto_destino": _first_text_from(info_factura, "puertoDestino"),
        "pais_destino": _first_text_from(info_factura, "paisDestino"),
        "pais_adquisicion": _first_text_from(info_factura, "paisAdquisicion"),
        "flete_internacional": _first_text_from(info_factura, "fleteInternacional"),
        "seguro_internacional": _first_text_from(info_factura, "seguroInternacional"),
        "gastos_aduaneros": _first_text_from(info_factura, "gastosAduaneros"),
        "gastos_transporte_otros": _first_text_from(info_factura, "gastosTransporteOtros"),
    }


def _build_reembolso_context(info_factura: Any, detalles: list[Any]) -> dict:
    items: list[dict] = []
    subtotal_reembolso_sum = Decimal("0")
    total_impuestos_sum = Decimal("0")

    for detalle in detalles:
        numero_comprobante = _join_values(
            [
                _first_text_from(detalle, "estabDocReembolso"),
                _first_text_from(detalle, "ptoEmiDocReembolso"),
                _first_text_from(detalle, "secuencialDocReembolso"),
            ],
            separator="-",
        )

        subtotal_item = _sum_relative_path(detalle, "detalleImpuestos.detalleImpuesto.baseImponibleReembolso")
        impuestos_item = _sum_relative_path(detalle, "detalleImpuestos.detalleImpuesto.impuestoReembolso")
        total_item = (subtotal_item or Decimal("0")) + (impuestos_item or Decimal("0"))

        if subtotal_item is not None:
            subtotal_reembolso_sum += subtotal_item
        if impuestos_item is not None:
            total_impuestos_sum += impuestos_item

        items.append(
            {
                "ruc_reembolso": _first_text_from(detalle, "identificacionProveedorReembolso"),
                "fecha_emision": _first_text_from(detalle, "fechaEmisionDocReembolso"),
                "numero_autorizacion": _first_text_from(detalle, "numeroautorizacionDocReembolso"),
                "numero_comprobante": numero_comprobante,
                "subtotal_reembolso": _fmt_decimal(subtotal_item),
                "total_impuestos": _fmt_decimal(impuestos_item),
                "total_reembolso": _fmt_decimal(total_item),
            }
        )

    total_comprobantes = len(detalles)
    subtotal_reembolso = _fmt_decimal(subtotal_reembolso_sum if detalles else None)
    total_impuestos = _fmt_decimal(total_impuestos_sum if detalles else None)
    total_reembolso = _fmt_decimal((subtotal_reembolso_sum + total_impuestos_sum) if detalles else None)

    return {
        "items": items,
        "ruc_reembolso": items[0]["ruc_reembolso"] if items else None,
        "fecha_emision": items[0]["fecha_emision"] if items else None,
        "numero_autorizacion": items[0]["numero_autorizacion"] if items else None,
        "numero_comprobante": items[0]["numero_comprobante"] if items else None,
        "total_base_reembolsos": _first_text_from(info_factura, "totalBaseImponibleReembolso"),
        "total_impuestos_reembolsos": _first_text_from(info_factura, "totalImpuestoReembolso"),
        "total_todos_reembolsos": _first_text_from(info_factura, "totalComprobantesReembolso"),
        "total_comprobantes": str(total_comprobantes) if detalles else None,
        "subtotal_reembolso": subtotal_reembolso,
        "total_impuestos": total_impuestos,
        "total_reembolso": total_reembolso,
    }


def _detalle_adicional_compuesto(detalle: Any) -> str | None:
    det_adicional_nodes = _walk_relative_nodes(detalle, "detallesAdicionales.detAdicional")
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


def _sum_relative_path(node: Any, dot_path: str) -> Decimal | None:
    total = Decimal("0")
    found = False
    for current in _walk_relative_nodes(node, dot_path):
        dec = _to_decimal(_node_text(current))
        if dec is None:
            continue
        total += dec
        found = True
    if not found:
        return None
    return total


def _sum_values(values: list[str | None]) -> Decimal | None:
    total = Decimal("0")
    found = False
    for value in values:
        dec = _to_decimal(value)
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
    # Eliminamos duplicados preservando orden.
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


def _fmt_decimal(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return str(value.quantize(Q2, rounding=ROUND_HALF_UP))


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
