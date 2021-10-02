from typing import Optional

from discord.ext import commands

from .actions import Actions
from .errors import SongNotFound
from .storage.model import Beatmap
from .storage.uow import UnitOfWork
from src.log import Logger


class BeatSaverAPI(commands.Cog):
    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

    async def get_beatmap_by_key(self, key: str) -> Optional[Beatmap]:
        try:
            return await self.actions.get_beatmap_by_key(key)
        except SongNotFound as error:
            Logger.log(self.__class__.__name__, error)
            return None
