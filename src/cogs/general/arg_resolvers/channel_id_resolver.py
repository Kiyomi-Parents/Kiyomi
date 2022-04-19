from ..storage.unit_of_work import UnitOfWork
from src.kiyomi.error import ErrorArgResolver


class ChannelIdResolver(ErrorArgResolver[int, str]):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def resolve_detailed(self, argument: int) -> str:
        channel = self.uow.channels.get_by_id(argument)

        if channel is None:
            return f"{argument} (Not in DB)"

        return f"{channel}"

    async def resolve(self, argument: int) -> str:
        channel = self.uow.channels.get_by_id(argument)

        if channel is None:
            return f"{argument}"

        return f"{channel.name}"

    @property
    def arg_name(self) -> str:
        return "channel_id"
