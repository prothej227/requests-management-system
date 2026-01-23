from app.repositories.abc import AbstractAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type
from app.models.requests import Request, Customer, Area


class RequestRepository(AbstractAsyncRepository[Request]):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    @property
    def model(self) -> Type[Request]:
        return Request


class CustomerRepository(AbstractAsyncRepository[Customer]):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    @property
    def model(self) -> Type[Customer]:
        return Customer


class AreaRepository(AbstractAsyncRepository[Area]):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    @property
    def model(self) -> Type[Area]:
        return Area
