from ..services import ServiceUnitOfWork
from src.kiyomi.error import ErrorArgResolver


class PlayerIdResolver(ErrorArgResolver[ServiceUnitOfWork, str, str]):
    async def resolve_detailed(self, argument: str) -> str:
        player = await self.service_uow.players.get_by_id(argument)

        if player is None:
            return f"{argument} (Not in DB)"

        return f"{player}"

    async def resolve(self, argument: str) -> str:
        player = await self.service_uow.players.get_by_id(argument)

        if player is None:
            return f"{argument}"

        return f"{player.name}"

    @property
    def arg_name(self) -> str:
        return "player_id"
