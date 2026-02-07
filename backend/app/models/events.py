from sqlalchemy import event
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.requests import Request
from zoneinfo import ZoneInfo
from app.core.config import get_settings

settings = get_settings()
env_timezone = ZoneInfo(settings.timezone)


def generate_lab_ref_no(session: Session) -> str:
    """
    Generate MM-YYYY-XXXXXX (zero-padded sequence per year).
    Example: 01-2026-000001
    """
    now = datetime.now(env_timezone)
    month = now.month
    year = now.year

    stmt = select(func.max(Request.ref_no)).where(
        Request.ref_no.like(f"{month:02d}-{year}-%")
    )

    last_ref_no = session.execute(stmt).scalar()

    if last_ref_no:
        last_seq = int(last_ref_no.split("-")[-1])
        next_seq = last_seq + 1
    else:
        next_seq = 1

    return f"{month:02d}-{year}-{next_seq:04d}"


@event.listens_for(Request, "before_insert")
def request_before_insert(mapper, connection, target: Request):
    if not bool(target.ref_no):
        session = Session(bind=connection)
        try:
            target.ref_no = generate_lab_ref_no(session)  # type: ignore
        finally:
            session.close()
