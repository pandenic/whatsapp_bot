"""Contain bot processing functions."""
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.bot import validators as v
from src.core.constants import RepeatInterval, Selector
from src.crud import crud_reminder
from src.models import BotUser


async def update_selector_to(
    bot_user: BotUser,
    session: AsyncSession,
    selector: Selector,
) -> None:
    """Update user's selector."""
    bot_user.selector_status = selector
    await crud_reminder.commit_and_refresh(bot_user, session)


async def greeting() -> str:
    """Process greeting command."""
    return (
        f"You can choose commands:\n\n"
        f"{Selector.get_numbered_str(1)}.\n\nJust write a number.\n"
        f"If you want to get back to menu, just write 'Menu'"
    )


async def create_new_reminder(
    bot_user: BotUser, body_text: str, session: AsyncSession, is_start: bool,
) -> str:
    """Process create new reminder command."""
    if is_start:
        return (
            "You can create a reminder using format:\n"
            "HH:MM dd.mm.YYYY any text\n\n"
            "Example:\n"
            "20:15 01.01.2025 drop table;"
        )
    reminder_text_list = body_text.split(" ")
    message = await v.validate_create_reminder_command(
        reminder_text_list,
    )
    if message:
        return message

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

    return (
        f"Reminder:\n{reminder.text}\nsaved.\n"
        f"You will be notified at:\n{reminder.remind_at}.\n"
    )


async def show_active_reminder(
    bot_user: BotUser,
    session: AsyncSession,
    is_start: bool,
) -> str:
    """Process show active reminder command."""
    reminders = bot_user.reminders
    reminders_numbered_list = "\n".join(
        [
            str(i) + ": " + str(reminder.remind_at) + " " + reminder.text
            for i, reminder in enumerate(reminders)
        ],
    )
    if is_start:
        await update_selector_to(
            bot_user,
            session,
            Selector.GREETING,
        )
    return f"Your active reminders:\n\n" f"{reminders_numbered_list}"


async def delete_reminder(
    bot_user: BotUser,
    body_text: str,
    session: AsyncSession,
    is_start: bool,
) -> str:
    """Process delete reminder command."""
    if is_start:
        message = "Choose reminder to delete.\nJust write a number.\n\n"
        message += await show_active_reminder(
            bot_user,
            session,
            is_start=False,
        )
        return message

    message = await v.validate_reminder_delete_number(body_text)
    if message:
        return message
    number = int(body_text)
    reminders = bot_user.reminders
    message = await v.validate_reminder_number_is_exist(number, len(reminders))
    if message:
        return message
    await crud_reminder.remove(reminders[number], session)
    reminders.pop(number)
    reminders_numbered_list = "\n".join(
        [
            str(i) + ": " + str(reminder.remind_at) + " " + reminder.text
            for i, reminder in enumerate(reminders)
        ],
    )
    return (
        f"Successfully deleted.\n\n"
        f"You're active reminders:\n\n"
        f"{reminders_numbered_list}"
    )


async def create_repeatable_reminder(
    bot_user: BotUser, body_text: str, session: AsyncSession, is_start: bool,
) -> str:
    """Process create repeatable reminder command."""
    if is_start:
        return (
            f"You can choose a repetition by code:\n\n"
            f"{RepeatInterval.get_numbered_str()}\n\n"
            f"You can create a reminder using format:\n"
            f"[repeat_code] HH:MM dd.mm.YYYY any text\n"
            f"Example:\n0 20:15 01.01.2025 drop table;"
        )
    reminder_text_list = body_text.split(" ")
    message = await v.validate_create_repeatable_reminder_command(
        reminder_text_list, len(RepeatInterval.get_list()),
    )
    if message:
        return message

    time_and_date = " ".join(reminder_text_list[1:3])
    text = " ".join(reminder_text_list[3:])
    remind_at = datetime.strptime(time_and_date, "%H:%M %d.%m.%Y")
    repeat_interval = RepeatInterval.get_list()[int(reminder_text_list[0])]
    reminder = await crud_reminder.create(
        session=session,
        obj_in={
            "remind_at": remind_at,
            "text": text,
            "bot_user_id": bot_user.id,
            "repeat_interval": repeat_interval,
        },
    )

    return (
        f"Reminder:\n{reminder.text}\nsaved.\n"
        f"You will be notified at:\n{reminder.remind_at}.\n\n"
        f"It will be repeated {repeat_interval.value.lower()}"
    )


async def main_selector(
    bot_user: BotUser,
    body_text: str,
    session: AsyncSession,
) -> str:
    """Define main menu command selector."""
    is_start = False
    if body_text == "Menu":
        await update_selector_to(
            bot_user,
            session,
            Selector.GREETING,
        )
        return await greeting()
    if bot_user.selector_status == Selector.GREETING:
        message = await v.validate_selector_choice(body_text)
        if message:
            return message
        is_start = True
        await update_selector_to(
            bot_user,
            session,
            Selector.get_list()[int(body_text)],
        )

    selector_dict = {
        Selector.GREETING: greeting(),
        Selector.CREATE_REMINDER: create_new_reminder(
            bot_user, body_text, session, is_start,
        ),
        Selector.SHOW_ACTIVE_REMINDERS: show_active_reminder(
            bot_user, session, is_start,
        ),
        Selector.DELETE_REMINDER: delete_reminder(
            bot_user, body_text, session, is_start,
        ),
        Selector.CREATE_REPEATABLE_REMINDER: create_repeatable_reminder(
            bot_user, body_text, session, is_start,
        ),
    }

    return await selector_dict[bot_user.selector_status]
