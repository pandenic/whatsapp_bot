from typing import TypeVar, Generic, Type

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBotUser(Generic[
    ModelType,
    CreateSchemaType,
    UpdateSchemaType
]):

    def __init__(
            self,
            model: Type[ModelType]
    ):
        self.model = model

    async def get_by_phone_number(
            self,
            session: AsyncSession,
            phone_number: str,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.phone_number == phone_number
            )
        )
        return db_obj.scalars().first()
        
    async def create(
            self,
            session: AsyncSession,
            phone_number: str,
    ) -> ModelType:
        db_obj = self.model(phone_number)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

