"""Define classes for CRUD operations with models."""
from datetime import datetime
from typing import Generic, List, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import Base
from src.models import BotUser, Reminder

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Define CRUD operations as superclass."""

    def __init__(self, model: Type[ModelType]):
        """Init for CRUDBase class."""
        self.model = model

    async def create(
        self,
        session: AsyncSession,
        obj_in: dict[str, str],
    ) -> ModelType:
        """Create a new object in DB."""
        new_obj = self.model(**obj_in)
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
        return new_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ) -> ModelType:
        """Remove an object from DB."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def commit_and_refresh(
        self,
        db_obj,
        session: AsyncSession,
    ) -> ModelType:
        """Commit to DB and refresh values."""
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


class CRUDBotUser(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Define CRUD operations for a bot user model."""

    async def get_by_phone_number(
        self,
        session: AsyncSession,
        phone_number: str,
    ):
        """Return user object by phone number."""
        db_obj = await session.execute(
            select(self.model).where(self.model.phone_number == phone_number),
        )
        return db_obj.scalars().first()

    async def get_or_create_by_phone_number(
        self,
        session: AsyncSession,
        phone_number: str,
    ):
        """
        Create a new user if they use a bot for the first time.

        Or return existed.
        """
        bot_user = await self.get_by_phone_number(
            session=session,
            phone_number=phone_number,
        )
        if bot_user:
            return bot_user
        return await self.create(
            session=session,
            obj_in={"phone_number": phone_number},
        )

    async def get_unsent_reminders(
        self,
        session: AsyncSession,
        bot_user: BotUser,
    ):
        """Return all reminders that are going to be sent in the future."""
        reminders = await session.run_sync(lambda session: bot_user.reminders)
        if not reminders:
            return []
        now = datetime.now()
        return [reminder for reminder in reminders if reminder.remind_at > now]


class CRUDReminder(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Define CRUD operations for a reminder model."""

    async def get_current_unsent_reminders_now(
        self,
        session: AsyncSession,
        time_now: datetime,
    ) -> List[ModelType]:
        """Return unsent reminder at a current minute only."""
        time_without_seconds = time_now.replace(second=0, microsecond=0)
        db_objs = await session.execute(
            select(self.model)
            .where(self.model.remind_at == time_without_seconds)
            .where(self.model.is_reminded == False)  # noqa
        )
        return db_objs.scalars().all()


crud_reminder = CRUDReminder(Reminder)
crud_bot_user = CRUDBotUser(BotUser)
