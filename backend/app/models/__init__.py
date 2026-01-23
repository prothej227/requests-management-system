# models/__init__.py

from .requests import Request, Area, Customer
from .user import User

# 🔥 This registers the event listener
import app.models.events  # noqa: F401
