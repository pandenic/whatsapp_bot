from fastapi import APIRouter
from src.api.endpoints import bot_router

main_router = APIRouter()

main_router.include_router(
    bot_router,
    prefix="/bot",
)
