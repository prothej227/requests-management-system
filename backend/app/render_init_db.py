# initialize db for render.com deployment

import asyncio
from app.core.database import engine, Base
from app.models import *
from app.core.config import get_settings

settings = get_settings()
print("✅ Database tables created successfully.")
print(f"Settings URI={settings.database_uri} | base_dir={settings.base_dir}")


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
