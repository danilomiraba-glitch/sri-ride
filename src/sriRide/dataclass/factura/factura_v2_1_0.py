from __future__ import annotations

from typing import Optional
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from ..signature.xmldsig_core_schema import Signature


@dataclass(repr=False, eq=False, kw_only=True)
class Compensacion:
    class Meta:
        name = "compensacion"

    codigo: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "pattern": r"1",
        })
    tarifa: Decimal = field(
        metadata={
            "type": "Element",
            "min_inclusive": Decimal("0"),
            "total_digits": 4,
            "fraction_digits": 2,
        }
    )
    valor: Decimal = field(
        metadata={
            "type": "Element",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )


@dataclass(repr=False, eq=False, kw_only=True)
class Destino:
    class Meta:
        name = "destino"

    motivo_traslado: Optional[str] = field(default=None, metadata={
            "name": "motivoTraslado",
            "type": "Element",
            "min_length": 1,
            "max_length": 300,
            "pattern": r"[^\n]*",
        })
    doc_aduanero_unico: None | str = field(
        default=None,
        metadata={
            "name": "docAduaneroUnico",
            "type": "Element",
            "min_length": 1,
            "max_length": 64,
            "pattern": r"[^\n]*",
        },
    )
    cod_estab_destino: None | str = field(
        default=None,
        metadata={
            "name": "codEstabDestino",
            "type": "Element",
            "pattern": r"[0-9]{3}",
        },
    )
    ruta: None | str = field(
        default=None,
        metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 300,
            "pattern": r"[^\n]*",
        },
    )


@dataclass(repr=False, eq=False, kw_only=True)
class DetalleImpuestos:
    class Meta:
        name = "detalleImpuestos"

    detalle_impuesto: list[DetalleImpuestos.DetalleImpuesto] = field(
        default_factory=list,
        metadata={
            "name": "detalleImpuesto",
            "type": "Element",
            "min_occurs": 1,
        },
    )

    @dataclass(repr=False, eq=False, kw_only=True)
    class DetalleImpuesto:
        codigo: Optional[str] = field(default=None, metadata={
                "type": "Element",
                "pattern": r"[235]",
            })
        codigo_porcentaje: Optional[str] = field(default=None, metadata={
                "name": "codigoPorcentaje",
                "type": "Element",
                "pattern": r"[0-9]{1,4}",
            })
        tarifa: Decimal = field(
            metadata={
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 4,
                "fraction_digits": 2,
            }
        )
        base_imponible_reembolso: Decimal = field(
            metadata={
                "name": "baseImponibleReembolso",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            }
        )
        impuesto_reembolso: Decimal = field(
            metadata={
                "name": "impuestoReembolso",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            }
        )


class FacturaId(Enum):
    COMPROBANTE = "comprobante"


