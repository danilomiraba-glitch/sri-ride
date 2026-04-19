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


class NotaDebitoId(Enum):
    COMPROBANTE = "comprobante"


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
class NotaDebito:
    class Meta:
        name = "notaDebito"

    info_tributaria: Optional[InfoTributaria] = field(default=None, metadata={
            "name": "infoTributaria",
            "type": "Element",
        })
    info_nota_debito: Optional[NotaDebito.InfoNotaDebito] = field(default=None, metadata={
            "name": "infoNotaDebito",
            "type": "Element",
        })
    motivos: Optional[NotaDebito.Motivos] = field(default=None, metadata={
            "type": "Element",
        })
    maquina_fiscal: None | MaquinaFiscal = field(
        default=None,
        metadata={
            "name": "maquinaFiscal",
            "type": "Element",
        },
    )
    info_adicional: None | NotaDebito.InfoAdicional = field(
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
    id: None | NotaDebitoId = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    version: Optional[str] = field(default=None, metadata={
            "type": "Attribute",
        })

    @dataclass(repr=False, eq=False, kw_only=True)
    class InfoNotaDebito:
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
        total_sin_impuestos: Optional[Decimal] = field(default=None, metadata={
                "name": "totalSinImpuestos",
                "type": "Element",
                "total_digits": 14,
                "fraction_digits": 2,
            })
        impuestos: Optional[NotaDebito.InfoNotaDebito.Impuestos] = field(default=None, metadata={
                "type": "Element",
            })
        compensaciones: None | NotaDebito.InfoNotaDebito.Compensaciones = (
            field(
                default=None,
                metadata={
                    "type": "Element",
                },
            )
        )
        valor_total: Decimal = field(
            metadata={
                "name": "valorTotal",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "total_digits": 14,
                "fraction_digits": 2,
            }
        )
        pagos: list[NotaDebito.InfoNotaDebito.Pagos] = field(
            default_factory=list,
            metadata={
                "type": "Element",
            },
        )

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
        class Compensaciones:
            compensacion: list[Compensacion] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

        @dataclass(repr=False, eq=False, kw_only=True)
        class Pagos:
            pago: list[Pago] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

    @dataclass(repr=False, eq=False, kw_only=True)
    class Motivos:
        motivo: list[NotaDebito.Motivos.Motivo] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "min_occurs": 1,
            },
        )

        @dataclass(repr=False, eq=False, kw_only=True)
        class Motivo:
            razon: Optional[str] = field(default=None, metadata={
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 300,
                    "pattern": r"[^\n]*",
                })
            valor: Decimal = field(
                metadata={
                    "type": "Element",
                    "min_inclusive": Decimal("0"),
                    "total_digits": 14,
                    "fraction_digits": 2,
                }
            )

    @dataclass(repr=False, eq=False, kw_only=True)
    class InfoAdicional:
        campo_adicional: list[NotaDebito.InfoAdicional.CampoAdicional] = field(
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
