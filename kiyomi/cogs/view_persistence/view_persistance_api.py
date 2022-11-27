import logging

from discord.ext import commands

from .services import ServiceUnitOfWork
from .errors import MissingPersistentViewClass
from .storage.model.persistence import Persistence
from kiyomi import BaseCog

_logger = logging.getLogger(__name__)


class ViewPersistenceAPI(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        @self.bot.events.on("on_new_view_sent")
        async def mark_scores_sent(persistence: Persistence):
            await self._service_uow.message_views.add_persistent_view(persistence)
            await self._service_uow.save_changes()
            await self._service_uow.close()

    @commands.Cog.listener()
    async def on_ready(self):
        persistences = await self._service_uow.message_views.get_persistent_views()

        for persistence in persistences:
            try:
                view = await persistence.get_view(self.bot)
                self.bot.add_view(view=view, message_id=persistence.message_id)
            except MissingPersistentViewClass as error:
                await error.handle()

        _logger.info("View Persistence", f"Loaded {len(persistences)} persistent views")
        await self._service_uow.close()
