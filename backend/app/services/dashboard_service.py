from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from app.core.types import *
from app.models.requests import Request, Area
from app.models.generic import RequestStatusEnum


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_requests_data(self) -> Dict[str, Any]:

        stmt = select(
            func.count(Request.id).label("total_count"),
            func.sum(
                case(
                    (Request.status == RequestStatusEnum.NOT_STARTED.value, 1), else_=0
                )
            ).label("not_started_count"),
            func.sum(
                case(
                    (Request.status == RequestStatusEnum.IN_PROGRESS.value, 1), else_=0
                )
            ).label("in_progress_count"),
            func.sum(
                case((Request.status == RequestStatusEnum.COMPLETED.value, 1), else_=0)
            ).label("completed_count"),
        )

        result = await self.db.execute(stmt)
        result = result.one()
        return {
            "total_count": result.total_count,
            "not_started_count": (
                result.not_started_count if result.not_started_count else 0
            ),
            "in_progress_count": (
                result.in_progress_count if result.in_progress_count else 0
            ),
            "completed_count": (
                result.completed_count if result.completed_count else 0
            ),
        }

    async def get_request_count_per_area(self) -> dict[str, int]:
        stmt = (
            select(Area.name, func.count(Request.id))
            .join(Request, Request.area_id == Area.id)
            .group_by(Area.name)
        )

        result = await self.db.execute(stmt)

        return {area_name: request_count for area_name, request_count in result.all()}
