from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import (
    create_async_engine,
)

from sqlalchemy.orm import sessionmaker

from src.config import Config


# Database URL .env se aa raha hai
DATABASE_URL = Config.DATABASE_URL


# Async database engine
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


# Create database tables
async def init_db():

    async with async_engine.begin() as conn:

        await conn.run_sync(
            SQLModel.metadata.create_all
        )


# Create database session
async def get_session():

    async_session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:

        yield session