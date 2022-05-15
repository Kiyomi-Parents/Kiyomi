from sqlalchemy.ext.asyncio import AsyncSession

from src.kiyomi import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
