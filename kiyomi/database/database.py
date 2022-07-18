import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_logger = logging.getLogger(__name__)
Base: declarative_base = declarative_base()


class Database:
    _engine: AsyncEngine
    _session_maker: sessionmaker
    session: AsyncSession

    def __init__(self, connection: str):
        self._connection = connection

    async def init(self):
        self._engine = create_async_engine(self._connection, echo=False, pool_size=20, max_overflow=10,
                                           pool_pre_ping=True, pool_recycle=3600)
        self._session_maker = sessionmaker(self._engine, class_=AsyncSession, expire_on_commit=False)

        # Don't change, this just works
        self.session = async_scoped_session(self._session_maker, scopefunc=asyncio.current_task)

    async def create_tables(self):
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

            Logger.log("Database", f"Created {len(Base.metadata.tables)} tables")

    async def drop_tables(self):
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

            Logger.log("Database", f"Dropped all database tables!")
