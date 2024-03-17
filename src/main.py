import asyncio

from fastapi import FastAPI, BackgroundTasks

from src.api.routers import main_router
from src.bot.bot import background_reminder
from src.core.config import settings

app = FastAPI(title=settings.app_title)

app.include_router(
    main_router,
    prefix="/api/v1"
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_reminder())
