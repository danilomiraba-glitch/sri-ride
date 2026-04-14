from __future__ import annotations

import asyncio
import inspect
from pathlib import Path
from typing import Any, Awaitable, Callable, Sequence

from playwright.async_api import async_playwright

from .pdf_layout import merge_pdf_bytes, render_layout_to_pdf_bytes  # type: ignore


async def render_pdf_desde_html(
    html: str | None = None,
    *,
    output_pdf: str | Path,
    base_dir: str | Path,
    format: str = "A4",
    margin_top: str = "0mm",
    margin_right: str = "0mm",
    margin_bottom: str = "0mm",
    margin_left: str = "0mm",
    page=None,
    html_parts: Sequence[Any] | None = None,
    page_provider=None,
) -> Path:
    output_path = Path(output_pdf).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    base_dir_path = Path(base_dir).resolve()

    partes = _normalizar_partes_html(html=html, html_parts=html_parts)
    for parte in partes:
        parte["html"] = _inyectar_base_href(str(parte["html"]), base_dir_path)

    if page is not None and page_provider is not None:
        raise ValueError("Debes enviar `page` o `page_provider`, no ambos.")

    if page is not None:
        resultados = await _render_partes_en_contexto(
            partes=partes,
            create_page=page.context.new_page,
            primary_page=page,
            format=format,
            margin_top=margin_top,
            margin_right=margin_right,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
        )
    elif page_provider is not None:
        resultados = await _render_partes_con_provider(
            partes=partes,
            page_provider=page_provider,
            format=format,
            margin_top=margin_top,
            margin_right=margin_right,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
        )
    else:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            resultados = await _render_partes_en_contexto(
                partes=partes,
                create_page=context.new_page,
                primary_page=None,
                format=format,
                margin_top=margin_top,
                margin_right=margin_right,
                margin_bottom=margin_bottom,
                margin_left=margin_left,
            )
            await browser.close()

    pdf_partes_ordenadas = [item["pdf_bytes"] for item in sorted(resultados, key=lambda x: x["orden"])]
    await asyncio.to_thread(merge_pdf_bytes, pdf_partes_ordenadas, output_path)

    return output_path


async def _render_partes_en_contexto(
    *,
    partes: list[dict[str, Any]],
    create_page: Callable[[], Awaitable[Any]],
    primary_page: Any | None,
    format: str,
    margin_top: str,
    margin_right: str,
    margin_bottom: str,
    margin_left: str,
) -> list[dict[str, Any]]:
    sem = asyncio.Semaphore(1)

    async def _render_una_parte(parte: dict[str, Any], *, page_to_use: Any, close_after: bool) -> dict[str, Any]:
        try:
            async with sem:
                pdf_bytes = await _render_html_en_page(
                    page_to_use=page_to_use,
                    html_con_base=str(parte["html"]),
                    format=format,
                    margin_top=margin_top,
                    margin_right=margin_right,
                    margin_bottom=margin_bottom,
                    margin_left=margin_left,
                )
            return {"orden": int(parte["orden"]), "pdf_bytes": pdf_bytes}
        finally:
            if close_after:
                await page_to_use.close()

    tareas = []
    for i, parte in enumerate(partes):
        usar_primary = i == 0 and primary_page is not None
        if usar_primary:
            page_to_use = primary_page
            close_after = False
        else:
            page_to_use = await create_page()
            close_after = True
        tareas.append(_render_una_parte(parte, page_to_use=page_to_use, close_after=close_after))

    return await asyncio.gather(*tareas)


async def _render_partes_con_provider(
    *,
    partes: list[dict[str, Any]],
    page_provider: Any,
    format: str,
    margin_top: str,
    margin_right: str,
    margin_bottom: str,
    margin_left: str,
) -> list[dict[str, Any]]:
    acquire = getattr(page_provider, "acquire_page", None)
    if acquire is None:
        raise TypeError("`page_provider` debe implementar `acquire_page()`.")

    release = getattr(page_provider, "release_page", None)
    sem = asyncio.Semaphore(3)

    async def _render_una_parte(parte: dict[str, Any]) -> dict[str, Any]:
        page_to_use = await _maybe_await(acquire())
        if page_to_use is None:
            raise RuntimeError("`page_provider.acquire_page()` devolvio None.")
        try:
            async with sem:
                pdf_bytes = await _render_html_en_page(
                    page_to_use=page_to_use,
                    html_con_base=str(parte["html"]),
                    format=format,
                    margin_top=margin_top,
                    margin_right=margin_right,
                    margin_bottom=margin_bottom,
                    margin_left=margin_left,
                )
            return {"orden": int(parte["orden"]), "pdf_bytes": pdf_bytes}
        finally:
            if release is not None:
                await _maybe_await(release(page_to_use))
            else:
                await page_to_use.close()

    tareas = [_render_una_parte(parte) for parte in partes]
    return await asyncio.gather(*tareas)


async def _render_html_en_page(
    *,
    page_to_use: Any,
    html_con_base: str,
    format: str,
    margin_top: str,
    margin_right: str,
    margin_bottom: str,
    margin_left: str,
) -> bytes:
    await page_to_use.set_content(html_con_base, wait_until="domcontentloaded")
    await page_to_use.emulate_media(media="print")
    return await render_layout_to_pdf_bytes(
        page_to_use,
        format=format,
        margin_top=margin_top,
        margin_right=margin_right,
        margin_bottom=margin_bottom,
        margin_left=margin_left,
    )


async def _maybe_await(value):
    if inspect.isawaitable(value):
        return await value
    return value


def _normalizar_partes_html(
    *,
    html: str | None,
    html_parts: Sequence[Any] | None,
) -> list[dict[str, Any]]:
    if not html_parts:
        if html is None:
            raise ValueError("Debes enviar `html` o `html_parts` para renderizar PDF.")
        return [{"orden": 0, "html": html}]

    partes: list[dict[str, Any]] = []
    for i, raw in enumerate(html_parts):
        if isinstance(raw, dict):
            html_val = raw.get("html")
            orden_val = raw.get("orden", raw.get("order", i))
        else:
            html_val = getattr(raw, "html", None)
            orden_val = getattr(raw, "orden", getattr(raw, "order", i))

        if not isinstance(html_val, str) or not html_val.strip():
            continue

        try:
            orden = int(orden_val)
        except (TypeError, ValueError):
            orden = i

        partes.append({"orden": orden, "html": html_val})

    if not partes:
        raise ValueError("`html_parts` no contiene contenido renderizable.")
    return sorted(partes, key=lambda x: int(x["orden"]))


def _inyectar_base_href(html: str, base_dir: Path) -> str:
    base_uri = base_dir.as_uri()
    if not base_uri.endswith("/"):
        base_uri = f"{base_uri}/"
    tag = f'<base href="{base_uri}">'

    lower = html.lower()
    head_pos = lower.find("<head>")
    if head_pos == -1:
        return tag + html
    insert_pos = head_pos + len("<head>")
    return html[:insert_pos] + "\n  " + tag + html[insert_pos:]
