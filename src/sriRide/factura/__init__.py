from .anexos import construir_anexos_contexto
from .cliente import construir_cliente_contexto
from .doc import construir_doc_contexto
from .emisor import construir_emisor_contexto
from .exportador import construir_exportador_contexto
from .index import construir_contexto_desde_xml
from .normalizer import normalizar_factura
from .producto import construir_producto_contexto
from .reembolso import construir_reembolso_contexto
from .repetibles import construir_info_adicional_contexto, construir_pago_contexto
from .remision import construir_destino_contexto, construir_remision_contexto
from .totales import construir_totales_contexto
from .xml_utils import XmlInput

try:
    from src.sriRide.preproceso.preproceso_sri import SriPreprocesoResultado, preprocesar_xml_autorizado_sri # type: ignore
except ModuleNotFoundError:  # Compatibilidad cuando PYTHONPATH=src
    from sriRide.preproceso.preproceso_sri import SriPreprocesoResultado, preprocesar_xml_autorizado_sri


__all__ = [
    "construir_cliente_contexto",
    "construir_anexos_contexto",
    "construir_destino_contexto",
    "construir_doc_contexto",
    "construir_emisor_contexto",
    "construir_exportador_contexto",
    "construir_info_adicional_contexto",
    "construir_contexto_desde_xml",
    "normalizar_factura",
    "construir_pago_contexto",
    "preprocesar_xml_autorizado_sri",
    "construir_producto_contexto",
    "construir_reembolso_contexto",
    "construir_remision_contexto",
    "construir_totales_contexto",
    "SriPreprocesoResultado",
    "XmlInput",
]
