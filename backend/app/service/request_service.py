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
import base64


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

    def decode_base64_image(self, b64_string) -> bytes:
        """
        Accepts:
        - data:image/png;base64,xxxx
        - or raw base64
        """
        if "," in b64_string:
            _, b64_data = b64_string.split(",", 1)
        else:
            b64_data = b64_string

        return base64.b64decode(b64_data)

    def bytes_to_base64(self, data: bytes, mime_type: str = "image/jpeg") -> str:
        """
        Converts raw bytes to a browser-ready base64 data URL
        """
        if not data:
            return ""

        b64 = base64.b64encode(data).decode("utf-8")
        return f"data:{mime_type};base64,{b64}"


class SalesPersonService(
    CrudService[
        SalesPerson, request.SalesPersonCreateSchema, request.SalesPersonUpdateSchema
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(SalesPerson, SalesPersonRepository, db)  # type: ignore
