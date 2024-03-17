from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class RepeatInterval(Enum):
    non_repeat = Annotated[str, "Non-repeatable"]
    everyday = Annotated[str, "Everyday"]
    every_week = Annotated[str, "Every week"]
    every_month = Annotated[str, "Every month"]
    every_year = Annotated[str, "Every year"]


class Selector(Enum):
    greeting = Annotated[str, "Greeting"]
    create_reminder = Annotated[str, "Create reminder"]
    show_active_reminders = Annotated[str, "Show active reminders"]
    delete_reminder = Annotated[str, "Delete reminder"]
    creat_repeatable_reminder = Annotated[str, "Create repeatable reminder"]


class BotUser(AsyncAttrs, Base):

    phone_number: Mapped[str]
    reminders: Mapped[Optional["Reminder"]] = relationship(backref="bot_user")
    # selector_status: Mapped[Selector] = mapped_column(default=Selector.greeting)


class Reminder(AsyncAttrs, Base):

    bot_user_id: Mapped[UUID] = mapped_column(ForeignKey("botuser.id"))
    text: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    remind_at: Mapped[datetime]
    is_reminded: Mapped[bool] = mapped_column(default=False)
    # repeat_interval: Mapped[RepeatInterval] = mapped_column(default=RepeatInterval.non_repeat)
