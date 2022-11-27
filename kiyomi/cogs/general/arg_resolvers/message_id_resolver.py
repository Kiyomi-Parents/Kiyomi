from ..services import ServiceUnitOfWork
from kiyomi.error import ErrorArgResolver


class MessageIdResolver(ErrorArgResolver[ServiceUnitOfWork, int, str]):
    async def resolve_detailed(self, argument: int) -> str:
        message = await self.service_uow.messages.get_by_id(argument)

        if message is None:
            return f"{argument} (Not in DB)"

        return f"{message}"

    async def resolve(self, argument: int) -> str:
        message = await self.service_uow.messages.get_by_id(argument)

        if message is None:
            return f"{argument}"

        return f"{message.id}"

    @property
    def arg_name(self) -> str:
        return "message_id"
