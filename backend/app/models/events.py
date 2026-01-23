from sqlalchemy import event
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.requests import Request
from zoneinfo import ZoneInfo

LAB_REF_PREFIX = "LAB"
ph_timezone = ZoneInfo("Asia/Manila")


def generate_lab_ref_no(session: Session) -> str:
    """
    Generate LAB-YYYY-XXXXXX (zero-padded sequence per year).
    Example: LAB-2026-000001
    """
    year = datetime.now(ph_timezone).year

    stmt = select(func.max(Request.ref_no)).where(
        Request.ref_no.like(f"{LAB_REF_PREFIX}-{year}-%")
    )

    last_ref_no = session.execute(stmt).scalar()

    if last_ref_no:
        last_seq = int(last_ref_no.split("-")[-1])
        next_seq = last_seq + 1
    else:
        next_seq = 1

    return f"{LAB_REF_PREFIX}-{year}-{next_seq:06d}"


@event.listens_for(Request, "before_insert")
def request_before_insert(mapper, connection, target: Request):
    if not bool(target.ref_no):
        session = Session(bind=connection)
        try:
            target.ref_no = generate_lab_ref_no(session)  # type: ignore
        finally:
            session.close()
