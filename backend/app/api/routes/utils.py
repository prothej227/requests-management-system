from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.generic import APIResponse
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.util_service import UtilService

router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/dropdown-values", status_code=status.HTTP_200_OK)
async def get_dropdown_values(
    category: str, db: AsyncSession = Depends(get_db)
) -> APIResponse:
    service = UtilService(db)
    try:
        dropdown_values = await service.get_dropdown_values(category)
        return APIResponse(response={"category": category, "values": dropdown_values})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/all-dropdown-values", status_code=status.HTTP_200_OK)
async def get_all_dropdown_values(db: AsyncSession = Depends(get_db)) -> APIResponse:
    service = UtilService(db)
    try:
        all_values = await service.get_all_dropdown_values()
        return APIResponse(response=all_values)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
