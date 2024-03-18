from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.bot import main_selector
from src.bot.engine import send_message
from src.bot.validators import validate_create_reminder_command
from src.core.database import get_async_session
from src.crud import crud_bot_user, crud_reminder

router = APIRouter()


@router.post("/chat")
async def chat(
    From: Annotated[str, Form(...)],
    Body: Annotated[str, Form(...)],
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
):

    phone_number = From.split(":")[1]
    bot_user = await crud_bot_user.get_or_create_by_phone_number(
        session=session,
        phone_number=phone_number,
    )

    message = await main_selector(
        bot_user, Body, session,
    )

    background_task.add_task(
        send_message,
        bot_user.phone_number,
        message,
    )
