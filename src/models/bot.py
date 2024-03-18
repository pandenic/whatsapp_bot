import enum
from datetime import datetime

from typing import Annotated, Optional, List

from sqlalchemy import UUID, ForeignKey, Enum
from sqlalchemy.dialects import postgresql as ps
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from src.core.constants import Selector, RepeatInterval
from src.core.database import Base
import alembic_postgresql_enum


class BotUser(AsyncAttrs, Base):

    phone_number: Mapped[str]
    reminders: Mapped[Optional[List["Reminder"]]] = relationship(backref="bot_user", lazy="joined")
    selector_status: Mapped[Selector] = mapped_column(default=Selector.GREETING)


class Reminder(AsyncAttrs, Base):

    bot_user_id: Mapped[UUID] = mapped_column(ForeignKey("botuser.id"))
    text: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    remind_at: Mapped[datetime]
    is_reminded: Mapped[bool] = mapped_column(default=False)
    repeat_interval: Mapped[RepeatInterval] = mapped_column(default=RepeatInterval.NON_REPEAT)
