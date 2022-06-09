from typing import Type, Optional, List

from .persistent_view import PersistentView
from src.kiyomi import Utils, Kiyomi
from ...errors import MissingPersistentViewClass


class Persistence:
    def __init__(
        self,
        guild_id: int,
        channel_id: int,
        message_id: int,
        view: str,
        *view_parameters: str,
    ):
        self.guild_id = guild_id
        self.message_id = message_id
        self.channel_id = channel_id
        self.view = view
        self._view_parameters = [item for item in list(view_parameters) if item is not None]

    @property
    def view_class(self) -> Type[PersistentView]:
        persistent_views = Utils.class_inheritors(PersistentView)

        for persistent_view in persistent_views:
            if persistent_view.__name__ == self.view:
                return persistent_view

        raise MissingPersistentViewClass(self.view, persistent_views)

    async def get_view(self, bot: Kiyomi) -> PersistentView:
        return await self.view_class.deserialize_persistence(bot, self)

    def get_params(self) -> List[Optional[str]]:
        return self._view_parameters

    def get_param(self, index: int) -> Optional[str]:
        if len(self._view_parameters) <= index or index < 0:
            return None

        return self._view_parameters[index]

    def __str__(self):
        return f"Persistence {self.view}({','.join(self._view_parameters)}) ({self.message_id})"
