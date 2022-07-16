from ..services import ServiceUnitOfWork
from kiyomi.error import ErrorArgResolver


class MemberIdResolver(ErrorArgResolver[ServiceUnitOfWork, int, str]):
    async def resolve_detailed(self, argument: int) -> str:
        member = await self.service_uow.members.get_by_id(argument)

        if member is None:
            return f"{argument} (Not in DB)"

        return f"{member}"

    async def resolve(self, argument: int) -> str:
        member = await self.service_uow.members.get_by_id(argument)

        if member is None:
            return f"{argument}"

        return f"{member.name}"

    @property
    def arg_name(self) -> str:
        return "member_id"
