import logging
from typing import TypeVar, Optional, Type, cast, List

import discord
from discord import Permissions
from discord.app_commands import CommandInvokeError
from discord.ext.commands import Bot, Context, Cog
from pyee import AsyncIOEventEmitter

from .base_cog import BaseCog
from .cogs.errors import NoPrivateMessagesException
from .base_command_tree import BaseCommandTree
from .error import KiyomiException
from .error.error_resolver import ErrorResolver
from .database import Database
from .error.error_utils import handle_global_error

TCog = TypeVar("TCog", bound=BaseCog)
_logger = logging.getLogger(__name__)


class Kiyomi(Bot):
    running_tests = False
    events = AsyncIOEventEmitter()
    default_guild: Optional[discord.Object] = None
    debug_guilds: Optional[List[discord.Object]] = None
    error_resolver = ErrorResolver()

    def __init__(self, *args, db: Database, **kwargs):
        intents = discord.Intents.default()
        intents.members = True
        intents.guilds = True
        intents.message_content = True

        super().__init__(*args, intents=intents, tree_cls=BaseCommandTree, **kwargs)

        self.add_check(self.global_block_dms)
        self.database = db

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        await super(Kiyomi, self).start(token, reconnect=reconnect)
        await self.database.init()

    async def on_ready(self):
        _logger.info(self.user, "Connected to Discord!")

        await self.register_commands()

        _logger.info(self.user, f"I'm ready!")
        _logger.info(self.user, f"Invite url: {self.invite_url}")

    async def on_guild_join(self, guild: discord.Guild):
        _logger.info(self.user, f"Joined new guild {guild}")
        await self.register_guild_commands(guild)

    async def register_commands(self):
        _logger.info(self.user, "Registering commands...")

        for guild in self.guilds:
            await self.register_guild_commands(guild)

        _logger.info(self.user, f"Registering global commands")
        await self.tree.sync()

        _logger.info(self.user, f"Commands registered!")

    async def register_guild_commands(self, guild: discord.Guild):
        # _logger.info(self.user, f"Clearing registered commands for {guild}")
        # # Remove commands from guild
        # self.tree.clear_commands(guild=guild)  # This removes all the commands registered to the guild prior by
        # commands. We shouldn't call this really....
        # IF command is deleted then it should also be deleted from the discord server. which this currently doesnt do
        # await self.tree.sync(guild=guild)

        _logger.info(self.user, f"Registering commands for {guild}")
        # Sync guild only commands
        await self.tree.sync(guild=guild)

    @property
    def invite_url(self) -> str:
        return discord.utils.oauth_url(
            self.user.id,
            permissions=Permissions(
                view_channel=True,
                manage_roles=True,
                send_messages=True,
                embed_links=True,
                attach_files=True,
                add_reactions=True,
                use_external_emojis=True,
                use_external_stickers=True,
                manage_messages=True,
                read_message_history=True,
                read_messages=True,
            ),
            scopes=("bot", "applications.commands"),
        )

    @property
    async def owners(self) -> List[discord.User]:
        await self.is_owner(self.user)  # Hack to populate self.owner_ids or self.owner_id

        if self.owner_ids:
            return [await self.fetch_user(owner_id) for owner_id in self.owner_ids]
        elif self.owner_id is not None:
            return [await self.fetch_user(self.owner_id)]

    @staticmethod
    def global_block_dms(ctx):
        if ctx.guild is None:
            raise NoPrivateMessagesException("no")

        return True

    async def on_command_error(self, context: Context["Kiyomi"], error: Exception) -> None:
        if isinstance(error, CommandInvokeError):
            error = error.original

        if isinstance(error, KiyomiException):
            if error.is_handled:
                return
            else:
                return await error.handle(ctx=context.interaction)

        await handle_global_error(self, error, ctx=context)

    # When using, please close database session. UI cogs don't need to be closed
    # or use: async with self.bot.get_cog("SomeCog") as some_cog_api:
    def get_cog(self, name: str, /) -> Cog:
        cog = super().get_cog(name)

        if cog is None:
            raise TypeError(f"Expected cog type {name}, but got {type(cog)}")

        return cog

    # When using, please close database session. UI cogs don't need to be closed
    # or use: async with self.bot.get_cog_api("SomeCog") as some_cog_api:
    def get_cog_api(self, cog_type: Type[TCog]) -> TCog:
        cog = self.get_cog(cog_type.__name__)

        if not isinstance(cog, cog_type):
            raise TypeError(f"Expected cog type {cog_type.__name__}, but got {type(cog)}")

        return cast(TCog, cog)
