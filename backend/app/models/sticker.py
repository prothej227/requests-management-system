from app.core.database import Base
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class StickerJob(Base):
    __tablename__ = "sticker_jobs"

    job_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
