from __future__ import annotations

import asyncio
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter


A4_HEIGHT_PX = 1122  # Aproximación estable en Chromium
PX_TO_MM = 0.264583  # Más preciso que 0.2646


async def render_layout_to_pdf(
    page,
    *,
    output_path: Path,
    format: str = "A4",
    margin_top: str = "0mm",
    margin_right: str = "0mm",
    margin_bottom: str = "0mm",
    margin_left: str = "0mm",
) -> None:
    pdf_bytes = await render_layout_to_pdf_bytes(
        page,
        format=format,
        margin_top=margin_top,
        margin_right=margin_right,
        margin_bottom=margin_bottom,
        margin_left=margin_left,
    )

    await asyncio.to_thread(merge_pdf_bytes, [pdf_bytes], output_path)


async def render_layout_to_pdf_bytes(
    page,
    *,
    format: str = "A4",
    margin_top: str = "0mm",
    margin_right: str = "0mm",
    margin_bottom: str = "0mm",
    margin_left: str = "0mm",
) -> bytes:
    await page.emulate_media(media="print")

    await page.evaluate(
        """async () => {
            if (document.fonts && document.fonts.ready) {
                await document.fonts.ready;
            }
        }"""
    )

    content_height = await page.evaluate(
        """() => {
            const body = document.body;
            const html = document.documentElement;

            return Math.max(
                body.scrollHeight,
                body.offsetHeight,
                html.clientHeight,
                html.scrollHeight,
                html.offsetHeight
            );
        }"""
    )

    if content_height <= A4_HEIGHT_PX:
        height_mm = content_height * PX_TO_MM

        return await page.pdf(
            width="210mm",
            height=f"{height_mm:.2f}mm",
            print_background=True,
            display_header_footer=False,
            scale=1,
            margin={
                "top": margin_top,
                "right": margin_right,
                "bottom": margin_bottom,
                "left": margin_left,
            },
        )

    return await page.pdf(
        format=format,
        print_background=True,
        display_header_footer=False,
        scale=1,
        margin={
            "top": margin_top,
            "right": margin_right,
            "bottom": margin_bottom,
            "left": margin_left,
        },
    )


def merge_pdf_bytes(pdf_parts: list[bytes], output_path: Path) -> None:
    writer = PdfWriter()

    for pdf_part in pdf_parts:
        reader = PdfReader(BytesIO(pdf_part))
        for page in reader.pages:
            writer.add_page(page)

    with output_path.open("wb") as f:
        writer.write(f)