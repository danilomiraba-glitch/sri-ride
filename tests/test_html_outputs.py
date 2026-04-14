from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from src.sriRide import SriRide


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "xml"


def _assert_partes_html(partes: object) -> list[dict]:
    assert isinstance(partes, list)
    assert len(partes) >= 1

    for parte in partes:
        assert isinstance(parte, dict)
        assert isinstance(parte.get("clave"), str)
        assert isinstance(parte.get("template_name"), str)
        assert isinstance(parte.get("orden"), int)
        html = parte.get("html")
        assert isinstance(html, str)
        assert "<html" in html.lower()

    return partes


@pytest.mark.parametrize("xml_path", sorted((FIXTURES_DIR / "factura").glob("*.xml")))
def test_factura_html_partes(xml_path: Path) -> None:
    ride = SriRide(mode="html")
    partes = asyncio.run(ride.factura(xml=xml_path))
    partes = _assert_partes_html(partes)

    if "anexo" in xml_path.name.lower():
        assert len(partes) >= 2


@pytest.mark.parametrize("xml_path", sorted((FIXTURES_DIR / "guia_remision").glob("*.xml")))
def test_guia_remision_html_partes(xml_path: Path) -> None:
    ride = SriRide(mode="html")
    partes = asyncio.run(ride.guiaremision(xml=xml_path))
    _assert_partes_html(partes)


@pytest.mark.parametrize("xml_path", sorted((FIXTURES_DIR / "nota_credito").glob("*.xml")))
def test_nota_credito_html_partes(xml_path: Path) -> None:
    ride = SriRide(mode="html")
    partes = asyncio.run(ride.notacredito(xml=xml_path))
    _assert_partes_html(partes)


@pytest.mark.parametrize("xml_path", sorted((FIXTURES_DIR / "nota_debito").glob("*.xml")))
def test_nota_debito_html_partes(xml_path: Path) -> None:
    ride = SriRide(mode="html")
    partes = asyncio.run(ride.notadebito(xml=xml_path))
    _assert_partes_html(partes)


@pytest.mark.parametrize("xml_path", sorted((FIXTURES_DIR / "retencion").glob("*.xml")))
def test_retencion_html_partes(xml_path: Path) -> None:
    ride = SriRide(mode="html")
    partes = asyncio.run(ride.retencion(xml=xml_path))
    _assert_partes_html(partes)
