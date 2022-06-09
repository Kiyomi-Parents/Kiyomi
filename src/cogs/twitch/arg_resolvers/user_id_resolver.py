from typing import Optional

from twitchio import User

from ..services import ServiceUnitOfWork
from ..errors import BroadcasterNotFound
from ..storage.model.twitch_broadcaster import TwitchBroadcaster
from src.kiyomi.error import ErrorArgResolver


class TwitchUserIdResolver(ErrorArgResolver[str, str]):
    def __init__(self, service_uow: ServiceUnitOfWork):
        self.service_uow = service_uow

    async def resolve_detailed(self, argument: int, detailed: bool = True) -> str:
        user: Optional[TwitchBroadcaster] = await self.service_uow.twitch_broadcasters.get_by_id(argument)
        if user is not None:
            return f"{user}"

        try:
            user: User = await self.service_uow.twitch_broadcasters.fetch_user(user_id=argument)
            return f"{user}" + " (Not in DB)" * detailed
        except BroadcasterNotFound:
            return "Twitch user with ID " * detailed + f"{argument}" + " (Not found in DB nor on Twitch)" * detailed

    async def resolve(self, argument: int) -> str:
        return await self.resolve_detailed(argument, False)

    @property
    def arg_name(self) -> str:
        return "twitch_user_id"
