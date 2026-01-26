from app.service.crud import CrudService
from app.schemas import request
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.requests import Request, Customer, Area, SalesPerson
from app.repositories.request import (
    RequestRepository,
    CustomerRepository,
    AreaRepository,
    SalesPersonRepository,
)


class RequestService(
    CrudService[Request, request.RequestCreateSchema, request.RequestUpdateSchema]
):
    def __init__(self, db: AsyncSession):
        super().__init__(Request, RequestRepository, db)  # type: ignore


class CustomerService(
    CrudService[Customer, request.CustomerCreateSchema, request.CustomerUpdateSchema]
):
    def __init__(self, db: AsyncSession):
        super().__init__(Customer, CustomerRepository, db)  # type: ignore


class AreaService(
    CrudService[Area, request.AreaCreateSchema, request.AreaUpdateSchema]
):
    def __init__(self, db: AsyncSession):
        super().__init__(Area, AreaRepository, db)  # type: ignore


class SalesPersonService(
    CrudService[
        SalesPerson, request.SalesPersonCreateSchema, request.SalesPersonUpdateSchema
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(SalesPerson, SalesPersonRepository, db)  # type: ignore
