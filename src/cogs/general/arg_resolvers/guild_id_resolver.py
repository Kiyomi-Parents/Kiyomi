from ..storage.storage_unit_of_work import StorageUnitOfWork
from src.kiyomi.error import ErrorArgResolver


class GuildIdResolver(ErrorArgResolver[str, str]):
    def __init__(self, uow: StorageUnitOfWork):
        self.uow = uow

    async def resolve_detailed(self, argument: str) -> str:
        guild = await self.uow.guilds.get_by_id(argument)

        if guild is None:
            return f"{argument} (Not in DB)"

        return f"{guild}"

    async def resolve(self, argument: str) -> str:
        guild = await self.uow.guilds.get_by_id(argument)

        if guild is None:
            return f"{argument}"

        return f"{guild.name}"

    @property
    def arg_name(self) -> str:
        return "guild_id"
