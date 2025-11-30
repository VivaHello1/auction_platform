from asyncio import current_task
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.schema import CreateSchema

from .schema_base import ModelDeclarativeBase


def _get_current_task_id() -> Any:
    try:
        return id(current_task())
    except LookupError:
        return id(current_task())


class Database:
    def __init__(self, db_url: str, schema: str):
        self.schema = schema
        async_engine = create_async_engine(
            db_url,
            echo=False,
            future=True,
            pool_pre_ping=True,
            # pool_recycle=,  # TODO
        )
        self.async_engine = async_engine.execution_options(schema_translate_map={None: self.schema})

        self.async_session_factory = async_sessionmaker(
            self.async_engine,
            class_=AsyncSession,
            autoflush=True,
            expire_on_commit=False,
        )

        engine = create_engine(
            db_url.replace("postgresql+asyncpg://", "postgresql://"),
            echo=False,
            future=True,
        )

        self.engine = engine.execution_options(schema_translate_map={None: self.schema})
        self.sync_session_factory = sessionmaker(self.engine, class_=Session, autoflush=True, expire_on_commit=False)

    async def init_db(self) -> None:
        async with self.async_engine.begin() as conn:
            await conn.execute(CreateSchema(self.schema, if_not_exists=True))
            await conn.run_sync(ModelDeclarativeBase.metadata.create_all)

    async def close_db(self) -> None:
        await self.async_engine.dispose()
        self.engine.dispose()

    @asynccontextmanager
    async def session_factory(self) -> AsyncGenerator[AsyncSession, None]:
        scoped_session_factory = async_scoped_session(self.async_session_factory, scopefunc=_get_current_task_id)
        try:
            async with scoped_session_factory() as session, session.begin():
                try:
                    yield session
                except Exception:
                    await session.rollback()
                    raise
        except Exception:
            await scoped_session_factory.rollback()
            raise
        else:
            await scoped_session_factory.commit()
        finally:
            await scoped_session_factory.remove()

    def sync_session(self) -> Session:
        return self.sync_session_factory()
