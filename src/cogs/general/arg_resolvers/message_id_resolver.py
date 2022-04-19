from ..storage.unit_of_work import UnitOfWork
from src.kiyomi.error import ErrorArgResolver


class MessageIdResolver(ErrorArgResolver[int, str]):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def resolve_detailed(self, argument: int) -> str:
        message = self.uow.messages.get_by_id(argument)

        if message is None:
            return f"{argument} (Not in DB)"

        return f"{message}"

    async def resolve(self, argument: int) -> str:
        message = self.uow.messages.get_by_id(argument)

        if message is None:
            return f"{argument}"

        return f"{message.id}"

    @property
    def arg_name(self) -> str:
        return "message_id"
