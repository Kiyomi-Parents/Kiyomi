# bot.py
import os

import requests
import json
import discord
from dotenv import load_dotenv
import re
from datetime import datetime
from datetime import timedelta
import dateutil.parser
import asyncio
from discord.ext import tasks, commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

try:
    with open("config.json", "r") as configfile:
        config = json.load(configfile)
except:
    config = {}

def saveconfig(config):
    with open("config.json", "w") as configfile:
        json.dump(config, configfile)

#client = discord.Client()
client = commands.Bot(('!'))

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

def guildcheck(guild):
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

    if message.content.startswith('!player '):
        pattern = re.compile(r"!player *(\w+) *(https://scoresaber\.com/u/)?(\d{17})")
        match = re.match(pattern, message.content)
        if match:
            playerID = int(match.group(3))
            action = match.group(1)
            await playerfunc(playerID, message, action)
        else:
            await format_error_message(message)
    
    if message.content.startswith('!channel '):
        pattern = re.compile(r'!channel *(\w+) *(\d{18})?')
        match = re.match(pattern, message.content)
        inputchannelID = message.channel.id
        if match:
            if bool(match.group(2)):
                inputchannelID = int(match.group(2))
            action = match.group(1)
            await channelfunc(inputchannelID, message.channel.guild.id, message, action)

        else:
            await format_error_message(message)

async def playerfunc(playerID, message, action):
    msg_guild = message.guild
    guildcheck(msg_guild.id)
    global config
    try:
        playerIDs = config[str(msg_guild.id)]["playerIDs"]
    except KeyError:
        playerIDs = config[str(msg_guild.id)]["playerIDs"] = []
    if action == "add":
        if playerID not in playerIDs:
            playerID_check = get_player(playerID)
            try:
                playername = playerID_check["playerInfo"]["playerName"]
                await message.channel.send(f'Player {playername} successfully added!')
                playerIDs.append(playerID)
                saveconfig(config)
            except KeyError:
                await message.channel.send(f'Couldn\'t find a player with ID {playerID}')
        else:
            await message.channel.send(f'Player ID {playerID} has already been added!')
    elif action == "remove":
        if playerID in playerIDs:
            playerIDs.pop(playerIDs.index(playerID))
            saveconfig(config)
            await message.channel.send(f'Player ID {playerID} successfully removed!')
        else:
            await message.channel.send(f'Player ID {playerID} already doesn\'t exist in this Discord server\'s player list.')
    del playerIDs

def get_player(playerID):
    playerID_request = requests.get(f'https://new.scoresaber.com/api/player/{playerID}/basic')
    playerID_text = json.loads(playerID_request.text)
    return playerID_text

async def channelfunc(channelID, guildID, message, action):
    guildID = str(guildID)
    guildcheck(guildID)
    guild = client.get_guild(guildID)
    global config
    try:
        channellist = config[guildID]["channelIDs"]
    except:
        channellist = config[guildID]["channelIDs"] = []
    if action == "add":
        currentguildchannels = [channel.id for channel in message.channel.guild.channels]
        if channelID not in channellist and channelID in currentguildchannels:
            channellist.append(channelID)
            saveconfig(config)
            await message.channel.send(f'Channel ID {channelID} successfully added!')
        elif channelID not in currentguildchannels:
            if channelID in channellist:
                channellist.pop(channellist.index(channelID))
                saveconfig(config)
            await message.channel.send(f'Channel ID {channelID} doesn\'t exist in this Discord server (or isn\'t visible to the bot).')
        else:
            await message.channel.send(f'Channel ID {channelID} has already been added!')
    elif action == "remove":
        if channelID in channellist:
            channellist.pop(channellist.index(channelID))
            saveconfig(config)
            await message.channel.send(f'Channel ID {channelID} successfully removed!')
        else:
            await message.channel.send(f'Channel ID {channelID} already doesn\'t exist in the channel list for server {guild}.')
    del channellist

def checkSS(playerID):
    url = f"https://new.scoresaber.com/api/player/{playerID}/scores/recent"
    scoresrequest = requests.get(url)
    recentscores = json.loads(scoresrequest.text)["scores"]
    recentscores.reverse()
    return recentscores

@tasks.loop(seconds = 60)
async def SSLoop():
    await client.wait_until_ready()
    global config
    lastchecked = datetime.utcnow() - timedelta(minutes=1)
    #lastchecked = dateutil.parser.isoparse("2021-04-21T01:49:21.000Z").replace(tzinfo=None)
    #print(lastchecked)
    for guildID in config:
        for playerID in config[guildID]["playerIDs"]:
            recentscores = checkSS(playerID)
            for recentscore in recentscores:
                timeSet = dateutil.parser.isoparse(recentscore["timeSet"]).replace(tzinfo=None)
                # I'm removing time zone info because I'm assuming ScoreSaber has everything in UTC anyway
                # and when comparing 2 datetime objects either both of them need to have timezone info available
                # or both of them need to lack it.
                print(timeSet)
                print(lastchecked)
                if timeSet > lastchecked:
                    playername = get_player(playerID)["playerInfo"]["playerName"]
                    songName = recentscore["songName"]
                    songSubName = recentscore["songSubName"]
                    if songSubName:
                        songCombinedName = f'{songName}: {songSubName}'
                    else:
                        songCombinedName = songName
                    #songHash = recentscore["songHash"]
                    leaderboardId = recentscore["leaderboardId"]
                    rank = recentscore["rank"]
                    score = recentscore["score"]
                    maxScore = recentscore["maxScore"]
                    if maxScore:
                        acc = round(score/maxScore*100, 3)
                    else:
                        acc = "N/A"
                    rawpp = round(recentscore["pp"], 3)
                    weight = recentscore["weight"]
                    pp = round(rawpp*weight, 3)
                    leaderboardPage = (rank-1)//12 + 1
                    leaderboardLink = f"http://scoresaber.com/leaderboard/{leaderboardId}?page={leaderboardPage}"
                    for channelID in config[guildID]["channelIDs"]:
                        try:
                            channel = client.get_channel(channelID)
                            s1 = f'{playername} set a score of {score} on {songCombinedName}\n'
                            s2 = f'**Rank:** {rank}, **Raw PP:** {rawpp}, **PP:** {pp}, **ACC:** {acc}%\n{leaderboardLink}'
                            await channel.send(s1+s2)
                        except Exception as e:
                            print(e)


SSLoop.start()

client.run(TOKEN)