import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.repositories.user import UserRepository
from app.schemas.users import UserPublic
from app.schemas.sticker import StickerRequestForm
from app.schemas.generic import APIResponse
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.user_service import get_current_user
from app.service.sticker_service import CreateStickerService

router = APIRouter(prefix="/sticker-service", tags=["stickers"])


@router.post(
    "/create",
    status_code=status.HTTP_200_OK,
)
async def create_sticker(
    form: StickerRequestForm, _user: UserPublic = Depends(get_current_user)
) -> Response:

    sticker_pdf_bytes: bytes = await CreateStickerService().generate_pdf(
        data=[sticker.model_dump() for sticker in form.data]
    )
    canvas_appian_id = form.canvasAppianId
    return Response(
        content=sticker_pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename=sticker-canvas-{canvas_appian_id}.pdf"
        },
    )