@dataclass(repr=False, eq=False, kw_only=True)
class Impuesto:
    class Meta:
        name = "impuesto"

    codigo: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 1,
            "pattern": r"[235]",
        })
    codigo_porcentaje: Optional[str] = field(default=None, metadata={
            "name": "codigoPorcentaje",
            "type": "Element",
            "min_length": 1,
            "max_length": 4,
            "pattern": r"[0-9]+",
        })
    tarifa: Decimal = field(
        metadata={
            "type": "Element",
            "min_inclusive": Decimal("0"),
            "total_digits": 4,
            "fraction_digits": 2,
        }
    )
    base_imponible: Decimal = field(
        metadata={
            "name": "baseImponible",
            "type": "Element",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )
    valor: Decimal = field(
        metadata={
            "type": "Element",
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
            "pattern": r"[1-2]{1}",
        })
    tipo_emision: Optional[str] = field(default=None, metadata={
            "name": "tipoEmision",
            "type": "Element",
            "pattern": r"[12]{1}",
        })
    razon_social: Optional[str] = field(default=None, metadata={
            "name": "razonSocial",
            "type": "Element",
            "min_length": 1,
            "max_length": 300,
            "pattern": r"[^\n]*",
        })
    nombre_comercial: None | str = field(
        default=None,
        metadata={
            "name": "nombreComercial",
            "type": "Element",
            "min_length": 1,
            "max_length": 300,
            "pattern": r"[^\n]*",
        },
    )
    ruc: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "pattern": r"[0-9]{10}001",
        })
    clave_acceso: Optional[str] = field(default=None, metadata={
            "name": "claveAcceso",
            "type": "Element",
            "pattern": r"[0-9]{49}",
        })
    cod_doc: Optional[str] = field(default=None, metadata={
            "name": "codDoc",
            "type": "Element",
            "pattern": r"[0-9]{2}",
        })
    estab: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "pattern": r"[0-9]{3}",
        })
    pto_emi: Optional[str] = field(default=None, metadata={
            "name": "ptoEmi",
            "type": "Element",
            "pattern": r"[0-9]{3}",
        })
    secuencial: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "pattern": r"[0-9]{9}",
        })
    dir_matriz: Optional[str] = field(default=None, metadata={
            "name": "dirMatriz",
            "type": "Element",
            "min_length": 1,
            "max_length": 300,
            "pattern": r"[^\n]*",
        })
    agente_retencion: None | str = field(
        default=None,
        metadata={
            "name": "agenteRetencion",
            "type": "Element",
            "max_length": 8,
            "pattern": r"[0-9]+",
        },
    )
    contribuyente_rimpe: None | str = field(
        default=None,
        metadata={
            "name": "contribuyenteRimpe",
            "type": "Element",
            "pattern": r"CONTRIBUYENTE RÉGIMEN RIMPE",
        },
    )


@dataclass(repr=False, eq=False, kw_only=True)
class MaquinaFiscal:
    class Meta:
        name = "maquinaFiscal"

    marca: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 30,
            "pattern": r"[^\n]*",
        })
    modelo: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 30,
            "pattern": r"[^\n]*",
        })
    serie: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 30,
            "pattern": r"[^\n]*",
        })


class ObligadoContabilidad(Enum):
    SI = "SI"
    NO = "NO"


@dataclass(repr=False, eq=False, kw_only=True)
class Pagos:
    class Meta:
        name = "pagos"

    pago: list[Pagos.Pago] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )

    @dataclass(repr=False, eq=False, kw_only=True)
    class Pago:
        forma_pago: Optional[str] = field(default=None, metadata={
                "name": "formaPago",
                "type": "Element",
                "pattern": r"[0][1-9]|[1][0-9]|[2][0-1]",
            })
        total: Decimal = field(
            metadata={
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            }
        )
        plazo: None | Decimal = field(
            default=None,
            metadata={
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            },
        )
        unidad_tiempo: None | str = field(
            default=None,
            metadata={
                "name": "unidadTiempo",
                "type": "Element",
                "min_length": 1,
                "max_length": 10,
                "pattern": r"[^\n]*",
            },
        )


@dataclass(repr=False, eq=False, kw_only=True)
class Rubro:
    class Meta:
        name = "rubro"

    concepto: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 300,
            "pattern": r"[^\n]*",
        })
    total: Decimal = field(
        metadata={
            "type": "Element",
            "min_inclusive": Decimal("0"),
            "total_digits": 14,
            "fraction_digits": 2,
        }
    )


@dataclass(repr=False, eq=False, kw_only=True)
class TipoNegociable:
    class Meta:
        name = "tipoNegociable"

    correo: Optional[str] = field(default=None, metadata={
            "type": "Element",
            "min_length": 1,
            "max_length": 100,
            "pattern": r"[^\n]*",
        })


@dataclass(repr=False, eq=False, kw_only=True)
class Compensaciones:
    class Meta:
        name = "compensaciones"

    compensacion: list[Compensacion] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass(repr=False, eq=False, kw_only=True)
