from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.bot import send_message, validate_create_reminder_command
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

    reminder_text_list = Body.split(" ")
    if not validate_create_reminder_command(
        reminder_text_list, bot_user, background_task
    ):
        return

    time_and_date = " ".join(reminder_text_list[0:2])
    text = " ".join(reminder_text_list[2:])
    remind_at = datetime.strptime(time_and_date, "%H:%M %d.%m.%Y")
    reminder = await crud_reminder.create(
        session=session,
        obj_in={
            "remind_at": remind_at,
            "text": text,
            "bot_user_id": bot_user.id,
        },
    )

    background_task.add_task(
        send_message,
        bot_user.phone_number,
        f"Reminder:\n{reminder.text}\nsaved.\n"
        f"You will be notified at:\n{reminder.remind_at}.",
    )
