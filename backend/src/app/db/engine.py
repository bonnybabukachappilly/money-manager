# app/db/engine.py

from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession,
    async_sessionmaker, create_async_engine
)

from app.core import get_settings, Settings


settings: Settings = get_settings()


def _build_database_url() -> str:
    if settings.database_url.startswith('postgresql+asyncpg://'):
        return settings.database_url

    if settings.database_url.startswith('postgresql://'):
        return settings.database_url.replace(
            'postgresql://',
            'postgresql+asyncpg://',
            1,
        )

    raise ValueError('DATABASE_URL must start with postgresql://')


DATABASE_URL: str = _build_database_url()


engine: AsyncEngine = create_async_engine(
    DATABASE_URL,

    # Logging
    echo=settings.debug,

    # Pool configuration
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,

    # Optional future-proofing
    future=True,
)


# Session factory
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)
