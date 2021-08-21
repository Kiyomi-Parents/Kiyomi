from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, BadArgument, NotOwner, MissingPermissions
from pyee import AsyncIOEventEmitter

from src.cogs.errors import NoPrivateMessagesException
from src.database import Database
from src.log import Logger


class Kiyomi(commands.Bot):
    running_tests = False
    events = AsyncIOEventEmitter()
    running_tasks = []
    activity_list = ["Sleeping", "Sitting in a tiny box", "Chilling @ Smugle Stick"]

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

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.CommandNotFound):
            return

        if isinstance(exception, MissingRequiredArgument):
            await context.send_help(context.command)
            await context.send(exception)
        elif isinstance(exception, NoPrivateMessagesException):
            await context.send(exception)
        elif isinstance(exception, BadArgument):
            await context.send("I don't understand what you're trying to do (bad argument)")
        elif isinstance(exception, NotOwner):
            await context.send("Only the bot owner can use this command!")
        elif isinstance(exception, MissingPermissions):
            await context.send(exception)
        else:
            await context.send("Something went horribly wrong, check console!")
            raise exception
