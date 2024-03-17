import asyncio
import logging
import re
from datetime import datetime
from typing import List

from fastapi import BackgroundTasks
from twilio.rest import Client

from src.core.config import settings
from src.core.database import AsyncSessionLocal
from src.core.exceptions import (WrongBotDateFormat,
                                 WrongBotReminderCreateFormat,
                                 WrongBotTimeFormat)
from src.core.regex_patterns import RegexPatterns
from src.crud import crud_reminder
from src.models import BotUser

account_sid = settings.twilio_account_sid
auth_token = settings.twilio_auth_token
client = Client(account_sid, auth_token)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{settings.whatsapp_sender}",
            body=body_text,
            to=f"whatsapp:{to_number}",
        )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")


async def background_reminder():
    while True:
        now = datetime.now()
        if now.second == 0:
            reminders = []
            async with AsyncSessionLocal() as session:
                reminders = (
                    await crud_reminder.get_current_unsent_reminders_now(
                        session=session,
                        time_now=now,
                    )
                )
                for reminder in reminders:
                    reminder.is_reminded = True
                    await crud_reminder.commit_and_refresh(reminder, session)
                    bot_user = await session.run_sync(
                        lambda session: reminder.bot_user
                    )
                    message = f"Kindly remind:\n{reminder.text}"
                    await asyncio.create_task(
                        send_message(bot_user.phone_number, message)
                    )
            print(now)
        await asyncio.sleep(1)


def validate_create_reminder_command(
    reminder_text_list: List[str],
    bot_user: BotUser,
    background_task: BackgroundTasks,
):

    try:
        if len(reminder_text_list) < 3:
            raise WrongBotReminderCreateFormat(
                "Wrong reminder format.\n" "Pattern HH:MM dd.mm.YYYY text"
            )
        if not re.match(RegexPatterns.BOT_TIME, reminder_text_list[0]):
            raise WrongBotTimeFormat(
                "Wrong time.\nPattern HH:MM.\n" "From 0:00 to 23:59."
            )
        if not re.match(RegexPatterns.BOT_DATE, reminder_text_list[1]):
            raise WrongBotDateFormat(
                "Wrong date.\nPattern dd.mm.YYYY.\n"
                "From 01.01.1600 to 31.12.9999."
            )
    except (
        WrongBotReminderCreateFormat,
        WrongBotTimeFormat,
        WrongBotDateFormat,
    ) as error:
        background_task.add_task(
            send_message,
            bot_user.phone_number,
            error,
        )
        return False
    return True
