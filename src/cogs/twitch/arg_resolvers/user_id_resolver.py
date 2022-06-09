from typing import Optional

from ..services.twitch_broadcaster_service import BroadcasterService
from ..errors import BroadcasterNotFound
from ..storage.model.twitch_broadcaster import TwitchBroadcaster
from ..storage.unit_of_work import UnitOfWork
from src.kiyomi.error import ErrorArgResolver

from twitchio import User


class TwitchUserIdResolver(ErrorArgResolver[str, str]):
    def __init__(self, uow: UnitOfWork, broadcaster_service: BroadcasterService):
        self.uow = uow
        self.broadcaster_service = broadcaster_service

    async def resolve_detailed(self, argument: int, detailed: bool = True) -> str:
        user: Optional[TwitchBroadcaster] = await self.uow.twitch_broadcasters.get_by_id(argument)
        if user is not None:
            return f"{user}"

        try:
            user: User = await self.broadcaster_service.fetch_user(user_id=argument)
            return f"{user}" + \
                   " (Not in DB)" * detailed
        except BroadcasterNotFound:
            return "Twitch user with ID " * detailed + \
                   f"{argument}" + \
                   " (Not found in DB nor on Twitch)" * detailed

    async def resolve(self, argument: int) -> str:
        return await self.resolve_detailed(argument, False)

    @property
    def arg_name(self) -> str:
        return "twitch_user_id"
