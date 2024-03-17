import json
from datetime import datetime
from http import HTTPStatus
from typing import Annotated

import requests
from fastapi import APIRouter, Form, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from src.bot.bot import send_message
from src.core.config import settings
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
    if len(reminder_text_list) < 3:
        return ""
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
        f"You will be notified at:\n{reminder.remind_at}." )

    return "" # Response(content=str(response), media_type="application/xml")
