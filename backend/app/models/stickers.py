from app.core.database import Base
from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Request


class Sticker(Base):
    __tablename__ = "stickers"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(
        Integer, ForeignKey("requests.id"), nullable=True
    )  # ===> Get {customer, desciption, labref, quantity, note <feedback>}
    # Foreign key to StickerCanvas (one canvas can have many stickers, max 10)
    canvas_id = Column(Integer, ForeignKey("sticker_canvases.id"), nullable=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=True)
    # Relationships
    requests = relationship("Request", back_populates="stickers")
    sticker_canvases = relationship("StickerCanvas", back_populates="stickers")


class StickerCanvas(Base):
    __tablename__ = "sticker_canvases"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False, unique=True)
    relative_file_path = Column(String(500), nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=True)

    stickers = relationship("Sticker", back_populates="sticker_canvases")
