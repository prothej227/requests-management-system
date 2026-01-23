from typing import List
from pydantic import BaseModel
from enum import Enum


class StickerJobStatus(int, Enum):
    IN_PROGRESS = 0
    COMPLETED = 1
    FAILED = -1


class StickerTemplateInfo(BaseModel):
    customer: str
    product: str
    description: str
    labRefNo: str
    quantity: str
    note: str


class StickerRequestForm(BaseModel):
    data: List[StickerTemplateInfo]
    canvasAppianId: int
    pdfTemplateName: str = "base_template"
