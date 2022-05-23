from src.kiyomi.error.error_arg_resolver import TArg, TReturn
from src.kiyomi.error import ErrorArgResolver


class TwitchUserIdResolver(ErrorArgResolver[str, str]):
    async def resolve_detailed(self, argument: TArg) -> TReturn:
        return await self.resolve(argument)

    async def resolve(self, argument: int) -> str:
        return f"{argument}"

    @property
    def arg_name(self) -> str:
        return "twitch_user_id"
