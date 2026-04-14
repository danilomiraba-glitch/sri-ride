import asyncio
import time
from pathlib import Path

from sriRide import SriRide


DIRECTORIO_XML = Path("xml")
MAX_CONCURRENCIA = 3
LOGO_PATH = Path(__file__).parent / "logo.png"


import re
import xml.etree.ElementTree as ET


def detectar_tipo(xml_input):
    try:
        root = ET.fromstring(xml_input)

        comprobante = root.find(".//comprobante")
        if comprobante is None or comprobante.text is None:
            return None

        xml_comprobante = comprobante.text.strip()
        xml_comprobante = re.sub(r"<\?xml.*?\?>", "", xml_comprobante).strip()

        match = re.search(r"<\s*([a-zA-Z0-9_:-]+)", xml_comprobante)
        if not match:
            return None

        tipo = match.group(1).split(":")[-1]

        mapping = {
            "factura": "factura",
            "notaCredito": "notacredito",
            "notaDebito": "notadebito",
            "guiaRemision": "guiaremision",
            "comprobanteRetencion": "retencion"
        }

        return mapping.get(tipo)

    except Exception:
        return None


async def procesar_xml_html(i, xml_path, semaforo, tiempos):
    async with semaforo:

        xml_text = xml_path.read_text(encoding="utf-8")
        tipo = detectar_tipo(xml_text)

        if not tipo:
            print(f"⚠️ {xml_path.name} ignorado")
            return

        ride = SriRide(mode="html")  # 👈 CLAVE: SIN PLAYWRIGHT

        metodo = getattr(ride, tipo)

        inicio = time.perf_counter()

        # 🔥 SOLO PREPROCESO + HTML GENERATION
        resultado = await metodo(xml=xml_text, logo=str(LOGO_PATH))

        fin = time.perf_counter()

        duracion = fin - inicio
        tiempos.append(duracion)

        print(f"⚡ {i} HTML listo en {duracion:.3f}s | partes: {len(resultado)}")



async def main():

    xml_files = list(DIRECTORIO_XML.glob("*.xml"))

    if not xml_files:
        print("❌ No hay XML")
        return

    print(f"✔ {len(xml_files)} XML encontrados")

    semaforo = asyncio.Semaphore(MAX_CONCURRENCIA)
    tiempos = []

    tareas = [
        procesar_xml_html(i, xml, semaforo, tiempos)
        for i, xml in enumerate(xml_files, 1)
    ]

    t_global = time.perf_counter()
    await asyncio.gather(*tareas)
    t_global_fin = time.perf_counter()

    if not tiempos:
        print("❌ No se procesó nada")
        return

    promedio = sum(tiempos) / len(tiempos)

    print("\n📊 RESULTADOS HTML (SIN NAVEGADOR)")
    print(f"⏱ Promedio: {promedio:.4f} s por documento")
    print(f"🚀 Tiempo total batch: {t_global_fin - t_global:.4f} s")
    print(f"⚙️ Concurrencia: {MAX_CONCURRENCIA}")


if __name__ == "__main__":
    asyncio.run(main())