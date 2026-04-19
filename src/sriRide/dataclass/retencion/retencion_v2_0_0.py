from __future__ import annotations

from typing import Optional
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from ..signature.xmldsig_core_schema import Signature


@dataclass(repr=False, eq=False, kw_only=True)
class CompraCajBanano:
    class Meta:
        name = "compraCajBanano"

    num_caj_ban: Optional[str] = field(default=None, metadata={
            "name": "numCajBan",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{1,7}",
        })
    prec_caj_ban: Decimal = field(
        metadata={
            "name": "precCajBan",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )


class ComprobanteRetencionId(Enum):
    COMPROBANTE = "comprobante"


@dataclass(repr=False, eq=False, kw_only=True)
class DetalleImpuesto:
    class Meta:
        name = "detalleImpuesto"

    codigo: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"[235]",
        })
    codigo_porcentaje: Optional[str] = field(default=None, metadata={
            "name": "codigoPorcentaje",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{1,4}",
        })
    tarifa: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{1,4}",
        })
    base_imponible_reembolso: Decimal = field(
        metadata={
            "name": "baseImponibleReembolso",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )
    impuesto_reembolso: Decimal = field(
        metadata={
            "name": "impuestoReembolso",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )


@dataclass(repr=False, eq=False, kw_only=True)
class Dividendos:
    class Meta:
        name = "dividendos"

    fecha_pago_div: str = field(
        metadata={
            "name": "fechaPagoDiv",
            "type": "Element",
            "namespace": "",
            "pattern": r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/20[0-9][0-9]",
        }
    )
    im_renta_soc: Decimal = field(
        metadata={
            "name": "imRentaSoc",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )
    ejer_fis_ut_div: str = field(
        metadata={
            "name": "ejerFisUtDiv",
            "type": "Element",
            "namespace": "",
            "pattern": r"(19|20)[0-9]{2}",
        }
    )


@dataclass(repr=False, eq=False, kw_only=True)
class ImpuestoDocSustento:
    class Meta:
        name = "impuestoDocSustento"

    cod_impuesto_doc_sustento: Optional[str] = field(default=None, metadata={
            "name": "codImpuestoDocSustento",
            "type": "Element",
            "namespace": "",
            "pattern": r"[235]{1}",
        })
    codigo_porcentaje: Optional[str] = field(default=None, metadata={
            "name": "codigoPorcentaje",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{1,4}",
        })
    base_imponible: Decimal = field(
        metadata={
            "name": "baseImponible",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )
    tarifa: Decimal = field(
        metadata={
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0"),
            "total_digits": 3,
            "fraction_digits": 2,
        }
    )
    valor_impuesto: Decimal = field(
        metadata={
            "name": "valorImpuesto",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )


@dataclass(repr=False, eq=False, kw_only=True)
class InfoTributaria:
    class Meta:
        name = "infoTributaria"

    ambiente: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"[1-2]{1}",
        })
    tipo_emision: Optional[str] = field(default=None, metadata={
            "name": "tipoEmision",
            "type": "Element",
            "namespace": "",
            "pattern": r"[12]{1}",
        })
    razon_social: Optional[str] = field(default=None, metadata={
            "name": "razonSocial",
            "type": "Element",
            "namespace": "",
            "min_length": 1,
            "max_length": 300,
            "pattern": r"[^\n]*",
        })
    nombre_comercial: None | str = field(
        default=None,
        metadata={
            "name": "nombreComercial",
            "type": "Element",
            "namespace": "",
            "min_length": 1,
            "max_length": 300,
            "pattern": r"[^\n]*",
        },
    )
    ruc: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{10}001",
        })
    clave_acceso: Optional[str] = field(default=None, metadata={
            "name": "claveAcceso",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{49}",
        })
    cod_doc: Optional[str] = field(default=None, metadata={
            "name": "codDoc",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{2}",
        })
    estab: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{3}",
        })
    pto_emi: Optional[str] = field(default=None, metadata={
            "name": "ptoEmi",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{3}",
        })
    secuencial: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{9}",
        })
    dir_matriz: Optional[str] = field(default=None, metadata={
            "name": "dirMatriz",
            "type": "Element",
            "namespace": "",
            "min_length": 1,
            "max_length": 300,
            "white_space": "preserve",
            "pattern": r"[^\n]*",
        })
    agente_retencion: None | str = field(
        default=None,
        metadata={
            "name": "agenteRetencion",
            "type": "Element",
            "namespace": "",
            "max_length": 8,
            "pattern": r"[0-9]+",
        },
    )
    contribuyente_rimpe: None | str = field(
        default=None,
        metadata={
            "name": "contribuyenteRimpe",
            "type": "Element",
            "namespace": "",
            "pattern": r"CONTRIBUYENTE RÉGIMEN RIMPE",
        },
    )


