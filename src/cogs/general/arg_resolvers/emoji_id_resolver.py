from ..services import ServiceUnitOfWork
from src.kiyomi.error import ErrorArgResolver


class EmojiIdResolver(ErrorArgResolver[ServiceUnitOfWork, int, str]):
    async def resolve_detailed(self, argument: int) -> str:
        emoji = await self.service_uow.emojis.get_by_id(argument)

        if emoji is None:
            return f"{argument} (Not in DB)"

        return f"{emoji}"

    async def resolve(self, argument: int) -> str:
        emoji = await self.service_uow.emojis.get_by_id(argument)

        if emoji is None:
            return f"{argument}"

        return f"{emoji.name}"

    @property
    def arg_name(self) -> str:
        return "emoji_id"
