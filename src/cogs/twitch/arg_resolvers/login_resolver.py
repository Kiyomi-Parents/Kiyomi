from src.kiyomi.error.error_arg_resolver import TArg, TReturn
from src.kiyomi.error import ErrorArgResolver


class TwitchLoginResolver(ErrorArgResolver[str, str]):
    async def resolve_detailed(self, argument: TArg) -> TReturn:
        return await self.resolve(argument)

    async def resolve(self, argument: str) -> str:
        return f"{argument}"

    @property
    def arg_name(self) -> str:
        return "twitch_login"
