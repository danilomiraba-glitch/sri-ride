from __future__ import annotations

from typing import Optional
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from ..signature.xmldsig_core_schema import Signature


@dataclass(repr=False, eq=False, kw_only=True)
class Detalle:
    class Meta:
        name = "detalle"

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
    detalles_adicionales: None | Detalle.DetallesAdicionales = field(
        default=None,
        metadata={
            "name": "detallesAdicionales",
            "type": "Element",
        },
    )

    @dataclass(repr=False, eq=False, kw_only=True)
    class DetallesAdicionales:
        det_adicional: list[Detalle.DetallesAdicionales.DetAdicional] = field(
            default_factory=list,
            metadata={
                "name": "detAdicional",
                "type": "Element",
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


class GuiaRemisionId(Enum):
    COMPROBANTE = "comprobante"


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
class Destinatario:
    class Meta:
        name = "destinatario"

    identificacion_destinatario: Optional[str] = field(default=None, metadata={
            "name": "identificacionDestinatario",
            "type": "Element",
            "min_length": 1,
            "max_length": 20,
            "pattern": r"[^\n]*",
        })
    razon_social_destinatario: Optional[str] = field(default=None, metadata={
            "name": "razonSocialDestinatario",
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
            "max_length": 20,
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
    cod_doc_sustento: None | str = field(
        default=None,
        metadata={
            "name": "codDocSustento",
            "type": "Element",
            "pattern": r"[0-9]{2}",
        },
    )
    num_doc_sustento: None | str = field(
        default=None,
        metadata={
            "name": "numDocSustento",
            "type": "Element",
            "pattern": r"[0-9]{3}-[0-9]{3}-[0-9]{9}",
        },
    )
    num_aut_doc_sustento: None | str = field(
        default=None,
        metadata={
            "name": "numAutDocSustento",
            "type": "Element",
            "pattern": r"[0-9]{10,49}",
        },
    )
    fecha_emision_doc_sustento: None | str = field(
        default=None,
        metadata={
            "name": "fechaEmisionDocSustento",
            "type": "Element",
            "pattern": r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/20[0-9][0-9]",
        },
    )
    detalles: Optional[Destinatario.Detalles] = field(default=None, metadata={
            "type": "Element",
        })

    @dataclass(repr=False, eq=False, kw_only=True)
    class Detalles:
        detalle: list[Detalle] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "min_occurs": 1,
            },
        )


@dataclass(repr=False, eq=False, kw_only=True)
class GuiaRemision:
    class Meta:
        name = "guiaRemision"

    info_tributaria: Optional[InfoTributaria] = field(default=None, metadata={
            "name": "infoTributaria",
            "type": "Element",
        })
    info_guia_remision: Optional[GuiaRemision.InfoGuiaRemision] = field(default=None, metadata={
            "name": "infoGuiaRemision",
            "type": "Element",
        })
    destinatarios: Optional[GuiaRemision.Destinatarios] = field(default=None, metadata={
            "type": "Element",
        })
    maquina_fiscal: None | MaquinaFiscal = field(
        default=None,
        metadata={
            "name": "maquinaFiscal",
            "type": "Element",
        },
    )
    info_adicional: None | GuiaRemision.InfoAdicional = field(
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
    id: Optional[GuiaRemisionId] = field(default=None, metadata={
            "type": "Attribute",
        })
    version: Optional[str] = field(default=None, metadata={
            "type": "Attribute",
        })

    @dataclass(repr=False, eq=False, kw_only=True)
    class InfoGuiaRemision:
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
        dir_partida: Optional[str] = field(default=None, metadata={
                "name": "dirPartida",
                "type": "Element",
                "min_length": 1,
                "max_length": 300,
                "pattern": r"[^\n]*",
            })
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
        rise: None | str = field(
            default=None,
            metadata={
                "type": "Element",
                "min_length": 1,
                "max_length": 40,
            },
        )
        obligado_contabilidad: None | ObligadoContabilidad = field(
            default=None,
            metadata={
                "name": "obligadoContabilidad",
                "type": "Element",
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
        placa: Optional[str] = field(default=None, metadata={
                "type": "Element",
                "min_length": 1,
                "max_length": 20,
                "pattern": r"[^\n]*",
            })

    @dataclass(repr=False, eq=False, kw_only=True)
    class Destinatarios:
        destinatario: list[Destinatario] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "min_occurs": 1,
            },
        )

    @dataclass(repr=False, eq=False, kw_only=True)
    class InfoAdicional:
        campo_adicional: list[GuiaRemision.InfoAdicional.CampoAdicional] = (
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
