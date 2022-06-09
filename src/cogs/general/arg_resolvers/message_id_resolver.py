from ..storage.storage_unit_of_work import StorageUnitOfWork
from src.kiyomi.error import ErrorArgResolver


class MessageIdResolver(ErrorArgResolver[int, str]):
    def __init__(self, uow: StorageUnitOfWork):
        self.uow = uow

    async def resolve_detailed(self, argument: int) -> str:
        message = await self.uow.messages.get_by_id(argument)

        if message is None:
            return f"{argument} (Not in DB)"

        return f"{message}"

    async def resolve(self, argument: int) -> str:
        message = await self.uow.messages.get_by_id(argument)

        if message is None:
            return f"{argument}"

        return f"{message.id}"

    @property
    def arg_name(self) -> str:
        return "message_id"
