"""Settings for database connection and sessions creation."""
import uuid
from typing import AsyncGenerator

from sqlalchemy import Column, UUID
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine, AsyncAttrs)
from sqlalchemy.orm import declarative_base, declared_attr

from src.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls): # noqa
        """Bind table name to the class name."""
        return cls.__name__.lower()

    id = Column(UUID, primary_key=True, default=uuid.uuid4)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.postgres_connection_url)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Create async db session."""
    async with AsyncSessionLocal() as session:
        yield session