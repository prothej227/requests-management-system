from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.request import CustomerRepository, AreaRepository
from app.core.types import *


class UtilService:
    _BATCH_SIZE = 1000
    _START_INDEX = 0
    _REPO_MAPPING = {
        "customer": CustomerRepository,
        "area": AreaRepository,
    }

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dropdown_values(self, category: str) -> List[Dict[str, Any]]:
        if not category:
            return []
        repo_class = UtilService._REPO_MAPPING.get(category.lower())
        if not repo_class:
            raise ValueError(
                f"Invalid category: {category}. Available categories: [{[k for k in UtilService._REPO_MAPPING.keys()]}]"
            )
        repo: Union[CustomerRepository, AreaRepository] = repo_class(self.db)
        ref_values: Union[List[Dict[str, Any]], List[Any]] = await repo.get_all_denorm(
            start_index=UtilService._START_INDEX,
            batch_size=UtilService._BATCH_SIZE,
            field_names=["id", "name"],
        )
        return ref_values

    async def get_all_dropdown_values(self) -> Dict[str, List[Dict[str, Any]]]:
        all_values: Dict[str, List[Dict[str, Any]]] = {}
        for category in UtilService._REPO_MAPPING.keys():
            values = await self.get_dropdown_values(category)
            all_values[category] = values
        return all_values
