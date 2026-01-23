from pydantic import BaseModel, EmailStr, Field, field_validator
from app.core.types import *
import re


class UserBase(BaseModel):
    email: EmailStr = Field(
        ..., example="john.doe@domain.com"
    )  # pyright: ignore[reportCallIssue]
    username: str = Field(
        ..., min_length=3, max_length=80, example="johndoe"
    )  # pyright: ignore[reportCallIssue]
    first_name: str = Field(
        ..., min_length=2, max_length=80, example="John"
    )  # pyright: ignore[reportCallIssue]
    last_name: str = Field(
        ..., min_length=2, max_length=80, example="Doe"
    )  # pyright: ignore[reportCallIssue]
    role: str = Field(
        ..., example="admin"
    )  # e.g., "admin", "user", "manager" # pyright: ignore[reportCallIssue]
    is_active: bool = Optional[
        Field(..., example="true")  # type: ignore
    ]  # pyright: ignore[reportCallIssue, reportAssignmentType]

    @classmethod
    @field_validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character.")
        return v


class UserCreate(UserBase):
    password: str = Field(
        ..., min_length=8, example="strongpassword"
    )  # pyright: ignore[reportCallIssue]

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    id: int
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        orm_mode = True


class APIResponse(BaseModel):
    response: Union[UserPublic, Dict, None]
    message: str
