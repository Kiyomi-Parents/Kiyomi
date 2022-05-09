from ..storage.unit_of_work import UnitOfWork
from src.kiyomi.error import ErrorArgResolver


class EmojiIdResolver(ErrorArgResolver[int, str]):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def resolve_detailed(self, argument: int) -> str:
        emoji = await self.uow.emojis.get_by_id(argument)

        if emoji is None:
            return f"{argument} (Not in DB)"

        return f"{emoji}"

    async def resolve(self, argument: int) -> str:
        emoji = await self.uow.emojis.get_by_id(argument)

        if emoji is None:
            return f"{argument}"

        return f"{emoji.name}"

    @property
    def arg_name(self) -> str:
        return "emoji_id"
