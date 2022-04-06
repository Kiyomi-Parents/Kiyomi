from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.log import Logger

Base = declarative_base()


class Database:
    _engine: AsyncEngine
    _session_maker: sessionmaker

    def __init__(self, connection: str):
        self._connection = connection

    async def init(self):
        self._engine = create_async_engine(self._connection, echo=False, pool_pre_ping=True, pool_recycle=3600)
        self._session_maker = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)

    async def get_session(self) -> AsyncSession:
        return self._session_maker()

    async def create_tables(self):
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

            Logger.log("Database", f"Created {len(Base.metadata.tables)} tables")

    async def drop_tables(self):
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

            Logger.log("Database", f"Dropped all database tables!")
