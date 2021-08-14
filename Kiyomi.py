import os

from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from discord.ext.commands.errors import BadArgument
from dotenv import load_dotenv
from pymitter import EventEmitter
from sqlalchemy import create_engine

from src.cogs.errors import NoPrivateMessagesException
from src.database import Database
from src.log import Logger


class Kiyomi(commands.Bot):
    running_tests = False
    events = EventEmitter()

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
        else:
            await context.send("Something went horribly wrong, check console!")
            raise exception


if __name__ == "__main__":
    # Init database
    database = Database(create_engine("sqlite:///bot.db", echo=False))

    bot = Kiyomi(command_prefix="!", db=database)

    Logger.log_init()

    bot.load_extension(name="src.cogs.general")
    bot.load_extension(name="src.cogs.settings")
    bot.load_extension(name="src.cogs.scoresaber")
    bot.load_extension(name="src.cogs.beatsaver")
    bot.load_extension(name="src.cogs.score_feed")
    bot.load_extension(name="src.cogs.leaderboard")
    bot.load_extension(name="src.cogs.achievements")
    bot.load_extension(name="src.cogs.achievement_roles")

    database.create_tables()
    # database.create_schema_image()

    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)
