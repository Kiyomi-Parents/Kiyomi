from ..storage.unit_of_work import UnitOfWork
from src.kiyomi.error import ErrorArgResolver


class PlayerIdResolver(ErrorArgResolver[str, str]):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def resolve(self, argument: str) -> str:
        player = self.uow.players.get_by_id(argument)

        if player is None:
            return f"{argument}"

        return f"{player.name} ({player.id})"

    @property
    def arg_name(self) -> str:
        return "player_id"
