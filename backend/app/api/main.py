from fastapi import APIRouter

from app.api.routes import users, requests, stickers, utils, dashboard

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(stickers.router)
api_router.include_router(requests.router)
api_router.include_router(utils.router)
api_router.include_router(dashboard.router)
