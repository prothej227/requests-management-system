from typing import TypeVar
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from pydantic import BaseModel
from enum import Enum


class RecordTypeModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


class RequestStatusEnum(str, Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class FeedbackEnum(str, Enum):
    NA = "N/A"
    SATISFIED = "Approved"
    REJECTED = "Rejected"
    CANCELLED = "Cancelled"


RecordType = TypeVar("RecordType", bound=RecordTypeModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
