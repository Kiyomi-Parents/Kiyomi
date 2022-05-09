from ..storage.unit_of_work import UnitOfWork
from src.kiyomi.error import ErrorArgResolver


class MemberIdResolver(ErrorArgResolver[int, str]):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def resolve_detailed(self, argument: int) -> str:
        member = self.uow.members.get_by_id(argument)

        if member is None:
            return f"{argument} (Not in DB)"

        return f"{member}"

    async def resolve(self, argument: int) -> str:
        member = self.uow.members.get_by_id(argument)

        if member is None:
            return f"{argument}"

        return f"{member.name}"

    @property
    def arg_name(self) -> str:
        return "member_id"
