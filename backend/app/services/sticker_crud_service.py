from app.services.crud import CrudService
from app.services.sticker_service import StickerStorageService
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
        self._storage_service = StickerStorageService()

    async def get_canvas_with_stickers_and_requests(
        self, sticker_canvas_id: int
    ) -> Optional[StickerCanvas]:
        return await self.repo.get_canvas_with_stickers_and_requests(sticker_canvas_id)

    async def delete_by_id(self, id: int, relative_path: Optional[str]) -> bool:
        if not relative_path:
            print("No relative path")
            return await super().delete_by_id(id)
        # Delete document first from storage if document is existing from relative_path
        storage_deletion_ok = await self._storage_service.delete_document_by_id(
            relative_path=relative_path
        )
        if storage_deletion_ok:
            return await super().delete_by_id(id)
        else:
            return False
