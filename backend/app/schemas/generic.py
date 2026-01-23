from pydantic import BaseModel
from app.schemas.users import UserPublic
from app.core.types import *


class APIResponse(BaseModel):
    response: Optional[Dict[str, Any]]
    message: Optional[str] = "Request processed sucessfully."


class LoginResponse(BaseModel):
    message: str
    access_token: str
    user: UserPublic
