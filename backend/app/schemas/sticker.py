from app.core.types import *
from pydantic import BaseModel, computed_field
from datetime import date, datetime
from enum import Enum


class LStickerJobStatus(int, Enum):
    IN_PROGRESS = 0
    COMPLETED = 1
    FAILED = -1


class LStickerTemplateInfo(BaseModel):
    customer: str
    product: str
    description: str
    labRefNo: str
    quantity: str
    note: str


class LStickerRequestForm(BaseModel):
    data: List[LStickerTemplateInfo]
    canvasAppianId: int
    pdfTemplateName: str = "base_template"


class StickerBase(BaseModel):
    request_id: int


class StickerCreate(StickerBase):
    sticker_canvas_id: Optional[int] = None


class StickerUpdate(StickerBase):
    canvas_id: Optional[int]
    request_id: Optional[int]


class StickerView(BaseModel):
    id: int
    request_id: int
    sticker_canvas_id: int
    created_on: datetime
    created_by: Optional[str]

    class Config:
        from_attributes = True


class StickerCanvasBase(BaseModel):
    document_id: Optional[str] = None
    relative_file_path: Optional[str] = None
    created_by: Optional[str] = None


class StickerCanvasCreate(StickerCanvasBase):
    stickers: List[StickerCreate]


class StickerCanvasUpdate(StickerCanvasBase):
    stickers: Optional[List[StickerUpdate]] = []
    document_id: Optional[str] = None
    relative_file_path: Optional[str] = None


class StickerCanvasView(StickerCanvasBase):
    id: int
    stickers: Union[List[StickerView], List[Dict]]
    created_on: datetime

    @computed_field
    @property
    def stickers_count(self) -> int:
        return len(self.stickers)

    class Config:
        from_attributes = True


class StickerCanvasResponseWithCount(BaseModel):
    total_count: int
    records: List[StickerCanvasView]
