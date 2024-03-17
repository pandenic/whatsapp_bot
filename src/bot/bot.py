import asyncio
import logging
from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import selectinload
from twilio.rest import Client

from src.core.config import settings
from src.core.database import get_async_session, AsyncSessionLocal
from src.crud import crud_reminder

account_sid = settings.twilio_account_sid
auth_token = settings.twilio_auth_token
client = Client(account_sid, auth_token)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:+14155238886",
            body=body_text,
            to=f"whatsapp:{to_number}"
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
                reminders = await crud_reminder.get_current_unsent_reminders_now(
                    session=session,
                    time_now=now,
                )
                for reminder in reminders:
                    reminder.is_reminded = True
                    await crud_reminder.commit_and_refresh(reminder, session)
                    bot_user = await session.run_sync(lambda session: reminder.bot_user)
                    message = (f"Kindly remind:\n{reminder.text}")
                    await asyncio.create_task(send_message(bot_user.phone_number, message))
            print(now)
        await asyncio.sleep(1)
