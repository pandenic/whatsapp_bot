from datetime import datetime
from enum import Enum
from typing import Optional, Annotated

from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import UUID, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class RepeatInterval(Enum):
    everyday = Annotated[str, "Каждый день"]
    every_week = Annotated[str, "Каждую неделю"]
    every_month = Annotated[str, "Каждый месяц"]
    every_year = Annotated[str, "Каждый год"]


class BotUser(Base):

    phone_number: Mapped[str]
    reminders: Mapped[Optional["Reminder"]] = relationship(back_populates="bot_user")


class Reminder(Base):

    bot_user_id: Mapped[UUID] = mapped_column(ForeignKey("botuser.id"))
    bot_user: Mapped[BotUser] = relationship(back_populates="reminders")
    text: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    remind_at: Mapped[datetime]
    repeat_interval: Mapped[Optional[RepeatInterval]]