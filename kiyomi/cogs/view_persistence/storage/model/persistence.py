import logging
from datetime import datetime
from typing import Type, Optional, List

import timeago

from .persistent_view import PersistentView
from kiyomi import Utils, Kiyomi
from ...errors import MissingPersistentViewClass, FailedToLoadPersistentView

_logger = logging.getLogger(__name__)

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
        try:
            start_time = datetime.now()
            view = await self.view_class.deserialize_persistence(bot, self)
            end_time = datetime.now()
            _logger.info(self, f"Finished loading in {timeago.format(end_time, start_time, locale='en_short')}")

            return view
        except Exception as error:
            raise FailedToLoadPersistentView(self) from error

    def get_params(self) -> List[Optional[str]]:
        return self._view_parameters

    def get_param(self, index: int) -> Optional[str]:
        if len(self._view_parameters) <= index or index < 0:
            return None

        return self._view_parameters[index]

    def __str__(self):
        return f"Persistence {self.view}({','.join(self._view_parameters)}) ({self.message_id})"
