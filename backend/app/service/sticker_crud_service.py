from app.service.crud import CrudService
from app.schemas import sticker
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.stickers import Sticker, StickerCanvas
from app.repositories.sticker import StickerRepository, StickerCanvasRepository
from typing import Optional


class StickerCrudService(
    CrudService[Sticker, sticker.StickerCreate, sticker.StickerUpdate]
):
    def __init__(self, db: AsyncSession):
        super().__init__(Sticker, StickerRepository, db)


class StickerCanvasCrudService(
    CrudService[StickerCanvas, sticker.StickerCanvasCreate, sticker.StickerCanvasUpdate]
):
    def __init__(self, db: AsyncSession):
        super().__init__(StickerCanvas, StickerCanvasRepository, db)
        self.repo: StickerCanvasRepository

    async def get_canvas_with_stickers_and_requests(
        self, sticker_canvas_id: int
    ) -> Optional[StickerCanvas]:
        return await self.repo.get_canvas_with_stickers_and_requests(sticker_canvas_id)
