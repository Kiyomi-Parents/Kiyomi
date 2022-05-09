from typing import TypeVar, Optional, Type, cast, List

import discord
from discord import Permissions
from discord.app_commands import CommandInvokeError
from discord.ext.commands import Bot, Context
from pyee import AsyncIOEventEmitter

from src.cogs.errors import NoPrivateMessagesException
from .base_command_tree import BaseCommandTree
from .error import KiyomiException
from .error.error_resolver import ErrorResolver
from .database import Database
from src.log import Logger
from .error.error_utils import handle_global_error

TCog = TypeVar('TCog')


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
        Logger.log(self.user, "Connected to Discord!")

        await self.register_commands()

        Logger.log(self.user, f"I'm ready!")
        Logger.log(self.user, f"Invite url: {self.invite_url}")

    async def on_guild_join(self, guild: discord.Guild):
        Logger.log(self.user, f"Joined new guild {guild}")
        await self.register_guild_commands(guild)

    async def register_commands(self):
        Logger.log(self.user, "Registering commands...")

        for guild in self.guilds:
            await self.register_guild_commands(guild)

        Logger.log(self.user, f"Registering global commands")
        await self.tree.sync()

        Logger.log(self.user, f"Commands registered!")

    async def register_guild_commands(self, guild: discord.Guild):
        # Logger.log(self.user, f"Clearing registered commands for {guild}")
        # # Remove commands from guild
        # self.tree.clear_commands(guild=guild)  # This removes all the commands registered to the guild prior by
        # commands. We shouldn't call this really....
        # IF command is deleted then it should also be deleted from the discord server. which this currently doesnt do
        # await self.tree.sync(guild=guild)

        Logger.log(self.user, f"Registering commands for {guild}")
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
                        read_messages=True
                ),
                scopes=('bot', 'applications.commands')
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

    def get_cog_api(self, cog_type: Type[TCog]) -> TCog:
        await handle_global_error(self, error, ctx=context)

    def get_cog(self, name: str, /) -> TCog:
        cog = super().get_cog(name)

        if cog is None:
            raise TypeError(f"Expected cog type {name}, but got {type(cog)}")

        return cog

    def get_cog_api(self, cog_type: Type[TCog]) -> TCog:
        cog = self.get_cog(cog_type.__name__)

        if not isinstance(cog, cog_type):
            raise TypeError(f"Expected cog type {cog_type.__name__}, but got {type(cog)}")

        return cast(TCog, cog)
