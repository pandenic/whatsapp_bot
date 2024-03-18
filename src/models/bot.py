"""Contain models for a bot operations description."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.constants import RepeatInterval, Selector
from src.core.database import Base


class BotUser(Base):
    """
    Contain a bot user model description.

    phone_number - user's phone number
    reminders - a list of user's reminders
    selector_status - show current user's bot action selector status
    """

    phone_number: Mapped[str]
    reminders: Mapped[Optional[List["Reminder"]]] = relationship(
        backref="bot_user", lazy="joined",
    )
    selector_status: Mapped[Selector] = mapped_column(
        default=Selector.GREETING,
    )


class Reminder(Base):
    """
    Contain a reminder model description.

    bot_user_id - foreign key for user id who owns a reminder
    text - a reminder text
    created_at - datetime when a reminder was created
    remind_at - datetime when a reminder should remind
    is_reminded - flag that shows if a reminder was reminded
    repeat_interval - interval with which a reminder should remind again
    """

    bot_user_id: Mapped[UUID] = mapped_column(ForeignKey("botuser.id"))
    text: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    remind_at: Mapped[datetime]
    is_reminded: Mapped[bool] = mapped_column(default=False)
    repeat_interval: Mapped[RepeatInterval] = mapped_column(
        default=RepeatInterval.NON_REPEAT,
    )
