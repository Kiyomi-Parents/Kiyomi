# good bot.py
import os
import re

from discord.ext import tasks, commands
from dotenv import load_dotenv

from src.log import Logger
from src.storage.uow import UnitOfWork
from src.tasks import Tasks

client = commands.Bot('!')


@client.event
async def on_ready():
    Logger.log_add(f'{client.user} has connected to Discord!')


async def format_error_message(message):
    await message.channel.send('Sorry, something went wrong! Make sure your message is in the correct format.')


@client.event
async def on_message(message):
    guild = uow.guild_repo.get_guild_by_id(message.channel.guild.id)

    if guild is None:
        uow.guild_repo.add_guild(message.channel.guild)

    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello there!')

    if message.content.startswith('!help'):
        pattern = re.compile(r'!help *(\w*)')
        match = re.match(pattern, message.content)

        if match:
            action = match.group(1)
            await help_func(message, action)

    if message.content.startswith('!player'):
        pattern = re.compile(r"!player *(\w+) (<@!(\d+)>)? *(https?://scoresaber\.com/u/)?(\d{17})")
        match = re.match(pattern, message.content)

        if match:
            action = match.group(1)
            discord_user_id = match.group(3)
            player_id = str(match.group(5))

            await player_func(message.channel.guild.id, player_id, discord_user_id, message, action)
        else:
            await format_error_message(message)

    # SECURITY
    if not await can_execute(message):
        return

    if message.content.startswith("!feature"):
        pattern = re.compile(r'!feature *(\w+) *(\w+)')
        match = re.match(pattern, message.content)

        if match:
            action = match.group(1)
            feature_flag = match.group(2)

            await enable_feature(message, action, feature_flag)

    if message.content.startswith('!channel'):
        pattern = re.compile(r'!channel *(\w+)')
        match = re.match(pattern, message.content)

        if match:
            action = match.group(1)
            await channel_func(message.channel.id, message.channel.guild.id, message, action)
        else:
            await format_error_message(message)

    if message.content.startswith("!update"):
        pattern = re.compile(r'!update *(\w+)')
        match = re.match(pattern, message.content)

        if match:
            action = match.group(1)
            await run_task(message.channel.guild, action)
        else:
            await run_task(message.channel.guild)


async def help_func(message, action):
    Logger.log_add(f'help_func(action: {action})')
    if action == "69":
        await message.channel.send('420')
    elif action == "ayy":
        await message.channel.send("lmao")
    else:
        m1 = '**To add/remove player:**\n`!player add/remove <discord user> <ScoreSaber profile url>`\n'
        m2 = '**To add/remove current channel:**\n`!channel add/remove`\n'
        m3 = '**To add/remove another channel in the same Discord server:**\n`!channel add/remove channelID`\n'
        m4 = '**To add/remove feature from Discord server:**\n`!feature add/remove [ppRoles]`'
        m5 = '**To update data:**\n`!update [players/roles/scores/notifications]`'
        msg = m1 + m2 + m3 + m4 + m5
        await message.channel.send(msg)


async def player_func(guild_id, playerID, discord_user_id, message, action):
    Logger.log_add(f'player_func(guild_id: {guild_id}, playerID: {playerID}, discord_user_id: {discord_user_id}, action: {action})')

    db_guild = uow.guild_repo.get_guild_by_id(guild_id)
    db_player = uow.player_repo.get_player_by_player_id(playerID)

    if action == "add":
        if db_player in db_guild.players:
            await message.channel.send(f'Player ID {playerID} has already been added!')
            return

        new_player = uow.scoresaber.get_player(playerID)

        if new_player is None:
            await message.channel.send(f'Failed to add player!')
            return

        if discord_user_id is not None:
            new_player.discord_user_id = discord_user_id
        else:
            new_player.discord_user_id = message.author.id

        uow.player_repo.add_player(new_player)
        uow.player_repo.add_to_guild(new_player.playerId, db_guild)

        # Get player scores and marked them sent to decrease spam
        await tasks.update_player_scores(new_player)
        await tasks.mark_all_player_scores_sent(new_player)

        # Add role to player if enabled
        if db_guild.pp_roles:
            await tasks.update_player_roles(db_guild, new_player)

        await message.channel.send(f'Player {new_player.playerName} successfully added!')
    elif action == "remove":
        is_removed = False

        for db_player in db_guild.players:
            if playerID == db_player.playerId:
                uow.guild_repo.remove_player(db_guild.discord_guild_id, db_player)
                await tasks.remove_player_roles(db_guild, db_player)
                await message.channel.send(f'Player ID {playerID} successfully removed!')
                is_removed = True

        if not is_removed:
            await message.channel.send(f"Player ID {playerID} already doesn't exist in this Discord server's player list.")


async def channel_func(channel_id, guild_id, message, action):
    Logger.log_add(f'channel_func(channel: {channel_id}, guild: {guild_id}, action: {action})')
    db_guild = uow.guild_repo.get_guild_by_id(guild_id)

    if action == "add":
        if db_guild.recent_scores_channel_id is not None:
            await message.channel.send(f'Channel ID {message.channel.name} ({channel_id}) has already been added!')
            return

        uow.guild_repo.set_recent_score_channel_id(guild_id, channel_id)

        await tasks.mark_all_guild_scores_sent(db_guild)

        await message.channel.send(f'Channel ID {message.channel.name} ({channel_id}) successfully added!')
    elif action == "remove":
        if db_guild.recent_scores_channel_id is None:
            await message.channel.send(f"Channel ID {message.channel.name} ({channel_id}) already doesn't exist in the channel list for server {client.get_guild(guild_id)}.")

        uow.guild_repo.set_recent_score_channel_id(guild_id, None)
        await message.channel.send(f'Channel ID {message.channel.name} ({channel_id}) successfully removed!')
    else:
        await message.channel.send("Usage: !channel add/remove")


async def enable_feature(message, action, feature_flag):
    guild = message.channel.guild

    if action == "add":
        if feature_flag == "ppRoles":
            uow.guild_repo.set_feature(guild.id, feature_flag, True)
            await tasks.update_all_player_roles(guild)
            await message.channel.send("Enabled pp roles feature")

    elif action == "remove":
        if feature_flag == "ppRoles":
            uow.guild_repo.set_feature(guild.id, feature_flag, False)
            await tasks.remove_guild_roles(guild)
            await message.channel.send("Disabled pp roles feature")
    else:
        await message.channel.send("Usage: !feature add/remove [ppRoles]")


async def run_task(guild, action=None):
    if action == "players":
        await tasks.update_players(guild)
    elif action == "roles":
        await tasks.update_all_player_roles(guild)
    elif action == "scores":
        await tasks.update_players_scores(guild)
    elif action == "notifications":
        await tasks.send_notifications(guild)
    else:
        await tasks.update_players(guild)
        await tasks.update_all_player_roles(guild)
        await tasks.update_players_scores(guild)
        await tasks.send_notifications(guild)


async def can_execute(message):
    if not message.author.guild_permissions.administrator:
        await message.channel.send("You don't have access to this command")
        return False

    return True

if __name__ == '__main__':
    uow = UnitOfWork(client)
    tasks = Tasks(uow)
    Logger.log_init()

    tasks.update_players.start()
    tasks.update_all_player_roles.start()
    tasks.update_players_scores.start()
    tasks.send_notifications.start()

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)