@dataclass(repr=False, eq=False, kw_only=True)
class MaquinaFiscal:
    class Meta:
        name = "maquinaFiscal"

    marca: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "namespace": "",
            "min_length": 1,
            "max_length": 30,
            "pattern": r"[^\n]*",
        })
    modelo: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "namespace": "",
            "min_length": 1,
            "max_length": 30,
            "pattern": r"[^\n]*",
        })
    serie: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "namespace": "",
            "min_length": 1,
            "max_length": 30,
            "pattern": r"[^\n]*",
        })


class ObligadoContabilidad(Enum):
    SI = "SI"
    NO = "NO"


@dataclass(repr=False, eq=False, kw_only=True)
class Pago:
    class Meta:
        name = "pago"

    forma_pago: Optional[str] = field(default=None, metadata={
            "name": "formaPago",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0][1-9]|[1][0-9]|[2][0-1]",
        })
    total: Decimal = field(
        metadata={
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )


@dataclass(repr=False, eq=False, kw_only=True)
class DetalleImpuestos:
    class Meta:
        name = "detalleImpuestos"

    detalle_impuesto: list[DetalleImpuesto] = field(
        default_factory=list,
        metadata={
            "name": "detalleImpuesto",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )


@dataclass(repr=False, eq=False, kw_only=True)
class ImpuestosDocSustento:
    class Meta:
        name = "impuestosDocSustento"

    impuesto_doc_sustento: list[ImpuestoDocSustento] = field(
        default_factory=list,
        metadata={
            "name": "impuestoDocSustento",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )


@dataclass(repr=False, eq=False, kw_only=True)
class Pagos:
    class Meta:
        name = "pagos"

    pago: list[Pago] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )


@dataclass(repr=False, eq=False, kw_only=True)
class Retencion:
    class Meta:
        name = "retencion"

    codigo: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"[126]{1}",
        })
    codigo_retencion: Optional[str] = field(default=None, metadata={
            "name": "codigoRetencion",
            "type": "Element",
            "namespace": "",
            "min_length": 1,
            "max_length": 5,
            "pattern": r"[^\n]*",
        })
    base_imponible: Decimal = field(
        metadata={
            "name": "baseImponible",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )
    porcentaje_retener: Decimal = field(
        metadata={
            "name": "porcentajeRetener",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0"),
            "total_digits": 3,
            "fraction_digits": 2,
        }
    )
    valor_retenido: Decimal = field(
        metadata={
            "name": "valorRetenido",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )
    dividendos: None | Dividendos = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    compra_caj_banano: None | CompraCajBanano = field(
        default=None,
        metadata={
            "name": "compraCajBanano",
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(repr=False, eq=False, kw_only=True)
class Reembolsos:
    class Meta:
        name = "reembolsos"

    reembolso_detalle: list[Reembolsos.ReembolsoDetalle] = field(
        default_factory=list,
        metadata={
            "name": "reembolsoDetalle",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )

    @dataclass(repr=False, eq=False, kw_only=True)
    class ReembolsoDetalle:
        tipo_identificacion_proveedor_reembolso: Optional[str] = field(default=None, metadata={
                "name": "tipoIdentificacionProveedorReembolso",
                "type": "Element",
                "namespace": "",
                "pattern": r"[0][4-8]",
            })
        identificacion_proveedor_reembolso: Optional[str] = field(default=None, metadata={
                "name": "identificacionProveedorReembolso",
                "type": "Element",
                "namespace": "",
                "min_length": 1,
                "max_length": 20,
                "pattern": r"[^\n]*",
            })
        cod_pais_pago_proveedor_reembolso: None | str = field(
            default=None,
            metadata={
                "name": "codPaisPagoProveedorReembolso",
                "type": "Element",
                "namespace": "",
                "pattern": r"[0-9]{3}",
            },
        )
        tipo_proveedor_reembolso: Optional[str] = field(default=None, metadata={
                "name": "tipoProveedorReembolso",
                "type": "Element",
                "namespace": "",
                "pattern": r"[0][12]",
            })
        cod_doc_reembolso: Optional[str] = field(default=None, metadata={
                "name": "codDocReembolso",
                "type": "Element",
                "namespace": "",
                "pattern": r"[0-9]{2}",
            })
        estab_doc_reembolso: Optional[str] = field(default=None, metadata={
                "name": "estabDocReembolso",
                "type": "Element",
                "namespace": "",
                "pattern": r"[0-9]{3}",
            })
        pto_emi_doc_reembolso: Optional[str] = field(default=None, metadata={
                "name": "ptoEmiDocReembolso",
                "type": "Element",
                "namespace": "",
                "pattern": r"[0-9]{3}",
            })
        secuencial_doc_reembolso: Optional[str] = field(default=None, metadata={
                "name": "secuencialDocReembolso",
                "type": "Element",
                "namespace": "",
                "pattern": r"[0-9]{9}",
            })
        fecha_emision_doc_reembolso: str = field(
            metadata={
                "name": "fechaEmisionDocReembolso",
                "type": "Element",
                "namespace": "",
                "pattern": r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/20[0-9][0-9]",
            }
        )
        numero_autorizacion_doc_reemb: Optional[str] = field(default=None, metadata={
                "name": "numeroAutorizacionDocReemb",
                "type": "Element",
                "namespace": "",
                "min_length": 10,
                "max_length": 49,
                "pattern": r"[0-9]{10,49}",
            })
        detalle_impuestos: Optional[DetalleImpuestos] = field(default=None, metadata={
                "name": "detalleImpuestos",
                "type": "Element",
                "namespace": "",
            })


@dataclass(repr=False, eq=False, kw_only=True)
class Retenciones:
    class Meta:
        name = "retenciones"

    retencion: list[Retencion] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )


@dataclass(repr=False, eq=False, kw_only=True)
class DocSustento:
    class Meta:
        name = "docSustento"

    cod_sustento: Optional[str] = field(default=None, metadata={
            "name": "codSustento",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{2}",
        })
    cod_doc_sustento: Optional[str] = field(default=None, metadata={
            "name": "codDocSustento",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{1,3}",
        })
    num_doc_sustento: Optional[str] = field(default=None, metadata={
            "name": "numDocSustento",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{15}",
        })
    fecha_emision_doc_sustento: str = field(
        metadata={
            "name": "fechaEmisionDocSustento",
            "type": "Element",
            "namespace": "",
            "pattern": r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/20[0-9][0-9]",
        }
    )
    fecha_registro_contable: None | str = field(
        default=None,
        metadata={
            "name": "fechaRegistroContable",
            "type": "Element",
            "namespace": "",
            "pattern": r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/20[0-9][0-9]",
        },
    )
    num_aut_doc_sustento: None | str = field(
        default=None,
        metadata={
            "name": "numAutDocSustento",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{10,49}",
        },
    )
    pago_loc_ext: Optional[str] = field(default=None, metadata={
            "name": "pagoLocExt",
            "type": "Element",
            "namespace": "",
            "pattern": r"01|02",
        })
    tipo_regi: None | str = field(
        default=None,
        metadata={
            "name": "tipoRegi",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{2}",
        },
    )
    pais_efec_pago: None | str = field(
        default=None,
        metadata={
            "name": "paisEfecPago",
            "type": "Element",
            "namespace": "",
            "pattern": r"[0-9]{3,4}",
        },
    )
    aplic_conv_dob_trib: None | str = field(
        default=None,
        metadata={
            "name": "aplicConvDobTrib",
            "type": "Element",
            "namespace": "",
            "pattern": r"SI|NO",
        },
    )
    pag_ext_suj_ret_nor_leg: None | str = field(
        default=None,
        metadata={
            "name": "pagExtSujRetNorLeg",
            "type": "Element",
            "namespace": "",
            "pattern": r"SI|NO",
        },
    )
    pago_reg_fis: None | str = field(
        default=None,
        metadata={
            "name": "pagoRegFis",
            "type": "Element",
            "namespace": "",
            "pattern": r"SI|NO",
        },
    )
    total_comprobantes_reembolso: None | Decimal = field(
        default=None,
        metadata={
            "name": "totalComprobantesReembolso",
            "type": "Element",
            "namespace": "",
            "total_digits": 14,
            "fraction_digits": 2,
        },
    )
    total_base_imponible_reembolso: None | Decimal = field(
        default=None,
        metadata={
            "name": "totalBaseImponibleReembolso",
            "type": "Element",
            "namespace": "",
            "total_digits": 14,
            "fraction_digits": 2,
        },
    )
    total_impuesto_reembolso: None | Decimal = field(
        default=None,
        metadata={
            "name": "totalImpuestoReembolso",
            "type": "Element",
            "namespace": "",
            "total_digits": 14,
            "fraction_digits": 2,
        },
    )
    total_sin_impuestos: Optional[Decimal] = field(default=None, metadata={
            "name": "totalSinImpuestos",
            "type": "Element",
            "namespace": "",
            "total_digits": 14,
            "fraction_digits": 2,
        })
    importe_total: Decimal = field(
        metadata={
            "name": "importeTotal",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )
    impuestos_doc_sustento: Optional[ImpuestosDocSustento] = field(default=None, metadata={
            "name": "impuestosDocSustento",
            "type": "Element",
            "namespace": "",
        })
    retenciones: Optional[Retenciones] = field(default=None, metadata={
            "type": "Element",
            "namespace": "",
        })
    reembolsos: None | Reembolsos = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pagos: Optional[Pagos] = field(default=None, metadata={
            "type": "Element",
            "namespace": "",
        })


@dataclass(repr=False, eq=False, kw_only=True)
class ComprobanteRetencion:
    class Meta:
        name = "comprobanteRetencion"

    info_tributaria: Optional[InfoTributaria] = field(default=None, metadata={
            "name": "infoTributaria",
            "type": "Element",
            "namespace": "",
        })
    info_comp_retencion: Optional[ComprobanteRetencion.InfoCompRetencion] = field(default=None, metadata={
            "name": "infoCompRetencion",
            "type": "Element",
            "namespace": "",
        })
    docs_sustento: Optional[ComprobanteRetencion.DocsSustento] = field(default=None, metadata={
            "name": "docsSustento",
            "type": "Element",
            "namespace": "",
        })
    maquina_fiscal: None | MaquinaFiscal = field(
        default=None,
        metadata={
            "name": "maquinaFiscal",
            "type": "Element",
            "namespace": "",
        },
    )
    info_adicional: None | ComprobanteRetencion.InfoAdicional = field(
        default=None,
        metadata={
            "name": "infoAdicional",
            "type": "Element",
            "namespace": "",
        },
    )
    signature: None | Signature = field(
        default=None,
        metadata={
            "name": "Signature",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        },
    )
    id: None | ComprobanteRetencionId = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    version: Optional[str] = field(default=None, metadata={
            "type": "Attribute",
        })

    @dataclass(repr=False, eq=False, kw_only=True)
    class InfoCompRetencion:
        fecha_emision: str = field(
            metadata={
                "name": "fechaEmision",
                "type": "Element",
                "namespace": "",
                "pattern": r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/20[0-9][0-9]",
            }
        )
        dir_establecimiento: None | str = field(
            default=None,
            metadata={
                "name": "dirEstablecimiento",
                "type": "Element",
                "namespace": "",
                "min_length": 1,
                "max_length": 300,
                "pattern": r"[^\n]*",
            },
        )
        contribuyente_especial: None | str = field(
            default=None,
            metadata={
                "name": "contribuyenteEspecial",
                "type": "Element",
                "namespace": "",
                "min_length": 3,
                "max_length": 5,
                "pattern": r"([A-Za-z0-9])*",
            },
        )
        obligado_contabilidad: None | ObligadoContabilidad = field(
            default=None,
            metadata={
                "name": "obligadoContabilidad",
                "type": "Element",
                "namespace": "",
            },
        )
        tipo_identificacion_sujeto_retenido: Optional[str] = field(default=None, metadata={
                "name": "tipoIdentificacionSujetoRetenido",
                "type": "Element",
                "namespace": "",
                "pattern": r"[0][4-8]",
            })
        tipo_sujeto_retenido: None | str = field(
            default=None,
            metadata={
                "name": "tipoSujetoRetenido",
                "type": "Element",
                "namespace": "",
                "pattern": r"01|02",
            },
        )
        parte_rel: Optional[str] = field(default=None, metadata={
                "name": "parteRel",
                "type": "Element",
                "namespace": "",
                "pattern": r"SI|NO",
            })
        razon_social_sujeto_retenido: Optional[str] = field(default=None, metadata={
                "name": "razonSocialSujetoRetenido",
                "type": "Element",
                "namespace": "",
                "min_length": 1,
                "max_length": 300,
                "pattern": r"[^\n]*",
            })
        identificacion_sujeto_retenido: Optional[str] = field(default=None, metadata={
                "name": "identificacionSujetoRetenido",
                "type": "Element",
                "namespace": "",
                "min_length": 1,
                "max_length": 20,
                "pattern": r"[^\n]*",
            })
        periodo_fiscal: str = field(
            metadata={
                "name": "periodoFiscal",
                "type": "Element",
                "namespace": "",
                "pattern": r"(0[1-9]|1[012])/20[0-9][0-9]",
            }
        )

    @dataclass(repr=False, eq=False, kw_only=True)
    class DocsSustento:
        doc_sustento: list[DocSustento] = field(
            default_factory=list,
            metadata={
                "name": "docSustento",
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
            },
        )

    @dataclass(repr=False, eq=False, kw_only=True)
    class InfoAdicional:
        campo_adicional: list[
            ComprobanteRetencion.InfoAdicional.CampoAdicional
        ] = field(
            default_factory=list,
            metadata={
                "name": "campoAdicional",
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
                "max_occurs": 15,
            },
        )

        @dataclass(repr=False, eq=False, kw_only=True)
        class CampoAdicional:
            value: str = field(
                default="",
                metadata={
                    "min_length": 1,
                    "max_length": 300,
                    "pattern": r"[^\n]*",
                },
            )
            nombre: Optional[str] = field(default=None, metadata={
                    "type": "Attribute",
                    "min_length": 1,
                    "max_length": 300,
                    "pattern": r"[^\n]*",
                })
