import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/aegis")

_engine = None  # will be initialised on startup
_sessionmaker: async_sessionmaker[AsyncSession] | None = None


async def init_db() -> None:
    global _engine, _sessionmaker
    if _engine is None:
        _engine = create_async_engine(DATABASE_URL, echo=False, future=True)
        _sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if _sessionmaker is None:
        raise RuntimeError("DB not initialised")
    async with _sessionmaker() as session:
        yield session


async def close_db() -> None:
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None