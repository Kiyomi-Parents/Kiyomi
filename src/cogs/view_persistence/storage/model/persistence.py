from typing import Type

from .persistent_view import PersistentView
from src.kiyomi import Utils, Kiyomi


class Persistence:
    def __init__(self, guild_id: int, channel_id: int, message_id: int, view: str, *view_parameters: str):
        self.guild_id = guild_id
        self.message_id = message_id
        self.channel_id = channel_id
        self.view = view
        self.view_parameters = list(view_parameters)

    @property
    def view_class(self) -> Type[PersistentView]:
        persistent_views = Utils.class_inheritors(PersistentView)

        for persistent_view in persistent_views:
            if persistent_view.__name__ == self.view:
                return persistent_view

        raise RuntimeError(f"Could not locate class {self.view} among {', '.join([persistent_view.__name__ for persistent_view in persistent_views])}")

    async def get_view(self, bot: Kiyomi) -> PersistentView:
        return await self.view_class.deserialize_persistence(bot, self)

    def __str__(self):
        return f"Persistence {self.view}({','.join(self.view_parameters)}) ({self.message_id})"