class CompensacionesReembolso:
    class Meta:
        name = "compensacionesReembolso"

    compensacion_reembolso: list[Compensacion] = field(
        default_factory=list,
        metadata={
            "name": "compensacionReembolso",
            "type": "Element",
            "min_occurs": 1,
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
            "min_occurs": 1,
        },
    )

    @dataclass(repr=False, eq=False, kw_only=True)
    class ReembolsoDetalle:
        tipo_identificacion_proveedor_reembolso: Optional[str] = field(default=None, metadata={
                "name": "tipoIdentificacionProveedorReembolso",
                "type": "Element",
                "pattern": r"[0][4-8]",
            })
        identificacion_proveedor_reembolso: Optional[str] = field(default=None, metadata={
                "name": "identificacionProveedorReembolso",
                "type": "Element",
                "min_length": 1,
                "max_length": 20,
                "pattern": r"[^\n]*",
            })
        cod_pais_pago_proveedor_reembolso: None | str = field(
            default=None,
            metadata={
                "name": "codPaisPagoProveedorReembolso",
                "type": "Element",
                "pattern": r"[0-9]{3}",
            },
        )
        tipo_proveedor_reembolso: Optional[str] = field(default=None, metadata={
                "name": "tipoProveedorReembolso",
                "type": "Element",
                "pattern": r"[0][12]",
            })
        cod_doc_reembolso: Optional[str] = field(default=None, metadata={
                "name": "codDocReembolso",
                "type": "Element",
                "pattern": r"[0-9]{2,3}",
            })
        estab_doc_reembolso: Optional[str] = field(default=None, metadata={
                "name": "estabDocReembolso",
                "type": "Element",
                "pattern": r"[0-9]{3}",
            })
        pto_emi_doc_reembolso: Optional[str] = field(default=None, metadata={
                "name": "ptoEmiDocReembolso",
                "type": "Element",
                "pattern": r"[0-9]{3}",
            })
        secuencial_doc_reembolso: Optional[str] = field(default=None, metadata={
                "name": "secuencialDocReembolso",
                "type": "Element",
                "pattern": r"[0-9]{9}",
            })
        fecha_emision_doc_reembolso: str = field(
            metadata={
                "name": "fechaEmisionDocReembolso",
                "type": "Element",
                "pattern": r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/20[0-9][0-9]",
            }
        )
        numeroautorizacion_doc_reemb: Optional[str] = field(default=None, metadata={
                "name": "numeroautorizacionDocReemb",
                "type": "Element",
                "min_length": 10,
                "max_length": 49,
                "pattern": r"[0-9]{10,49}",
            })
        detalle_impuestos: Optional[DetalleImpuestos] = field(default=None, metadata={
                "name": "detalleImpuestos",
                "type": "Element",
            })
        compensaciones_reembolso: None | CompensacionesReembolso = field(
            default=None,
            metadata={
                "name": "compensacionesReembolso",
                "type": "Element",
            },
        )


