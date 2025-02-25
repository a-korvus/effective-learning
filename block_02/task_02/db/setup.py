"""Main database settings."""

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable, Coroutine

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from block_02.task_02.config import pg_config

async_engine: AsyncEngine = create_async_engine(
    url=pg_config.local_url_async,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get the async session as context manager."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def session_wrapper(
    func: Callable[..., Coroutine[Any, Any, Any]],
    *args,
    **kwargs,
) -> None:
    """
    Open the async session for further operations.

    Use it function as a wrapper for other functions
    that do something with the database.

    Args:
        func (Callable[..., Coroutine[Any, Any, Any]]): Asynchronous function
        that contains some logic for interacting with the database.
    """
    async with get_session() as session:
        kwargs["session"] = session
        await func(*args, **kwargs)
