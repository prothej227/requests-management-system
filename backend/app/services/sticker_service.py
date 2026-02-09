from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, lightgrey
from reportlab.lib.utils import ImageReader
from io import BytesIO
from typing import List, Dict, Optional, Union
from datetime import datetime
from zoneinfo import ZoneInfo
from app.core.config import get_settings
from PIL import Image
import base64
import uuid
from dataclasses import dataclass
from pathlib import Path

settings = get_settings()


@dataclass
class DocumentInformation:
    document_id: str
    path: str


class StickerGeneratorService:
    def __init__(self):
        # template_path kept for backward compatibility, not used
        self._template_path: str = "settings.pdf_template_path"
        self.output_dir = settings.sticker_storage_dir_resolved

    @property
    def template_path(self) -> str:
        return self._template_path

    @template_path.setter
    def template_path(self, path: str) -> None:
        self._template_path = path

    def draw_wrapped_text(
        self,
        c,
        label,
        value,
        label_x,
        y,
        font_name,
        font_size,
        max_width,
        line_height,
    ):
        """
        First line: LABEL: value
        Wrapped lines: start at label_x (aligned with label)
        Returns updated y
        """

        label_text = f"{label}: "
        label_width = c.stringWidth(label_text, f"{font_name}-Bold", font_size)

        words = value.split()
        line = ""

        # ----- draw label -----
        c.setFont(f"{font_name}-Bold", font_size)
        c.drawString(label_x, y, label_text)

        c.setFont(font_name, font_size)

        for word in words:
            test_line = f"{line} {word}".strip()

            if (
                c.stringWidth(test_line, font_name, font_size)
                <= max_width - label_width
            ):
                line = test_line
            else:
                # draw current line after label
                c.drawString(label_x + label_width, y, line)
                y -= line_height

                # wrapped line starts at label origin
                c.drawString(label_x, y, word)
                y -= line_height

                line = ""

        if line:
            c.drawString(label_x + label_width, y, line)
            y -= line_height

        return y

    async def generate_pdf(self, data: List[Dict[str, Union[str, bytes]]]) -> bytes:
        """
        Generate a single-page A4 sticker PDF (2x3 layout) and return Base64.

        :param data: List of sticker dicts (max 6)
        :return: Base64 encoded PDF
        """
        if len(data) > 10:
            raise ValueError("Maximum of 10 stickers allowed per page")

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
        text_x_offset = left_padding

        # Fixed logo size
        logo_width = 120
        logo_height = 50
        logo_text_padding = 16  # space between logo bottom and text

        # Field order
        field_order = [
            ("customer", "CUSTOMER"),
            ("product", "PRODUCT"),
            ("description", "DESCRIPTION"),
            ("labRefNo", "LAB REF #"),
            ("quantity", "QUANTITY"),
        ]

        # Draw sticker borders
        c.setStrokeColor(lightgrey)
        c.setLineWidth(0.5)
        for col in range(cols + 1):
            x = margin + col * cell_width
            c.line(x, margin, x, margin + usable_height)
        for row in range(rows + 1):
            y = margin + row * cell_height
            c.line(margin, y, margin + usable_width, y)

        for index, sticker in enumerate(data):
            col = index % cols
            row = rows - 1 - (index // cols)

            cell_x = margin + col * cell_width
            cell_y = margin + row * cell_height

            logo_bytes: bytes = sticker.get("logo")  # type: ignore

            if logo_bytes:
                logo_bytes = BytesIO(logo_bytes)  # type: ignore
                with Image.open(logo_bytes) as im:  # type: ignore
                    im = im.convert("RGBA")  # removes alpha/transparency
                    temp_buf = BytesIO()
                    im.save(temp_buf, format="PNG")  # can also use JPEG
                    temp_buf.seek(0)
                    logo_image = ImageReader(temp_buf)
                # logo_image = ImageReader(logo_bytes)
                logo_x = cell_x + text_x_offset
                logo_y = cell_y + cell_height - logo_height - 5  # 5pt margin from top
                c.drawImage(
                    logo_image,
                    logo_x,
                    logo_y,
                    width=logo_width,
                    height=logo_height,
                )
                start_y = logo_y - logo_text_padding
            else:
                start_y = cell_y + cell_height - 5  # no logo, start near top

            text_x = cell_x + text_x_offset
            max_text_width = cell_width - 2 * left_padding  # adjust as needed

            for key, label in field_order:
                c.setFont(f"{font_name}-Bold", font_size)
                c.drawString(text_x, start_y, f"{label}:")

                label_width = c.stringWidth(f"{label}:", f"{font_name}-Bold", font_size)
                c.setFont(font_name, font_size)
                value_x = text_x + label_width + 4
                value_text = str(sticker.get(key, "")).upper()

                if key in ["product", "description"]:
                    start_y = self.draw_wrapped_text(
                        c=c,
                        label=label,
                        value=value_text,
                        label_x=text_x,
                        y=start_y,
                        font_name=font_name,
                        font_size=font_size,
                        max_width=max_text_width,
                        line_height=line_height,
                    )
                else:
                    c.setFont(f"{font_name}-Bold", font_size)
                    c.drawString(text_x, start_y, f"{label}:")
                    c.setFont(font_name, font_size)
                    c.drawString(text_x + label_width + 4, start_y, value_text)
                    start_y -= line_height

        c.showPage()
        c.save()

        return buffer.getvalue()


class StickerStorageService:

    def __init__(self):
        self.storage_path = settings.sticker_storage_dir_resolved

    async def get_document_by_id(self, relative_path: str) -> bytes:
        document_path = self.storage_path / Path(relative_path)
        if not document_path.exists():
            raise FileNotFoundError(
                f"Document with path={str(document_path)} does not exists."
            )
        return Path(document_path).read_bytes()

    async def delete_document_by_id(self, relative_path: str) -> bool:
        document_path = self.storage_path / Path(relative_path)
        if document_path.exists():
            document_path.unlink()
            return True
        return False

    async def save_document_bytes(self, pdf_bytes: bytes) -> DocumentInformation:
        now = datetime.now(ZoneInfo(settings.timezone))

        output_dir = self.storage_path / str(now.year) / f"{now.month:02d}"
        output_dir.mkdir(parents=True, exist_ok=True)

        document_id = str(uuid.uuid4())
        file_path = output_dir / f"{str(document_id)}.pdf"

        # Save bytes to storage
        file_path.write_bytes(pdf_bytes)

        return DocumentInformation(
            document_id=document_id, path=str(file_path.relative_to(self.storage_path))
        )