@dataclass(repr=False, eq=False, kw_only=True)
class Factura:
    class Meta:
        name = "factura"

    info_tributaria: Optional[InfoTributaria] = field(default=None, metadata={
            "name": "infoTributaria",
            "type": "Element",
        })
    info_factura: Optional[Factura.InfoFactura] = field(default=None, metadata={
            "name": "infoFactura",
            "type": "Element",
        })
    detalles: Optional[Factura.Detalles] = field(default=None, metadata={
            "type": "Element",
        })
    reembolsos: None | Reembolsos = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    retenciones: None | Factura.Retenciones = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    info_sustitutiva_guia_remision: (
        None | Factura.InfoSustitutivaGuiaRemision
    ) = field(
        default=None,
        metadata={
            "name": "infoSustitutivaGuiaRemision",
            "type": "Element",
        },
    )
    otros_rubros_terceros: None | Factura.OtrosRubrosTerceros = field(
        default=None,
        metadata={
            "name": "otrosRubrosTerceros",
            "type": "Element",
        },
    )
    tipo_negociable: None | TipoNegociable = field(
        default=None,
        metadata={
            "name": "tipoNegociable",
            "type": "Element",
        },
    )
    maquina_fiscal: None | MaquinaFiscal = field(
        default=None,
        metadata={
            "name": "maquinaFiscal",
            "type": "Element",
        },
    )
    info_adicional: None | Factura.InfoAdicional = field(
        default=None,
        metadata={
            "name": "infoAdicional",
            "type": "Element",
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
    id: None | FacturaId = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    version: None | object = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass(repr=False, eq=False, kw_only=True)
    class InfoFactura:
        fecha_emision: str = field(
            metadata={
                "name": "fechaEmision",
                "type": "Element",
                "pattern": r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/20[0-9][0-9]",
            }
        )
        dir_establecimiento: None | str = field(
            default=None,
            metadata={
                "name": "dirEstablecimiento",
                "type": "Element",
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
                "min_length": 3,
                "max_length": 13,
                "pattern": r"([A-Za-z0-9])*",
            },
        )
        obligado_contabilidad: None | ObligadoContabilidad = field(
            default=None,
            metadata={
                "name": "obligadoContabilidad",
                "type": "Element",
            },
        )
        comercio_exterior: None | str = field(
            default=None,
            metadata={
                "name": "comercioExterior",
                "type": "Element",
                "pattern": r"EXPORTADOR",
            },
        )
        inco_term_factura: None | str = field(
            default=None,
            metadata={
                "name": "incoTermFactura",
                "type": "Element",
                "min_length": 1,
                "max_length": 10,
                "pattern": r"([A-Z])*",
            },
        )
        lugar_inco_term: None | str = field(
            default=None,
            metadata={
                "name": "lugarIncoTerm",
                "type": "Element",
                "min_length": 1,
                "max_length": 300,
                "pattern": r"[^\n]*",
            },
        )
        pais_origen: None | str = field(
            default=None,
            metadata={
                "name": "paisOrigen",
                "type": "Element",
                "pattern": r"[0-9]{3}",
            },
        )
        puerto_embarque: None | str = field(
            default=None,
            metadata={
                "name": "puertoEmbarque",
                "type": "Element",
                "min_length": 1,
                "max_length": 300,
                "pattern": r"[^\n]*",
            },
        )
        puerto_destino: None | str = field(
            default=None,
            metadata={
                "name": "puertoDestino",
                "type": "Element",
                "min_length": 1,
                "max_length": 300,
                "pattern": r"[^\n]*",
            },
        )
        pais_destino: None | str = field(
            default=None,
            metadata={
                "name": "paisDestino",
                "type": "Element",
                "pattern": r"[0-9]{3}",
            },
        )
        pais_adquisicion: None | str = field(
            default=None,
            metadata={
                "name": "paisAdquisicion",
                "type": "Element",
                "pattern": r"[0-9]{3}",
            },
        )
        tipo_identificacion_comprador: Optional[str] = field(default=None, metadata={
                "name": "tipoIdentificacionComprador",
                "type": "Element",
                "pattern": r"[0][4-8]",
            })
        guia_remision: None | str = field(
            default=None,
            metadata={
                "name": "guiaRemision",
                "type": "Element",
                "pattern": r"[0-9]{3}-[0-9]{3}-[0-9]{9}",
            },
        )
        razon_social_comprador: Optional[str] = field(default=None, metadata={
                "name": "razonSocialComprador",
                "type": "Element",
                "min_length": 1,
                "max_length": 300,
                "pattern": r"[^\n]*",
            })
        identificacion_comprador: Optional[str] = field(default=None, metadata={
                "name": "identificacionComprador",
                "type": "Element",
                "min_length": 1,
                "max_length": 20,
                "pattern": r"[^\n]*",
            })
        direccion_comprador: None | str = field(
            default=None,
            metadata={
                "name": "direccionComprador",
                "type": "Element",
                "min_length": 1,
                "max_length": 300,
                "pattern": r"[^\n]*",
            },
        )
        total_sin_impuestos: Decimal = field(
            metadata={
                "name": "totalSinImpuestos",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            }
        )
        total_subsidio: None | Decimal = field(
            default=None,
            metadata={
                "name": "totalSubsidio",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            },
        )
        inco_term_total_sin_impuestos: None | str = field(
            default=None,
            metadata={
                "name": "incoTermTotalSinImpuestos",
                "type": "Element",
                "min_length": 1,
                "max_length": 10,
                "pattern": r"([A-Z])*",
            },
        )
        total_descuento: Optional[Decimal] = field(default=None, metadata={
                "name": "totalDescuento",
                "type": "Element",
                "total_digits": 14,
                "fraction_digits": 2,
            })
        cod_doc_reembolso: None | str = field(
            default=None,
            metadata={
                "name": "codDocReembolso",
                "type": "Element",
                "pattern": r"[0-9]{2,3}",
            },
        )
        total_comprobantes_reembolso: None | Decimal = field(
            default=None,
            metadata={
                "name": "totalComprobantesReembolso",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            },
        )
        total_base_imponible_reembolso: None | Decimal = field(
            default=None,
            metadata={
                "name": "totalBaseImponibleReembolso",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            },
        )
        total_impuesto_reembolso: None | Decimal = field(
            default=None,
            metadata={
                "name": "totalImpuestoReembolso",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            },
        )
        total_con_impuestos: Optional[Factura.InfoFactura.TotalConImpuestos] = field(default=None, metadata={
                "name": "totalConImpuestos",
                "type": "Element",
            })
        compensaciones: None | Compensaciones = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )
        propina: None | Decimal = field(
            default=None,
            metadata={
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            },
        )
        flete_internacional: None | Decimal = field(
            default=None,
            metadata={
                "name": "fleteInternacional",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            },
        )
        seguro_internacional: None | Decimal = field(
            default=None,
            metadata={
                "name": "seguroInternacional",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            },
        )
        gastos_aduaneros: None | Decimal = field(
            default=None,
            metadata={
                "name": "gastosAduaneros",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            },
        )
        gastos_transporte_otros: None | Decimal = field(
            default=None,
            metadata={
                "name": "gastosTransporteOtros",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            },
        )
        importe_total: Decimal = field(
            metadata={
                "name": "importeTotal",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            }
        )
        moneda: None | str = field(
            default=None,
            metadata={
                "type": "Element",
                "min_length": 1,
                "max_length": 15,
                "pattern": r"[^\n]*",
            },
        )
        placa: None | str = field(
            default=None,
            metadata={
                "type": "Element",
                "min_length": 1,
                "max_length": 20,
                "pattern": r"[^\n]*",
            },
        )
        pagos: None | Pagos = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )
        valor_ret_iva: None | Decimal = field(
            default=None,
            metadata={
                "name": "valorRetIva",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            },
        )
        valor_ret_renta: None | Decimal = field(
            default=None,
            metadata={
                "name": "valorRetRenta",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            },
        )

        @dataclass(repr=False, eq=False, kw_only=True)
        class TotalConImpuestos:
            total_impuesto: list[
                Factura.InfoFactura.TotalConImpuestos.TotalImpuesto
            ] = field(
                default_factory=list,
                metadata={
                    "name": "totalImpuesto",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass(repr=False, eq=False, kw_only=True)
            class TotalImpuesto:
                codigo: Optional[str] = field(default=None, metadata={
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 1,
                        "pattern": r"[235]",
                    })
                codigo_porcentaje: Optional[str] = field(default=None, metadata={
                        "name": "codigoPorcentaje",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 4,
                        "pattern": r"[0-9]+",
                    })
                descuento_adicional: None | Decimal = field(
                    default=None,
                    metadata={
                        "name": "descuentoAdicional",
                        "type": "Element",
                        "total_digits": 14,
                        "fraction_digits": 2,
                    },
                )
                base_imponible: Decimal = field(
                    metadata={
                        "name": "baseImponible",
                        "type": "Element",
                        "min_inclusive": Decimal("0"),
                        "total_digits": 14,
                        "fraction_digits": 2,
                    }
                )
                tarifa: None | Decimal = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "min_inclusive": Decimal("0"),
                        "total_digits": 4,
                        "fraction_digits": 2,
                    },
                )
                valor: Decimal = field(
                    metadata={
                        "type": "Element",
                        "min_inclusive": Decimal("0"),
                        "total_digits": 14,
                        "fraction_digits": 2,
                    }
                )
                valor_devolucion_iva: None | Decimal = field(
                    default=None,
                    metadata={
                        "name": "valorDevolucionIva",
                        "type": "Element",
                        "min_inclusive": Decimal("0"),
                        "total_digits": 14,
                        "fraction_digits": 2,
                    },
                )

    @dataclass(repr=False, eq=False, kw_only=True)
    class Detalles:
        detalle: list[Factura.Detalles.Detalle] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "min_occurs": 1,
            },
        )

        @dataclass(repr=False, eq=False, kw_only=True)
        class Detalle:
            codigo_principal: None | str = field(
                default=None,
                metadata={
                    "name": "codigoPrincipal",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 25,
                    "pattern": r"[^\n]*",
                },
            )
            codigo_auxiliar: None | str = field(
                default=None,
                metadata={
                    "name": "codigoAuxiliar",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 25,
                    "pattern": r"[^\n]*",
                },
            )
            descripcion: Optional[str] = field(default=None, metadata={
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 300,
                    "pattern": r"[^\n]*",
                })
            unidad_medida: None | str = field(
                default=None,
                metadata={
                    "name": "unidadMedida",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 50,
                    "pattern": r"[^\n]*",
                },
            )
            cantidad: Decimal = field(
                metadata={
                    "type": "Element",
                    "min_inclusive": Decimal("0"),
                    "total_digits": 18,
                    "fraction_digits": 6,
                }
            )
            precio_unitario: Decimal = field(
                metadata={
                    "name": "precioUnitario",
                    "type": "Element",
                    "min_inclusive": Decimal("0"),
                    "total_digits": 18,
                    "fraction_digits": 6,
                }
            )
            precio_sin_subsidio: None | Decimal = field(
                default=None,
                metadata={
                    "name": "precioSinSubsidio",
                    "type": "Element",
                    "min_inclusive": Decimal("0"),
                    "total_digits": 18,
                    "fraction_digits": 6,
                },
            )
            descuento: Decimal = field(
                metadata={
                    "type": "Element",
                    "min_inclusive": Decimal("0"),
                    "total_digits": 14,
                    "fraction_digits": 2,
                }
            )
            precio_total_sin_impuesto: Decimal = field(
                metadata={
                    "name": "precioTotalSinImpuesto",
                    "type": "Element",
                    "min_inclusive": Decimal("0"),
                    "total_digits": 14,
                    "fraction_digits": 2,
                }
            )
            detalles_adicionales: (
                None | Factura.Detalles.Detalle.DetallesAdicionales
            ) = field(
                default=None,
                metadata={
                    "name": "detallesAdicionales",
                    "type": "Element",
                },
            )
            impuestos: Optional[Factura.Detalles.Detalle.Impuestos] = field(default=None, metadata={
                    "type": "Element",
                })

            @dataclass(repr=False, eq=False, kw_only=True)
            class DetallesAdicionales:
                det_adicional: list[
                    Factura.Detalles.Detalle.DetallesAdicionales.DetAdicional
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "detAdicional",
                        "type": "Element",
                        "min_occurs": 1,
                        "max_occurs": 3,
                    },
                )

                @dataclass(repr=False, eq=False, kw_only=True)
                class DetAdicional:
                    nombre: Optional[str] = field(default=None, metadata={
                            "type": "Attribute",
                            "min_length": 1,
                            "max_length": 300,
                        })
                    valor: Optional[str] = field(default=None, metadata={
                            "type": "Attribute",
                            "min_length": 1,
                            "max_length": 300,
                        })

            @dataclass(repr=False, eq=False, kw_only=True)
            class Impuestos:
                impuesto: list[Impuesto] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )

    @dataclass(repr=False, eq=False, kw_only=True)
    class Retenciones:
        retencion: list[Factura.Retenciones.Retencion] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "min_occurs": 1,
            },
        )

        @dataclass(repr=False, eq=False, kw_only=True)
        class Retencion:
            codigo: Optional[str] = field(default=None, metadata={
                    "type": "Element",
                    "pattern": r"[4]{1}",
                })
            codigo_porcentaje: Optional[str] = field(default=None, metadata={
                    "name": "codigoPorcentaje",
                    "type": "Element",
                    "pattern": r"[0-9]{1,3}",
                })
            tarifa: Decimal = field(
                metadata={
                    "type": "Element",
                    "min_inclusive": Decimal("0"),
                    "total_digits": 5,
                    "fraction_digits": 2,
                }
            )
            valor: Decimal = field(
                metadata={
                    "type": "Element",
                    "min_inclusive": Decimal("0"),
                    "total_digits": 14,
                    "fraction_digits": 2,
                }
            )

    @dataclass(repr=False, eq=False, kw_only=True)
    class InfoSustitutivaGuiaRemision:
        dir_partida: Optional[str] = field(default=None, metadata={
                "name": "dirPartida",
                "type": "Element",
                "min_length": 1,
                "max_length": 300,
                "pattern": r"[^\n]*",
            })
        dir_destinatario: Optional[str] = field(default=None, metadata={
                "name": "dirDestinatario",
                "type": "Element",
                "min_length": 1,
                "max_length": 300,
                "pattern": r"[^\n]*",
            })
        fecha_ini_transporte: str = field(
            metadata={
                "name": "fechaIniTransporte",
                "type": "Element",
                "pattern": r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/20[0-9][0-9]",
            }
        )
        fecha_fin_transporte: str = field(
            metadata={
                "name": "fechaFinTransporte",
                "type": "Element",
                "pattern": r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/20[0-9][0-9]",
            }
        )
        razon_social_transportista: Optional[str] = field(default=None, metadata={
                "name": "razonSocialTransportista",
                "type": "Element",
                "min_length": 1,
                "max_length": 300,
                "pattern": r"[^\n]*",
            })
        tipo_identificacion_transportista: Optional[str] = field(default=None, metadata={
                "name": "tipoIdentificacionTransportista",
                "type": "Element",
                "pattern": r"[0][4-8]",
            })
        ruc_transportista: Optional[str] = field(default=None, metadata={
                "name": "rucTransportista",
                "type": "Element",
                "min_length": 1,
                "max_length": 20,
                "pattern": r"[^\n]*",
            })
        placa: Optional[str] = field(default=None, metadata={
                "type": "Element",
                "min_length": 1,
                "max_length": 20,
                "pattern": r"[^\n]*",
            })
        destinos: Optional[Factura.InfoSustitutivaGuiaRemision.Destinos] = field(default=None, metadata={
                "type": "Element",
            })

        @dataclass(repr=False, eq=False, kw_only=True)
        class Destinos:
            destino: list[Destino] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

    @dataclass(repr=False, eq=False, kw_only=True)
    class OtrosRubrosTerceros:
        rubro: list[Rubro] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "min_occurs": 1,
            },
        )

    @dataclass(repr=False, eq=False, kw_only=True)
    class InfoAdicional:
        campo_adicional: list[Factura.InfoAdicional.CampoAdicional] = field(
            default_factory=list,
            metadata={
                "name": "campoAdicional",
                "type": "Element",
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
                },
            )
            nombre: Optional[str] = field(default=None, metadata={
                    "type": "Attribute",
                    "min_length": 1,
                    "max_length": 300,
                })
