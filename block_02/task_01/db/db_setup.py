"""Main database settings."""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from block_02.task_01.config import pg_config

async_engine: AsyncEngine = create_async_engine(
    url=pg_config.url_async,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)
