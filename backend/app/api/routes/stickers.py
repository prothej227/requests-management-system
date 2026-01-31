import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.repositories.user import UserRepository
from app.schemas.users import UserPublic
from app.schemas import sticker as sticker_schemas
from app.schemas.generic import APIResponse
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.user_service import get_current_user
from app.service.sticker_service import StickerGeneratorService, StickerStorageService
from app.service.sticker_crud_service import (
    StickerCanvasCrudService,
    StickerCrudService,
)
from fastapi.responses import FileResponse

router = APIRouter(prefix="/sticker-service", tags=["stickers"])


@router.post(
    "/legacy-create",
    status_code=status.HTTP_200_OK,
)
async def legacy_create_sticker_canvas(
    form: sticker_schemas.LStickerRequestForm,
    _user: UserPublic = Depends(get_current_user),
) -> Response:
    """Legacy endpoint for creating sticker canvas manually via Appian WebAPI."""
    sticker_pdf_bytes: bytes = await StickerGeneratorService().generate_pdf(
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


@router.post("/canvas/create", status_code=status.HTTP_200_OK)
async def create_sticker_canvas(
    form: sticker_schemas.StickerCanvasCreate,
    db: AsyncSession = Depends(get_db),
) -> APIResponse:

    sticker_service = StickerCrudService(db)
    sticker_canvas_service = StickerCanvasCrudService(db)

    if len(form.stickers) > 10:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Stickers cannot exceed 10.",
        )
    # Create everything in ONE transaction
    async with db.begin():
        # --- create canvas ---
        canvas_form = form.model_copy()
        canvas_form.stickers = []

        new_canvas = await sticker_canvas_service.create_no_commit(canvas_form)

        # Flush so PK is assigned
        await db.flush()

        # --- create stickers ---
        for sticker in form.stickers:
            sticker_with_canvas = sticker_schemas.StickerCreate(
                request_id=sticker.request_id,
                sticker_canvas_id=new_canvas.id,  # type: ignore
            )
            await sticker_service.create_no_commit(sticker_with_canvas)

    # Refresh after commit
    await db.refresh(new_canvas)

    return APIResponse(
        response={
            "canvas_id": new_canvas.id,
            "stickers_created": len(form.stickers),
        },
        message=f"New sticker canvas created with ID {new_canvas.id}",
    )


@router.get("/canvas/list", status_code=status.HTTP_200_OK)
async def list_sticker_canvases(
    start_index: int = 0,
    batch_size: int = 10,
    db: AsyncSession = Depends(get_db),
) -> sticker_schemas.StickerCanvasResponseWithCount:
    """List sticker canvases with pagination."""
    sticker_canvas_service = StickerCanvasCrudService(db)
    record_list = []
    records = await sticker_canvas_service.get_all_denorm_with_count(
        start_index=start_index,
        batch_size=batch_size,
        relationships=["stickers"],
    )

    for record in records["records"]:
        data = {c.name: getattr(record, c.name) for c in record.__table__.columns}
        if hasattr(record, "stickers"):
            data["stickers"] = [
                sticker_schemas.StickerView.model_validate(sticker)
                for sticker in record.stickers
            ]
        record_list.append(data)
    return sticker_schemas.StickerCanvasResponseWithCount(
        total_count=records["total_count"],
        records=[
            sticker_schemas.StickerCanvasView.model_validate(record)
            for record in record_list
        ],
    )


@router.get("/canvas/get/{sticker_canvas_id}", status_code=status.HTTP_200_OK)
async def get_sticker_canvas(
    sticker_canvas_id: int, db: AsyncSession = Depends(get_db)
) -> sticker_schemas.StickerCanvasView:
    try:
        sticker_canvas_service = StickerCanvasCrudService(db)
        record = await sticker_canvas_service.get_by_id(
            sticker_canvas_id, relationships=["stickers"]
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Request not found"
        )
    data = {c.name: getattr(record, c.name) for c in record.__table__.columns}
    if hasattr(record, "stickers"):
        data["stickers"] = [
            sticker_schemas.StickerView.model_validate(sticker)
            for sticker in record.stickers
        ]
    return sticker_schemas.StickerCanvasView.model_validate(data)


@router.post(
    "/generate-sticker-pdf", status_code=status.HTTP_200_OK, response_model=None
)
async def generate_sticker_pdf(
    sticker_canvas_id: int,
    preview_only: bool = False,
    db: AsyncSession = Depends(get_db),
):

    try:
        service = StickerCanvasCrudService(db)
        storage_service = StickerStorageService()
        sticker_canvas = await service.get_canvas_with_stickers_and_requests(
            sticker_canvas_id
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not sticker_canvas:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sticker canvas has empty stickers.",
        )

    if not sticker_canvas.stickers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No stickers found in this canvas.",
        )

    sticker_inputs = []
    for sticker in sticker_canvas.stickers:
        req = sticker.requests
        customer_name = req.customer.name if req.customer else ""
        sticker_inputs.append(
            {
                "customer": customer_name,
                "product": req.short_description,
                "description": req.long_description,
                "labRefNo": req.ref_no,
                "quantity": str(req.quantity),
                "note": "test note",
            }
        )

    pdf_bytes: bytes = await StickerGeneratorService().generate_pdf(data=sticker_inputs)

    if preview_only:
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    f"inline; filename=sticker_canvas_{sticker_canvas_id}.pdf"
                )
            },
        )

    document_info = await storage_service.save_document_bytes(pdf_bytes=pdf_bytes)

    # Update sticker canvas details
    # update_dto = sticker_schemas.StickerCanvasUpdate.model_validate(
    #     {
    #         c.name: getattr(sticker_canvas, c.name)
    #         for c in sticker_canvas.__table__.columns
    #     }
    # )
    update_dto = sticker_schemas.StickerCanvasUpdate(
        document_id=document_info.document_id,
        relative_file_path=document_info.path,
    )

    update_dto.document_id = document_info.document_id
    update_dto.relative_file_path = document_info.path

    _ = await service.update(sticker_canvas_id, update_dto)
    return APIResponse(
        response={"document_id": document_info.document_id},
        message="New document generated.",
    )


@router.get("/document/{sticker_canvas_id}", status_code=status.HTTP_200_OK)
async def download_sticker_canvas(
    sticker_canvas_id: int,
    db: AsyncSession = Depends(get_db),
    content_disposition: str = "attachment",
) -> Response:
    try:
        storage_service = StickerStorageService()
        crud_service = StickerCanvasCrudService(db)
        canvas = await crud_service.get_by_id(sticker_canvas_id)
        if not canvas:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sticker canvas ID = {sticker_canvas_id} cannot be found.",
            )
        relative_path = getattr(canvas, "relative_file_path")
        pdf_bytes = storage_service.get_document_by_id(relative_path)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"{content_disposition}; filename=sticker-canvas-{sticker_canvas_id}.pdf"
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
