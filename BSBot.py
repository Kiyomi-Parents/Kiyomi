# good bot.py
import json
import os
import re
from datetime import datetime
import dateutil.parser

import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv

from src.scoresaber import Scoresaber

scoresaber = Scoresaber()
client = commands.Bot('!')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

try:
    with open("config.json", "r") as configfile:
        config = json.load(configfile)
except FileNotFoundError:
    config = {}


def save_config(config):
    with open("config.json", "w") as configfile:
        json.dump(config, configfile)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


def guild_check(guild):
    global config
    if type(guild) == discord.Guild:
        guild = guild.id
    if str(guild) not in config:
        config[str(guild)] = {}


async def format_error_message(message):
    await message.channel.send('Sorry, something went wrong! Make sure your message is in the correct format.')


@client.event
async def on_message(message):
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

    if message.content.startswith('!player '):
        pattern = re.compile(r"!player *(\w+) *(https?://scoresaber\.com/u/)?(\d{17})")
        match = re.match(pattern, message.content)
        if match:
            player_id = int(match.group(3))
            action = match.group(1)
            await player_func(player_id, message, action)
        else:
            await format_error_message(message)

    if message.content.startswith('!channel '):
        pattern = re.compile(r'!channel *(\w+) *(\d{18})?')
        match = re.match(pattern, message.content)
        input_channel_id = message.channel.id
        if match:
            if bool(match.group(2)):
                input_channel_id = int(match.group(2))
            action = match.group(1)
            await channel_func(input_channel_id, message.channel.guild.id, message, action)

        else:
            await format_error_message(message)


async def help_func(message, action):
    if action == "69":
        await message.channel.send('420')
    else:
        m1 = '**To add/remove player:**\n`!player add/remove playerID`\n'
        m2 = '**To add/remove current channel:**\n`!channel add/remove`\n'
        m3 = '**To add/remove another channel in the same Discord server:**\n`!channel add/remove channelID`'
        msg = m1 + m2 + m3
        await message.channel.send(msg)


async def player_func(playerID, message, action):
    msg_guild = message.guild
    guild_check(msg_guild.id)
    global config
    try:
        player_ids = config[str(msg_guild.id)]["playerIDs"]
    except KeyError:
        player_ids = config[str(msg_guild.id)]["playerIDs"] = []
    if action == "add":
        if playerID not in player_ids:
            player = scoresaber.get_player(playerID)
            try:
                await message.channel.send(f'Player {player.playerName} successfully added!')
                player_ids.append(playerID)
                save_config(config)
            except KeyError:
                await message.channel.send(f'Couldn\'t find a player with ID {playerID}')
        else:
            await message.channel.send(f'Player ID {playerID} has already been added!')
    elif action == "remove":
        if playerID in player_ids:
            player_ids.pop(player_ids.index(playerID))
            save_config(config)
            await message.channel.send(f'Player ID {playerID} successfully removed!')
        else:
            await message.channel.send(f'Player ID {playerID} already doesn\'t exist in this Discord server\'s player list.')
    del player_ids


async def channel_func(channel_id, guild_id, message, action):
    guild_id = guild_id
    guild_check(guild_id)
    guild = client.get_guild(guild_id)
    global config
    try:
        channel_list = config[guild_id]["channelIDs"]
    except:
        channel_list = config[guild_id]["channelIDs"] = []
    if action == "add":
        current_guild_channels = [channel.id for channel in message.channel.guild.channels]
        if channel_id not in channel_list and channel_id in current_guild_channels:
            channel_list.append(channel_id)
            save_config(config)
            await message.channel.send(f'Channel ID {channel_id} successfully added!')
        elif channel_id not in current_guild_channels:
            if channel_id in channel_list:
                channel_list.pop(channel_list.index(channel_id))
                save_config(config)
            await message.channel.send(f'Channel ID {channel_id} doesn\'t exist in this Discord server (or isn\'t visible to the bot).')
        else:
            await message.channel.send(f'Channel ID {channel_id} has already been added!')
    elif action == "remove":
        if channel_id in channel_list:
            channel_list.pop(channel_list.index(channel_id))
            save_config(config)
            await message.channel.send(f'Channel ID {channel_id} successfully removed!')
        else:
            await message.channel.send(f'Channel ID {channel_id} already doesn\'t exist in the channel list for server {guild}.')
    del channel_list

timeran = datetime.utcnow()

@tasks.loop(seconds=60)
async def SSLoop():
    await client.wait_until_ready()
    global config
    for guildID in config:
        for playerID in config[guildID]["playerIDs"]:
            attempt = 0
            attempting = True
            while attempting and attempt < 6:
                try:
                    player = scoresaber.get_player(playerID)
                    new_scores = player.get_new_scores()
                    attempting = False
                except Exception as e:
                    print(f'{playerID}\n{e}')
                    attempt += 1
                else:
                    for new_score in new_scores:
                        if timeran < dateutil.parser.isoparse(new_score.timeSet).replace(tzinfo=None):
                            for channelID in config[guildID]["channelIDs"]:
                                try:
                                    channel = client.get_channel(channelID)
                                    embed = player.get_score_embed(new_score, new_score.get_song())

                                    await channel.send(embed=embed)
                                    print(f'Sent {player.playerName}\'s score ({new_score.scoreId}) to {channelID} in {guildID}!')
                                except Exception as e:
                                    print(f'{datetime.utcnow()} Channel: {channelID}, player: {player.playerName}, discord: {guildID}, Error: {e}')
                        else:
                            print("score too old")
                            pass


SSLoop.start()
client.run(TOKEN)
