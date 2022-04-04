import traceback
import typing
from typing import TypeVar

from discord import ApplicationContext, DiscordException, ApplicationCommandInvokeError, Bot
from pyee import AsyncIOEventEmitter

from src.cogs.errors import NoPrivateMessagesException
from .utils import Utils
from .database import Database
from src.log import Logger
from .errors import BadArgument, CogException

TCog = TypeVar('TCog')


class Kiyomi(Bot):
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

    async def on_application_command_error(self, context: ApplicationContext, exception: DiscordException) -> None:
        Logger.log("Global Exception", f"Got error {type(exception)}: {exception}")

        if isinstance(exception, ApplicationCommandInvokeError):
            if isinstance(exception.original, CogException):
                return

            if isinstance(exception.original, BadArgument):
                await context.respond(str(exception.original))
                return

        await self.send_dm_with_stacktrace(context, exception)
        await context.respond("Something went horribly wrong, Kiyomi has fallen out of her box!")
        raise exception

    async def send_dm_with_stacktrace(self, context: ApplicationContext, exception: DiscordException):
        await self.is_owner(context.author)  # populates self.owner_ids or self.owner_id

        stacktrace = \
            ''.join(traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))

        text = f"```python\n{stacktrace}```"

        send_list = []

        if self.owner_ids:
            for owner_id in self.owner_ids:
                owner = await self.fetch_user(owner_id)
                send_list.append(owner)
        elif self.owner_id is not None:
            owner = await self.fetch_user(self.owner_id)
            send_list.append(owner)

        for owner in send_list:
            if len(text) > 2000:
                await owner.send(file=Utils.text_to_file(stacktrace, "tmp_stacktrace.py"))
            else:
                await owner.send(text)

    def get_cog_api(self, cog_type: typing.Type[TCog]) -> TCog:
        cog = self.get_cog(cog_type.__name__)

        if not isinstance(cog, cog_type):
            raise TypeError(f"Expected cog type {cog_type.__name__}, but got {type(cog)}")

        return typing.cast(TCog, cog)
