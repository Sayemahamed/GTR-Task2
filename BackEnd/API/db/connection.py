
from API.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager


async_engine: AsyncEngine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,  
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_timeout=settings.POOL_TIMEOUT,
    pool_recycle=settings.POOL_RECYCLE,
)

async_session_maker = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db() -> None:
    """Initializes the database by creating all tables defined by SQLModel models."""
    async with async_engine.begin() as conn:
        try:
            from API.db.models import (  
                Device
            )

            await conn.run_sync(SQLModel.metadata.create_all)
        except Exception as e:
            raise  


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    """Dependency function that yields an async session."""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()  

@asynccontextmanager
async def get_agent_session() -> AsyncGenerator[AsyncSession, None]:
    """
    A self-contained session generator for use in background tasks or agent tools.
    It handles the entire lifecycle: creation, commit/rollback, and closing.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()