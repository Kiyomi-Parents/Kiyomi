# good bot.py
import os
import re

from discord.ext import tasks, commands
from dotenv import load_dotenv

from src.log import Logger
from src.storage.uow import UnitOfWork
from src.tasks import Tasks
from src.commands import BeatSaber

client = commands.Bot('!')


@client.event
async def on_ready():
    Logger.log_add(f'{client.user} has connected to Discord!')

if __name__ == '__main__':
    uow = UnitOfWork(client)
    tasks = Tasks(uow)
    Logger.log_init()

    tasks.update_players.start()
    tasks.update_all_player_roles.start()
    tasks.update_players_scores.start()
    tasks.send_notifications.start()
    client.add_cog(BeatSaber(uow, tasks, client))

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)
