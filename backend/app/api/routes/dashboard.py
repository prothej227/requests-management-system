from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.core.database import get_db
from app.services.dashboard_service import DashboardService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/request-data", status_code=status.HTTP_200_OK)
async def request_data(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    service = DashboardService(db)
    data = await service.get_requests_data()
    return JSONResponse(content=data)


@router.get("/request-count-by-area")
async def request_count_by_area(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    service = DashboardService(db)
    data = await service.get_request_count_per_area()
    return JSONResponse(content=data)
