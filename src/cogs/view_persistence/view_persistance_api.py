from discord.ext import commands

from . import MessageViewService, UnitOfWork
from .errors import MissingPersistentViewClass
from .storage.model.persistence import Persistence
from .view_persistence_cog import ViewPersistenceCog
from src.kiyomi import Kiyomi
from ...log import Logger


class ViewPersistenceAPI(ViewPersistenceCog):
    def __init__(self, bot: Kiyomi, message_view_service: MessageViewService, uow: UnitOfWork):
        super().__init__(bot, message_view_service)

        self.uow = uow

        # Register events
        self.events()

    def events(self):
        @self.bot.events.on("on_new_view_sent")
        async def mark_scores_sent(persistence: Persistence):
            await self.message_view_service.add_persistent_view(persistence)

    @commands.Cog.listener()
    async def on_ready(self):
        persistences = await self.message_view_service.get_persistent_views()

        for persistence in persistences:
            try:
                view = await persistence.get_view(self.bot)
                self.bot.add_view(view=view, message_id=persistence.message_id)
            except MissingPersistentViewClass as error:
                await error.handle()

        Logger.log("View Persistence", f"Loaded {len(persistences)} persistent views")
