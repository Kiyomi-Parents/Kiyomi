from ..services import ServiceUnitOfWork
from kiyomi.error import ErrorArgResolver


class TwitchLoginResolver(ErrorArgResolver[ServiceUnitOfWork, str, str]):
    async def resolve_detailed(self, argument: str) -> str:
        return await self.resolve(argument)

    async def resolve(self, argument: str) -> str:
        return f"{argument}"

    @property
    def arg_name(self) -> str:
        return "twitch_login"
