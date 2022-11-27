from typing import Type, TypeVar, Callable, List

from sqlalchemy.ext.asyncio import AsyncSession

from kiyomi import Utils, BaseUnitOfWork

TUow = TypeVar("TUow")


class UnitOfWorkFactory:
    _session: AsyncSession

    def __init__(self, session_maker: Callable[[], AsyncSession]):
        self._session_maker = session_maker

    async def start(self):
        self._session = self._session_maker()

    def find_unit_of_work(self, unit_of_works: List[BaseUnitOfWork], unit_of_work_type: Type[TUow]) -> TUow:
        for unit_of_work in unit_of_works:
            if not isinstance(unit_of_work, unit_of_work_type):
                continue

            return unit_of_work

        raise RuntimeError(f"Could not find correct Unit of Work for type {unit_of_work_type.__name__}")

    async def get_factory(self, unit_of_work_type: Type[TUow]) -> TUow:
        unit_of_works = Utils.class_inheritors(unit_of_work_type)

        unit_of_work = self.find_unit_of_work(unit_of_works, unit_of_work_type)

        return unit_of_work(self._session_maker())
