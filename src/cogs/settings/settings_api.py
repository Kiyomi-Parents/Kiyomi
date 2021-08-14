from typing import Optional

from discord.ext import commands

from .actions import Actions
from .storage.uow import UnitOfWork


class SettingsAPI(commands.Cog):

    def __init__(self, uow: UnitOfWork, actions: Actions):
        self.uow = uow
        self.actions = actions

    def set(self, guild_id: int, name: str, value: any) -> None:
        self.actions.set(guild_id, name, value)

    def get(self, guild_id: int, name: str) -> Optional[any]:
        return self.actions.get_value(guild_id, name)

    def delete(self, guild_id: int, name: str) -> None:
        self.actions.delete(guild_id, name)
