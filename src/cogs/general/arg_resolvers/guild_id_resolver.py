from ..services import ServiceUnitOfWork
from src.kiyomi.error import ErrorArgResolver


class GuildIdResolver(ErrorArgResolver[ServiceUnitOfWork, str, str]):
    async def resolve_detailed(self, argument: str) -> str:
        guild = await self.service_uow.guilds.get_by_id(argument)

        if guild is None:
            return f"{argument} (Not in DB)"

        return f"{guild}"

    async def resolve(self, argument: str) -> str:
        guild = await self.service_uow.guilds.get_by_id(argument)

        if guild is None:
            return f"{argument}"

        return f"{guild.name}"

    @property
    def arg_name(self) -> str:
        return "guild_id"
