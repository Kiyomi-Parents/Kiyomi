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

async def invalid_command(message, args=False):
    await message.channel.send('Sorry, something went wrong! Make sure your message is in the correct format.')

async def hello(message, args=False):
    await message.channel.send('Hello there!')

async def help_func(message, args=False):
    Logger.log_add(f'help_func()')
    m1 = '**To add/remove player:**\n`!player add/remove <ScoreSaber profile url/id> <discord user>`\n'
    m2 = '**To add/remove current channel:**\n`!channel add/remove`\n'
    m3 = '**To add/remove feature from Discord server:**\n`!feature add/remove [ppRoles]`\n'
    m4 = '**To update data:**\n`!update [players/roles/scores/notifications]`'
    msg = m1 + m2 + m3 + m4
    await message.channel.send(msg)

async def player_func(message, args):
    Logger.log_add(f'player_func(message.content: {message.content}, args: {args})')

    async def add_player():
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
    
    async def remove_player():
        is_removed = False

        for db_player in db_guild.players:
            if playerID == db_player.playerId:
                uow.guild_repo.remove_player(db_guild.discord_guild_id, db_player)
                await tasks.remove_player_roles(db_guild, db_player)
                await message.channel.send(f'Player ID {playerID} successfully removed!')
                is_removed = True

        if not is_removed:
            await message.channel.send(f"Player ID {playerID} already doesn't exist in this Discord server's player list.")


    actiondict = {
        "add": add_player,
        "remove": remove_player
    }
    action = args[0]
    actionfunc = actiondict.get(action, False)
    if not actionfunc:
        message.channel.send(f'{action} is not an applicable action, possible actions are: {[i for i in actiondict]}')
        return
    
    guild_id = message.channel.guild.id
    try:
        pattern = re.compile(r'(https?://scoresaber\.com/u/)?(\d{17})')
        match = re.match(pattern, args[1])
        if match:
            playerID = match.group(2)
        else:
            await message.channel.send('ScoreSaber ID/URL in incorrect format.')
            return
    except IndexError:
        await message.channel.send('You need to provide a ScoreSaber profile ID/URL')
        return
    
    try:
        pattern = re.compile(r'<@!(\d+)>')
        match = re.match(pattern, args[2])
        if match:
            discord_user_id = args[2]
            # not sure if it is necessary to check if user id is real or exists in current guild
            # I think that should be handled by other functions (ppRoles function(s)?)
        else:
            await message.channel.send(f'Discord ID in incorrect format (received input was: {args[2]}). You can try omitting this argument if you just wanted to add yourself.')
            return
    except IndexError:
        discord_user_id = message.author.id


    Logger.log_add(f'player_func(guild_id: {guild_id}, playerID: {playerID}, discord_user_id: {discord_user_id}, action: {action})')

    db_guild = uow.guild_repo.get_guild_by_id(guild_id)
    db_player = uow.player_repo.get_player_by_player_id(playerID)

    await actionfunc()

async def channel_func(message, args):
    if not await can_execute(message):
        return
    
    async def add_channel():
        if db_guild.recent_scores_channel_id is not None:
            await message.channel.send(f'Channel ID {message.channel.name} ({channel_id}) has already been added!')
            return

        uow.guild_repo.set_recent_score_channel_id(guild_id, channel_id)

        await tasks.mark_all_guild_scores_sent(db_guild)

        await message.channel.send(f'Channel ID {message.channel.name} ({channel_id}) successfully added!')
    async def remove_channel():
        if db_guild.recent_scores_channel_id is None:
            await message.channel.send(f"Channel ID {message.channel.name} ({channel_id}) already doesn't exist in the channel list for server {client.get_guild(guild_id)}.")

        uow.guild_repo.set_recent_score_channel_id(guild_id, None)
        await message.channel.send(f'Channel ID {message.channel.name} ({channel_id}) successfully removed!')

    actiondict = {
        "add": add_channel,
        "remove": remove_channel
    }
    action = args[0]
    actionfunc = actiondict.get(action, False)
    if not actionfunc:
        message.channel.send(f'{action} is not an applicable action, possible actions are: {[i for i in actiondict]}')
        return
    
    channel_id = message.channel.id
    guild_id = message.channel.guild.id

    Logger.log_add(f'channel_func(channel: {channel_id}, guild: {guild_id}, action: {action})')
    db_guild = uow.guild_repo.get_guild_by_id(guild_id)

    await actionfunc()

#async def enable_feature(message, action, feature_flag):
async def enable_feature(message, args):
    if not await can_execute(message):
        return
    
    async def add_feature():
        if feature_flag == "ppRoles":
            uow.guild_repo.set_feature(guild.id, feature_flag, True)
            await tasks.update_all_player_roles(guild)
            await message.channel.send("Enabled pp roles feature")
    
    async def remove_feature():
        if feature_flag == "ppRoles":
            uow.guild_repo.set_feature(guild.id, feature_flag, False)
            await tasks.remove_guild_roles(guild)
            await message.channel.send("Disabled pp roles feature")

    actiondict = {
        "add": add_feature,
        "remove": remove_feature
    }
    action = args[0]
    actionfunc = actiondict.get(action, False)
    if not actionfunc:
        await message.channel.send(f'{action} is not an applicable action, possible actions are: {[i for i in actiondict]}')
        return
    
    featurelist = [
        "ppRoles"
    ]
    feature_flag = args[1]
    if feature_flag not in featurelist:
        await message.channel.send(f'{feature_flag} is not an applicable action, possible actions are: {[i for i in featurelist]}')
        return
    
    guild = message.channel.guild

    await actionfunc()

async def run_task(message, args=False):
    if not await can_execute(message):
        return

    actiondict = {
        "players": tasks.update_players,
        "roles": tasks.update_all_player_roles,
        "scores": tasks.update_players_scores,
        "notifications": tasks.send_notifications
    }
    if args:
        action = args[0]
        actionfunc = actiondict.get(action, False)
        if not actionfunc:
            await message.channel.send(f'{action} is not an applicable action, possible actions are: {[i for i in actiondict]}')
            return
    else:
        async def actionfunc(guild):
            await tasks.update_players(guild)
            await tasks.update_all_player_roles(guild)
            await tasks.update_players_scores(guild)
            await tasks.send_notifications(guild)

    Logger.log_add(f'update(guild: {message.guild}, args: {args})')
    await actionfunc(message.guild)


async def command(message, command, args):
    command_dict = {
        "hello": [hello, 0],
        "help": [help_func, 0],
        "player": [player_func, 2],
        "channel": [channel_func, 1],
        "feature": [enable_feature, 2],
        "update": [run_task, 0]
    }
    func, required_args = [i for i in command_dict.get(command, invalid_command)]
    if len(args) >= required_args:
        await func(message, args)
    else:
        await message.channel.send(f'The {command} command requires {required_args} arguments')
        

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
            command_msg, *args = [match.group(i+1) for i in range(3) if bool(match.group(i+1))]
            await command(message, command_msg, args)



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
