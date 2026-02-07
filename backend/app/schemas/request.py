from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


# -------------------------
# Shared Base Schema
# -------------------------
class RequestBaseSchema(BaseModel):
    date_received: Optional[date] = None
    customer_id: int
    area_id: int
    sales_person_id: Optional[int] = None
    long_description: Optional[str] = None
    short_description: Optional[str] = None
    status: Optional[str] = None
    feedback: Optional[str] = None
    quantity: Optional[int] = None
    lpo_no: Optional[str] = None


# -------------------------
# Create Schema (POST)
# -------------------------
class RequestCreateSchema(RequestBaseSchema):
    created_by: Optional[str] = None
    # lab_ref_no is NOT here → auto-generated


# -------------------------
# Update Schema (PATCH/PUT)
# -------------------------
class RequestUpdateSchema(BaseModel):
    date_received: Optional[date] = None
    customer_id: Optional[int] = None
    area_id: Optional[int] = None

    long_description: Optional[str] = None
    short_description: Optional[str] = None

    sales_person_id: Optional[int] = None

    status: Optional[str] = None
    feedback: Optional[str] = None
    quantity: Optional[int] = None
    lpo_no: Optional[str] = None

    modified_by: Optional[str] = None


# -------------------------
# Customer Schemas
# -------------------------
class CustomerBaseSchema(BaseModel):
    name: str = Field(..., max_length=255)


class CustomerCreateSchema(CustomerBaseSchema):
    pass


class CustomerUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)


class CustomerViewSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# -------------------------
# Area Schemas
# -------------------------
class AreaBaseSchema(BaseModel):
    name: str = Field(..., max_length=255)
    logo: Optional[str | bytes]


class AreaCreateSchema(AreaBaseSchema):
    pass


class AreaUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    logo: Optional[str | bytes]


class AreaViewSchema(BaseModel):
    id: int
    name: str
    logo: Optional[str | bytes]

    class Config:
        from_attributes = True


# -------------------------
# SalesPerson Schemas
# -------------------------
class SalesPersonBaseSchema(BaseModel):
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)


class SalesPersonCreateSchema(SalesPersonBaseSchema):
    pass


class SalesPersonUpdateSchema(BaseModel):
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)


class SalesPersonViewSchema(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


# -------------------------
# View Schema (API Response)
# -------------------------
class RequestViewSchema(BaseModel):
    id: int

    ref_no: str
    date_received: Optional[date]

    status: Optional[str]
    feedback: Optional[str]
    lpo_no: Optional[str]
    quantity: Optional[int]
    short_description: Optional[str]
    long_description: Optional[str]

    sales_person: Optional[str]

    created_by: Optional[str]
    created_on: datetime

    modified_by: Optional[str]
    modified_on: Optional[datetime]

    customer_name: Optional[str]
    area_name: Optional[str]

    class Config:
        from_attributes = True


class RequestNormalViewSchema(BaseModel):
    id: int

    ref_no: str
    date_received: Optional[date]

    status: Optional[str]
    feedback: Optional[str]
    lpo_no: Optional[str]
    quantity: Optional[int]
    short_description: Optional[str]
    long_description: Optional[str]

    sales_person_id: Optional[int]

    created_by: Optional[str]
    created_on: datetime

    modified_by: Optional[str]
    modified_on: Optional[datetime]

    customer_id: Optional[int]
    area_id: Optional[int]

    class Config:
        from_attributes = True


class RequestResponseWithCount(BaseModel):
    total_count: int
    records: (
        list[RequestViewSchema]
        | list[AreaViewSchema]
        | list[CustomerViewSchema]
        | list[SalesPersonViewSchema]
    )
