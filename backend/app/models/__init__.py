# models/__init__.py

from .requests import Request, Area, Customer
from .user import User
from .stickers import StickerCanvas, Sticker

# 🔥 This registers the event listener
import app.models.events  # noqa: F401


__all__ = ["Request", "Area", "Customer", "StickerCanvas", "Sticker"]
