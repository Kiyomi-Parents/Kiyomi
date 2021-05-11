# good bot.py
import os
import re

from discord.ext import tasks, commands
from dotenv import load_dotenv

from src.log import Logger
from src.storage.uow import UnitOfWork
from src.tasks import Tasks
from src.commands import Commands

client = commands.Bot('!')


@client.event
async def on_ready():
    Logger.log_add(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    guild = uow.guild_repo.get_guild_by_id(message.channel.guild.id)

    if guild is None:
        uow.guild_repo.add_guild(message.channel.guild)

    if message.author == client.user:
        return

    pattern = re.compile(r'!(\w+) *(\S*) *(\S*) *(\S*)')
    
    if message.content.startswith('!'):
        match = re.match(pattern, message.content)
        if match:
            try:
                command_msg, *args = [match.group(i+1) for i in range(3) if bool(match.group(i+1))]
                await commandobject.command(message, command_msg, args)
            except Exception as e:
                Logger.log_add(f'Exception in on_message, message.content: {message.content}, exception: {e}')
                await message.channel.send('Sorry, an error occurred')


if __name__ == '__main__':
    uow = UnitOfWork(client)
    tasks = Tasks(uow)
    Logger.log_init()

    tasks.update_players.start()
    tasks.update_all_player_roles.start()
    tasks.update_players_scores.start()
    tasks.send_notifications.start()
    commandobject = Commands(uow, tasks)

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)
