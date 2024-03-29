"""Entrypoint where everything starts."""
import asyncio

from fastapi import FastAPI

from src.api.routers import main_router
from src.bot.engine import background_reminder
from src.core.config import settings

app = FastAPI(title=settings.app_title)

app.include_router(main_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Define actions on startup of a fastapi app."""
    asyncio.create_task(background_reminder())
