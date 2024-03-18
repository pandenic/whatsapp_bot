"""Contain functions for a basic bot functioning."""
import asyncio
import logging
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from twilio.rest import Client

from src.core.config import settings
from src.core.constants import RepeatInterval
from src.core.database import AsyncSessionLocal
from src.crud import crud_reminder

account_sid = settings.twilio_account_sid
auth_token = settings.twilio_auth_token
client = Client(account_sid, auth_token)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def send_message(to_number, body_text):
    """Define message sending."""
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
    """Define endless loop for a reminder processing."""
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
                    if reminder.repeat_interval == RepeatInterval.NON_REPEAT:
                        reminder.is_reminded = True
                    elif reminder.repeat_interval == RepeatInterval.EVERYDAY:
                        reminder.remind_at += timedelta(hours=24)
                    elif reminder.repeat_interval == RepeatInterval.EVERY_WEEK:
                        reminder.remind_at += timedelta(weeks=1)
                    elif (
                        reminder.repeat_interval == RepeatInterval.EVERY_MONTH
                    ):
                        reminder.remind_at += relativedelta(months=1)
                    elif reminder.repeat_interval == RepeatInterval.EVERY_YEAR:
                        reminder.remind_at += relativedelta(years=1)
                    await crud_reminder.commit_and_refresh(reminder, session)
                    bot_user = reminder.bot_user
                    message = f"Kindly remind:\n{reminder.text}"
                    await asyncio.create_task(
                        send_message(bot_user.phone_number, message),
                    )
        await asyncio.sleep(1)
