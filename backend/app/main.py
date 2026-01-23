from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.config import get_settings
from contextlib import asynccontextmanager
import logging

settings = get_settings()
logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        f"Starting up {settings.app_name} in {settings.environment} environment"
    )
    yield
    logger.info(f"Shutting down {settings.app_name}")


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)
app.include_router(api_router, prefix=settings.prefix)
