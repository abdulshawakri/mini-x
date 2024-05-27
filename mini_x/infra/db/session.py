from typing import AsyncIterator

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from mini_x.settings.pg_database_settings import get_pg_database_settings

pg_settings = get_pg_database_settings()

url = URL.create(
    "postgresql+asyncpg",
    username=pg_settings.username,
    password=pg_settings.password.get_secret_value(),
    host=pg_settings.host,
    port=pg_settings.port,
    database=pg_settings.database_name,
)

engine: AsyncEngine = create_async_engine(url=url, echo=True)
async_session = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
