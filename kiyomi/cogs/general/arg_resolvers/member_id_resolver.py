from ..services import ServiceUnitOfWork
from kiyomi.error import ErrorArgResolver


class MemberIdResolver(ErrorArgResolver[ServiceUnitOfWork, int, str]):
    async def resolve_detailed(self, argument: int) -> str:
        member = await self.service_uow.members.get_by_id(argument)
        if member is not None:
            return f"{member}"

        discord_user = await self.service_uow.members.find_discord_user(argument)
        if discord_user is not None:
            return f"{discord_user.display_name} ({discord_user.id})"

        return f"{argument} (Not found)"

    async def resolve(self, argument: int) -> str:
        member = await self.service_uow.members.get_by_id(argument)
        if member is not None:
            return f"{member.name}"

        discord_user = await self.service_uow.members.find_discord_user(argument)
        if discord_user is not None:
            return f"{discord_user.display_name}"

        return f"{argument}"

    @property
    def arg_name(self) -> str:
        return "member_id"
