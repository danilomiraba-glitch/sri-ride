import asyncio
import time
import base64
from pathlib import Path
from playwright.async_api import async_playwright
from sriRide import SriRide
import re
import xml.etree.ElementTree as ET

DIRECTORIO_XML = Path("xml")
DIR_RESULTADOS = Path("./resultados_test")
LOGO_PATH = Path(__file__).parent / "logo.png"
MAX_CONCURRENCIA = 3
POOL_SIZE = 4

class PoolPageProvider:
    def __init__(self, browser, pool_size=4):
        self.browser = browser
        self.pool_size = pool_size
        self.queue = asyncio.Queue()

    async def init_pool(self):
        for _ in range(self.pool_size):
            context = await self.browser.new_context()
            page = await context.new_page()
            await self.queue.put(page)

    async def acquire_page(self):
        page = await self.queue.get()
        await page.goto("about:blank")  # limpieza fuerte antes de usar
        return page

    async def release_page(self, page):
        self.queue.put_nowait(page)

    async def close(self):
        while not self.queue.empty():
            page = await self.queue.get()
            await page.context.close()


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


def clasificar_rendimiento(promedio):
    if promedio <= 0.20:
        return "EFICIENTE"
    elif promedio <= 0.40:
        return "MEDIO"
    else:
        return "BAJO"



async def procesar_xml(i, xml_path, ride, semaforo, tiempos):
    async with semaforo:
        xml_text = xml_path.read_text(encoding="utf-8")
        tipo = detectar_tipo(xml_text)

        if not tipo:
            print(f"⚠️ {xml_path.name} ignorado")
            return

        metodo = getattr(ride, tipo)

        inicio = time.perf_counter()
        pdf_b64 = await metodo(xml=xml_text, logo=str(LOGO_PATH))
        fin = time.perf_counter()

        duracion = fin - inicio
        tiempos.append(duracion)

        pdf_bytes = base64.b64decode(pdf_b64)
        output_path = DIR_RESULTADOS / f"{xml_path.stem}.pdf"

        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

        print(f"📄 PDF {i} listo en {duracion:.3f} s")



async def warmup_browser(provider, ride, xml_files):
    print("\n🧪 PREPARANDO NAVEGADOR (warm-up real)\n")

    warmup_xml = xml_files[0]
    xml_text = warmup_xml.read_text(encoding="utf-8")

    tipo = detectar_tipo(xml_text)
    metodo = getattr(ride, tipo)

    page = await provider.acquire_page()

    try:
        inicio = time.perf_counter()
        await metodo(xml=xml_text)
        fin = time.perf_counter()

        duracion = fin - inicio

    finally:
        await page.goto("about:blank")
        await provider.release_page(page)

    print(f"⚡ Warm-up completado en {duracion:.3f}s")
    print("🚀 Navegador listo\n")


async def main():
    print("\n📂 Listando XML en directorio...")
    xml_files = list(DIRECTORIO_XML.glob("*.xml"))

    if not xml_files:
        print("❌ No hay XML")
        return

    print(f"✔ {len(xml_files)} XML encontrados")

    print("\n🚀 Iniciando navegador...")
    t0 = time.perf_counter()

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch()

    provider = PoolPageProvider(browser, POOL_SIZE)
    await provider.init_pool()

    t1 = time.perf_counter()
    print(f"✅ Navegador listo en {(t1 - t0):.2f} segundos")

    ride = SriRide(mode="pdf", page_provider=provider)

    await warmup_browser(provider, ride, xml_files)

    DIR_RESULTADOS.mkdir(exist_ok=True)

    semaforo = asyncio.Semaphore(MAX_CONCURRENCIA)
    tiempos = []

    tareas = [
        procesar_xml(i, xml, ride, semaforo, tiempos)
        for i, xml in enumerate(xml_files, 1)
    ]

    await asyncio.gather(*tareas)

    if not tiempos:
        print("❌ No se generaron PDFs")
        return

    promedio = sum(tiempos) / len(tiempos)
    nivel = clasificar_rendimiento(promedio)

    print("\n📊 Test terminado")
    print(f"⏱ Promedio: {promedio:.3f} s")
    print(f"🚦 Rendimiento: {nivel}")

    print("\n🧹 Limpiando memoria y cerrando navegador...")
    await provider.close()
    await browser.close()
    await playwright.stop()

    print("✅ Finalizado\n")

if __name__ == "__main__":
    asyncio.run(main())