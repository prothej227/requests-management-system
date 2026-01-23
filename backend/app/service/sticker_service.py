from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, lightgrey
from io import BytesIO
from typing import List, Dict
import base64

from app.core.config import get_settings

settings = get_settings()


class CreateStickerService:
    def __init__(self):
        # template_path kept for backward compatibility, not used
        self._template_path: str = "settings.pdf_template_path"

    @property
    def template_path(self) -> str:
        return self._template_path

    @template_path.setter
    def template_path(self, path: str) -> None:
        self._template_path = path

    async def generate_pdf(self, data: List[Dict[str, str]]) -> bytes:
        """
        Generate a single-page A4 sticker PDF (2x3 layout) and return Base64.

        :param data: List of sticker dicts (max 6)
        :return: Base64 encoded PDF
        """

        if len(data) > 10:
            raise ValueError("Maximum of 6 stickers allowed per page")

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        page_width, page_height = A4

        # Layout
        margin = 20
        cols, rows = 2, 5
        usable_width = page_width - 2 * margin
        usable_height = page_height - 2 * margin

        cell_width = usable_width / cols
        cell_height = usable_height / rows

        # Text styling
        font_name = "Helvetica"
        font_size = 10
        line_height = 14
        left_padding = 12

        c.setFont(font_name, font_size)
        c.setFillColor(black)

        field_order = [
            ("customer", "CUSTOMER"),
            ("product", "PRODUCT"),
            ("description", "DESCRIPTION"),
            ("labRefNo", "LAB REF #"),
            ("quantity", "QUANTITY"),
            ("note", "NOTE"),
        ]

        # ----------------------------
        # 1️⃣ Draw sticker borders (RESTORED)
        # ----------------------------
        c.setStrokeColor(lightgrey)
        c.setLineWidth(0.5)

        # Vertical lines
        for col in range(cols + 1):
            x = margin + col * cell_width
            c.line(x, margin, x, margin + usable_height)

        # Horizontal lines
        for row in range(rows + 1):
            y = margin + row * cell_height
            c.line(margin, y, margin + usable_width, y)

        for index, sticker in enumerate(data):
            col = index % cols
            row = rows - 1 - (index // cols)

            cell_x = margin + col * cell_width
            cell_y = margin + row * cell_height

            # Vertical centering
            total_lines = len(field_order)
            text_block_height = total_lines * line_height
            start_y = cell_y + (cell_height + text_block_height) / 2 - line_height

            text_x = cell_x + left_padding

            for i, (key, label) in enumerate(field_order):
                value = sticker.get(key, "")

                y = start_y - (i * line_height)

                # Bold label
                c.setFont("Helvetica-Bold", 10)
                c.drawString(text_x, y, f"{label}:")

                # Normal value
                label_width = c.stringWidth(f"{label}:", "Helvetica-Bold", 10)
                c.setFont("Helvetica", 10)
                c.drawString(text_x + label_width + 4, y, value)

        # Single-page guarantee
        c.showPage()
        c.save()

        return buffer.getvalue()
