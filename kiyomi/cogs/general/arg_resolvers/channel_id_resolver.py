from ..services import ServiceUnitOfWork
from kiyomi.error import ErrorArgResolver


class ChannelIdResolver(ErrorArgResolver[ServiceUnitOfWork, int, str]):
    async def resolve_detailed(self, argument: int) -> str:
        channel = await self.service_uow.channels.get_by_id(argument)

        if channel is None:
            return f"{argument} (Not in DB)"

        return f"{channel}"

    async def resolve(self, argument: int) -> str:
        channel = await self.service_uow.channels.get_by_id(argument)

        if channel is None:
            return f"{argument}"

        return f"{channel.name}"

    @property
    def arg_name(self) -> str:
        return "channel_id"
