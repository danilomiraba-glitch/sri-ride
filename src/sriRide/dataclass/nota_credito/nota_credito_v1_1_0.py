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
class Detalle:
    class Meta:
        name = "detalle"

    motivo_modificacion: Optional[str] = field(default=None, metadata={
            "name": "motivoModificacion",
            "type": "Element",
        })


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
    tarifa: None | Decimal = field(
        default=None,
        metadata={
            "type": "Element",
            "min_inclusive": Decimal("0"),
            "total_digits": 4,
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


class NotaCreditoId(Enum):
    COMPROBANTE = "comprobante"


class ObligadoContabilidad(Enum):
    SI = "SI"
    NO = "NO"


@dataclass(repr=False, eq=False, kw_only=True)
class TotalConImpuestos:
    class Meta:
        name = "totalConImpuestos"

    total_impuesto: list[TotalConImpuestos.TotalImpuesto] = field(
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
class NotaCredito:
    class Meta:
        name = "notaCredito"

    info_tributaria: Optional[InfoTributaria] = field(default=None, metadata={
            "name": "infoTributaria",
            "type": "Element",
        })
    info_nota_credito: Optional[NotaCredito.InfoNotaCredito] = field(default=None, metadata={
            "name": "infoNotaCredito",
            "type": "Element",
        })
    detalles: Optional[NotaCredito.Detalles] = field(default=None, metadata={
            "type": "Element",
        })
    maquina_fiscal: None | MaquinaFiscal = field(
        default=None,
        metadata={
            "name": "maquinaFiscal",
            "type": "Element",
        },
    )
    info_adicional: None | NotaCredito.InfoAdicional = field(
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
    id: Optional[NotaCreditoId] = field(default=None, metadata={
            "type": "Attribute",
        })
    version: Optional[str] = field(default=None, metadata={
            "type": "Attribute",
        })

    @dataclass(repr=False, eq=False, kw_only=True)
    class InfoNotaCredito:
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
        tipo_identificacion_comprador: Optional[str] = field(default=None, metadata={
                "name": "tipoIdentificacionComprador",
                "type": "Element",
                "min_length": 1,
                "max_length": 13,
                "pattern": r"[0][4-8]",
            })
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
        rise: None | str = field(
            default=None,
            metadata={
                "type": "Element",
                "min_length": 1,
                "max_length": 40,
            },
        )
        cod_doc_modificado: Optional[str] = field(default=None, metadata={
                "name": "codDocModificado",
                "type": "Element",
                "pattern": r"[0-9]{2}",
            })
        num_doc_modificado: Optional[str] = field(default=None, metadata={
                "name": "numDocModificado",
                "type": "Element",
                "pattern": r"[0-9]{3}-[0-9]{3}-[0-9]{9}",
            })
        fecha_emision_doc_sustento: str = field(
            metadata={
                "name": "fechaEmisionDocSustento",
                "type": "Element",
                "pattern": r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/20[0-9][0-9]",
            }
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
        compensaciones: None | Compensaciones = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )
        valor_modificacion: Decimal = field(
            metadata={
                "name": "valorModificacion",
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
        total_con_impuestos: Optional[TotalConImpuestos] = field(default=None, metadata={
                "name": "totalConImpuestos",
                "type": "Element",
            })
        motivo: Optional[str] = field(default=None, metadata={
                "type": "Element",
                "min_length": 1,
                "max_length": 300,
                "pattern": r"[^\n]*",
            })

    @dataclass(repr=False, eq=False, kw_only=True)
    class Detalles:
        detalle: list[NotaCredito.Detalles.Detalle] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "min_occurs": 1,
            },
        )

        @dataclass(repr=False, eq=False, kw_only=True)
        class Detalle:
            codigo_interno: None | str = field(
                default=None,
                metadata={
                    "name": "codigoInterno",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 25,
                    "pattern": r"[^\n]*",
                },
            )
            codigo_adicional: None | str = field(
                default=None,
                metadata={
                    "name": "codigoAdicional",
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
            descuento: None | Decimal = field(
                default=None,
                metadata={
                    "type": "Element",
                    "min_inclusive": Decimal("0"),
                    "total_digits": 14,
                    "fraction_digits": 2,
                },
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
                None | NotaCredito.Detalles.Detalle.DetallesAdicionales
            ) = field(
                default=None,
                metadata={
                    "name": "detallesAdicionales",
                    "type": "Element",
                },
            )
            impuestos: Optional[NotaCredito.Detalles.Detalle.Impuestos] = field(default=None, metadata={
                    "type": "Element",
                })

            @dataclass(repr=False, eq=False, kw_only=True)
            class DetallesAdicionales:
                det_adicional: list[
                    NotaCredito.Detalles.Detalle.DetallesAdicionales.DetAdicional
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
                    },
                )

    @dataclass(repr=False, eq=False, kw_only=True)
    class InfoAdicional:
        campo_adicional: list[NotaCredito.InfoAdicional.CampoAdicional] = (
            field(
                default_factory=list,
                metadata={
                    "name": "campoAdicional",
                    "type": "Element",
                    "min_occurs": 1,
                    "max_occurs": 15,
                },
            )
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
