from app.repositories.abc import AbstractAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Type, Optional
from app.models.stickers import Sticker, StickerCanvas
from app.models.requests import Request


class StickerRepository(AbstractAsyncRepository[Sticker]):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    @property
    def model(self) -> Type[Sticker]:
        return Sticker


class StickerCanvasRepository(AbstractAsyncRepository[StickerCanvas]):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    @property
    def model(self) -> Type[StickerCanvas]:
        return StickerCanvas

    async def get_canvas_with_stickers_and_requests(
        self, sticker_canvas_id: int
    ) -> Optional[StickerCanvas]:
        stmt = (
            select(StickerCanvas)
            .options(
                joinedload(StickerCanvas.stickers)
                .joinedload(Sticker.requests)
                .joinedload(Request.customer),  # load customer
                joinedload(StickerCanvas.stickers)
                .joinedload(Sticker.requests)
                .joinedload(Request.area),  # load area
            )
            .where(StickerCanvas.id == sticker_canvas_id)
        )

        result = await self.db.execute(stmt)
        return result.unique().scalar_one_or_none()
