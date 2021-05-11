# good bot.py
import os

from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from dotenv import load_dotenv

from src.commands.beatsaber import BeatSaber
from src.commands.errors import NoPrivateMessages
from src.log import Logger
from src.storage.uow import UnitOfWork
from src.tasks import Tasks

client = commands.Bot('!')


@client.event
async def on_ready():
    Logger.log_add(f'{client.user} has connected to Discord!')


@client.check
async def global_block_dms(ctx):
    if ctx.guild is None:
        raise NoPrivateMessages("no")

    return True


@client.check
async def global_db_guild(ctx):
    db_guild = uow.guild_repo.get_guild_by_discord_id(ctx.guild.id)

    if db_guild is None:
        uow.guild_repo.add_guild(ctx.guild)

    return True


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send_help(ctx.command)
        await ctx.send(error)
    elif isinstance(error, NoPrivateMessages):
        await ctx.send(error)
    else:
        await ctx.send(f"Something went horribly wrong, check console!")
        raise error


if __name__ == '__main__':
    uow = UnitOfWork(client)
    tasks = Tasks(uow)
    Logger.log_init()

    # tasks.update_players.start()
    # tasks.update_all_player_roles.start()
    # tasks.update_players_scores.start()
    # tasks.send_notifications.start()
    client.add_cog(BeatSaber(uow, tasks))

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)
