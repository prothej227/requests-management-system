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

    long_description: Optional[str] = None
    short_description: Optional[str] = None

    sales_person_id: Optional[int] = None

    status: Optional[str] = None
    category: Optional[str] = None
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
    category: Optional[str] = None
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


class AreaCreateSchema(AreaBaseSchema):
    pass


class AreaUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)


class AreaViewSchema(BaseModel):
    id: int
    name: str

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
    category: Optional[str]
    lpo_no: Optional[str]

    short_description: Optional[str]
    long_description: Optional[str]

    sales_person_id: Optional[int]

    created_by: Optional[str]
    created_on: datetime

    modified_by: Optional[str]
    modified_on: Optional[datetime]

    customer_name: Optional[str]
    area_name: Optional[str]

    class Config:
        from_attributes = True


class RequestResponseWithCount(BaseModel):
    total_count: int
    records: list[RequestViewSchema]
