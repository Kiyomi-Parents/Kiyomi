import traceback
import typing
from typing import TypeVar

from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, BadArgument, NotOwner, MissingPermissions, Context
from pyee import AsyncIOEventEmitter

from src.cogs.errors import NoPrivateMessagesException
from src.database import Database
from src.log import Logger

TCog = TypeVar('TCog')


class Kiyomi(commands.Bot):
    running_tests = False
    events = AsyncIOEventEmitter()
    running_tasks = []
    activity_list = ["Sleeping", "Sitting in a tiny box", "Chilling @ Smugle Stick", "Drinking wine"]

    def __init__(self, *args, db: Database, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_check(self.global_block_dms)
        self.database = db

    async def on_ready(self):
        Logger.log(self.user.name, "Connected to Discord!")

    @staticmethod
    def global_block_dms(ctx):
        if ctx.guild is None:
            raise NoPrivateMessagesException("no")

        return True

    async def on_command_error(self, context: Context, exception):
        if isinstance(exception, commands.CommandNotFound):
            return
        if isinstance(exception, MissingRequiredArgument):
            await context.send_help(context.command)
            await context.send(str(exception))
        elif isinstance(exception, NoPrivateMessagesException):
            await context.send(str(exception))
        elif isinstance(exception, BadArgument):
            await context.send("I don't understand what you're trying to do (bad argument)")
        elif isinstance(exception, NotOwner):
            await context.send("Only the bot owner can use this command!")
        elif isinstance(exception, MissingPermissions):
            await context.send(str(exception))
        else:
            await self.send_dm_with_stacktrace(context, exception)
            await context.send("Something went horribly wrong, check console!")
            raise exception

    async def send_dm_with_stacktrace(self, context: Context, exception):
        await self.is_owner(context.author)  # populates self.owner_ids or self.owner_id

        stacktrace = \
            ''.join(traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))

        if self.owner_ids:
            for owner_id in self.owner_ids:
                owner = await self.fetch_user(owner_id)
                await owner.send(f"```python\n{stacktrace}```")
        elif self.owner_id is not None:
            owner = await self.fetch_user(self.owner_id)
            await owner.send(f"```python\n{stacktrace}```")

    def get_cog_api(self, cog_type: typing.Type[TCog]) -> TCog:
        cog = self.get_cog(cog_type.__name__)

        if not isinstance(cog, cog_type):
            raise TypeError(f"Expected cog type {cog_type.__name__}, but got {type(cog)}")

        return typing.cast(TCog, cog)
