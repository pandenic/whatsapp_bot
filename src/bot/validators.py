"""Describe validatore for a bot moduile."""
import re
from typing import List

from src.core import exceptions as e
from src.core.constants import RegexPatterns, Selector


async def validate_create_reminder_command(
    reminder_text_list: List[str],
):
    """Check if a text match create reminder command pattern."""
    try:
        if len(reminder_text_list) < 3:
            raise e.WrongBotReminderCreateFormat(
                "Wrong reminder format.\n" "Pattern HH:MM dd.mm.YYYY text",
            )
        if not re.match(RegexPatterns.BOT_TIME, reminder_text_list[0]):
            raise e.WrongBotTimeFormat(
                "Wrong time.\n" "Pattern HH:MM.\nFrom 0:00 to 23:59.",
            )
        if not re.match(RegexPatterns.BOT_DATE, reminder_text_list[1]):
            raise e.WrongBotDateFormat(
                "Wrong date.\nPattern dd.mm.YYYY.\n"
                "From 01.01.1600 to 31.12.9999.",
            )
    except (
        e.WrongBotReminderCreateFormat,
        e.WrongBotTimeFormat,
        e.WrongBotDateFormat,
    ) as error:
        return error


async def validate_create_repeatable_reminder_command(
    reminder_text_list: List[str],
    repeat_scenarios_quantity: int,
):
    """Check if a text match create repeatable reminder command pattern."""
    try:
        if len(reminder_text_list) < 4:
            raise e.WrongBotReminderCreateFormat(
                "Wrong reminder format.\n"
                "Pattern [code] HH:MM dd.mm.YYYY text",
            )
        if (
            not reminder_text_list[0].isdigit()
            and 0 > int(reminder_text_list[0]) > repeat_scenarios_quantity
        ):
            raise e.WrongSelectorValue(
                f"Wrong repeat selector.\n"
                f"Pattern [code].\nFrom 0 to {repeat_scenarios_quantity-1}.",
            )
        if not re.match(RegexPatterns.BOT_TIME, reminder_text_list[1]):
            raise e.WrongBotTimeFormat(
                "Wrong time.\n" "Pattern HH:MM.\n" "From 0:00 to 23:59.",
            )
        if not re.match(RegexPatterns.BOT_DATE, reminder_text_list[2]):
            raise e.WrongBotDateFormat(
                "Wrong date.\nPattern dd.mm.YYYY.\n"
                "From 01.01.1600 to 31.12.9999.",
            )
    except (
        e.WrongBotReminderCreateFormat,
        e.WrongSelectorValue,
        e.WrongBotTimeFormat,
        e.WrongBotDateFormat,
    ) as error:
        return error


async def validate_selector_choice(
    choice: str,
):
    """Check if selector choice is available."""
    try:
        if not choice.isdigit() or int(choice) >= len(list(Selector)):
            raise e.WrongSelectorValue(
                f"Wrong selector value.\n"
                f"Choose a number between 1 and {len(Selector.get_list())-1}",
            )
    except e.WrongSelectorValue as error:
        return error


async def validate_reminder_delete_number(
    value: str,
):
    """Validate if a written number is greater than or equal to 0."""
    try:
        if not value.isdigit() or int(value) < 0:
            raise e.WrongReminderNumber(
                "Write a number. It should be greater than or equal to 0.",
            )
    except e.WrongReminderNumber as error:
        return error


async def validate_reminder_number_is_exist(number: int, quantity: int):
    """Validate if a written number match an existing reminder."""
    try:
        if quantity <= number:
            raise e.WrongReminderNumber(
                f"Reminder with this number does not exist.\n"
                f"Write number from 0 to {quantity-1}.",
            )
    except e.WrongReminderNumber as error:
        return error
