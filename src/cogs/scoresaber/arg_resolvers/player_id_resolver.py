from src.kiyomi.error.error_arg_resolver import TArg, TReturn
from ..storage.unit_of_work import UnitOfWork
from src.kiyomi.error import ErrorArgResolver


class PlayerIdResolver(ErrorArgResolver[str, str]):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def resolve_detailed(self, argument: TArg) -> TReturn:
        player = await self.uow.players.get_by_id(argument)

        if player is None:
            return f"{argument} (Not in DB)"

        return f"{player}"

    async def resolve(self, argument: str) -> str:
        player = await self.uow.players.get_by_id(argument)

        if player is None:
            return f"{argument}"

        return f"{player.name}"

    @property
    def arg_name(self) -> str:
        return "player_id"
