from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator
from sqlalchemy import event
from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_uri,
    connect_args=settings.database_connect_args,
    echo=settings.database_echo,
)

SessionLocal = async_sessionmaker(engine)
Base = declarative_base()


@event.listens_for(engine.sync_engine, "connect")
def _enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
