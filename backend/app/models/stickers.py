from app.core.database import Base
from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship


class Sticker(Base):
    __tablename__ = "stickers"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(
        Integer, ForeignKey("requests.id"), nullable=False
    )  # ===> Get {customer, desciption, labref, quantity, note <feedback>}
    # Foreign key to StickerCanvas (one canvas can have many stickers, max 10)
    sticker_canvas_id = Column(
        Integer, ForeignKey("sticker_canvases.id", ondelete="CASCADE"), nullable=True
    )
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=True)
    # Relationships
    requests = relationship("Request", back_populates="stickers")
    sticker_canvases = relationship("StickerCanvas", back_populates="stickers")


class StickerCanvas(Base):
    __tablename__ = "sticker_canvases"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(36), nullable=True, unique=True)
    relative_file_path = Column(String(500), nullable=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=True)

    stickers = relationship(
        "Sticker",
        back_populates="sticker_canvases",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
