from src.log import Logger
import re
from discord.ext import commands
from discord import Member

class BeatSaber(commands.Cog):
    def __init__(self, uow, tasks, client):
        self.uow = uow
        self.tasks = tasks
        self.client = client
    
    async def admin(self, message, func):
        async def wrapper():
            if not message.author.guild_permissions.administrator:
                func()
            else:
                await message.channel.send("You don't have access to this command")
        return wrapper

    async def invalid_command(self, message, args=False):
        await message.channel.send('Sorry, something went wrong! Make sure your message is in the correct format.')

    @commands.command()
    async def hello(self, message, args=False):
        await message.channel.send('Hello there!')
    
    # @commands.command()
    # async def help_func(self, message, args=False):
    #     Logger.log_add(f'help_func()')
    #     m1 = '**To add/remove player:**\n`!player add/remove <ScoreSaber profile url/id> <discord user>`\n'
    #     m2 = '**To add/remove current channel:**\n`!channel add/remove`\n'
    #     m3 = '**To add/remove feature from Discord server:**\n`!feature add/remove [ppRoles]`\n'
    #     m4 = '**To update data:**\n`!update [players/roles/scores/notifications]`'
    #     msg = m1 + m2 + m3 + m4
    #     await message.channel.send(msg)

    @commands.command()
    async def player(self, ctx, action: str, ScoreSaberID: str):
        Logger.log_add(f'player(message.content: {ctx.message.content}, action: {action}, ScoreSaberID: {ScoreSaberID})')

        async def add_player():
            if db_player in db_guild.players:
                await ctx.send(f'Player ID {playerID} has already been added!')
                return

            new_player = self.uow.scoresaber.get_player(playerID)

            if new_player is None:
                await ctx.send(f'Failed to add player!')
                return

            new_player.discord_user_id = discord_user_id

            self.uow.player_repo.add_player(new_player)
            self.uow.player_repo.add_to_guild(new_player.playerId, db_guild)

            # Get player scores and marked them sent to decrease spam
            await self.tasks.update_player_scores(new_player)
            await self.tasks.mark_all_player_scores_sent(new_player)

            # Add role to player if enabled
            if db_guild.pp_roles:
                await self.tasks.update_player_roles(db_guild, new_player)

            await ctx.send(f'Player {new_player.playerName} successfully added!')
        
        async def remove_player():
            is_removed = False

            for db_player in db_guild.players:
                if playerID == db_player.playerId:
                    self.uow.guild_repo.remove_player(db_guild.discord_guild_id, db_player)
                    await self.tasks.remove_player_roles(db_guild, db_player)
                    await ctx.send(f'Player ID {playerID} successfully removed!')
                    is_removed = True

            if not is_removed:
                await ctx.send(f"Player ID {playerID} already doesn't exist in this Discord server's player list.")


        actiondict = {
            "add": add_player,
            "remove": remove_player
        }
        actionfunc = actiondict.get(action, False)
        if not actionfunc:
            ctx.send(f'{action} is not an applicable action, possible actions are: {[i for i in actiondict]}')
            return
        
        guild_id = ctx.guild.id
        try:
            pattern = re.compile(r'(https?://scoresaber\.com/u/)?(\d{17})')
            match = re.match(pattern, ScoreSaberID)
            if match:
                playerID = match.group(2)
            else:
                await ctx.send('ScoreSaber ID/URL in incorrect format.')
                return
        except IndexError:
            await ctx.send('You need to provide a ScoreSaber profile ID/URL')
            return
        
        discord_user_id = ctx.author.id

        Logger.log_add(f'player_func(guild_id: {guild_id}, playerID: {playerID}, discord_user_id: {discord_user_id}, action: {action})')

        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)
        db_player = self.uow.player_repo.get_player_by_player_id(playerID)

        await actionfunc()

    @commands.command() 
    async def channel(self, ctx, action):
        async def add_channel():
            if db_guild.recent_scores_channel_id is not None:
                await ctx.send(f'Channel ID {ctx.channel.name} ({channel_id}) has already been added!')
                return

            self.uow.guild_repo.set_recent_score_channel_id(guild_id, channel_id)

            await self.tasks.mark_all_guild_scores_sent(db_guild)

            await ctx.send(f'Channel ID {ctx.channel.name} ({channel_id}) successfully added!')
        async def remove_channel():
            if db_guild.recent_scores_channel_id is None:
                await ctx.send(f"Channel ID {ctx.channel.name} ({channel_id}) already doesn't exist in the channel list for server {self.client.get_guild(guild_id)}.")
                return

            self.uow.guild_repo.set_recent_score_channel_id(guild_id, None)
            await ctx.send(f'Channel ID {ctx.channel.name} ({channel_id}) successfully removed!')

        actiondict = {
            "add": add_channel,
            "remove": remove_channel
        }
        actionfunc = actiondict.get(action, False)
        if not actionfunc:
            ctx.send(f'{action} is not an applicable action, possible actions are: {[i for i in actiondict]}')
            return
        
        channel_id = ctx.channel.id
        guild_id = ctx.guild.id

        Logger.log_add(f'channel(channel: {channel_id}, guild: {guild_id}, action: {action})')
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)

        await actionfunc()

    @commands.command()
    async def feature(self, ctx, action: str, feature_flag: str):
        async def add_feature():
            if feature_flag == "ppRoles":
                self.uow.guild_repo.set_feature(guild.id, feature_flag, True)
                await self.tasks.update_all_player_roles(guild)
                await ctx.send("Enabled pp roles feature")
        
        async def remove_feature():
            if feature_flag == "ppRoles":
                self.uow.guild_repo.set_feature(guild.id, feature_flag, False)
                await self.tasks.remove_guild_roles(guild)
                await ctx.send("Disabled pp roles feature")

        actiondict = {
            "add": add_feature,
            "remove": remove_feature
        }
        actionfunc = actiondict.get(action, False)
        if not actionfunc:
            await ctx.send(f'{action} is not an applicable action, possible actions are: {[i for i in actiondict]}')
            return
        
        featurelist = [
            "ppRoles"
        ]
        if feature_flag not in featurelist:
            await ctx.send(f'{feature_flag} is not an applicable action, possible actions are: {[i for i in featurelist]}')
            return
        
        guild = ctx.guild

        await actionfunc()

    @commands.command()
    async def update(self, ctx, action: str = None):
        actiondict = {
            "players": self.tasks.update_players,
            "roles": self.tasks.update_all_player_roles,
            "scores": self.tasks.update_players_scores,
            "notifications": self.tasks.send_notifications
        }
        if action:
            if action in actiondict:
                actionfunc = actiondict.get(action)
        else:
            async def actionfunc(guild):
                await self.tasks.update_players(guild)
                await self.tasks.update_all_player_roles(guild)
                await self.tasks.update_players_scores(guild)
                await self.tasks.send_notifications(guild)

        Logger.log_add(f'update(guild: {ctx.guild}, action: {action})')
        await actionfunc(ctx.guild)

    @commands.command()
    async def showpp(self, ctx):
        Logger.log_add(f'get_pp() ran by {ctx.author.name} ({ctx.author.id} in {ctx.guild})')
        try:
            db_player = self.uow.guild_repo.get_player_by_discord_id(ctx.guild, ctx.author.id)
            pp_size = round(db_player.pp / 100)
            await ctx.send(f"{ctx.author.name}'s PP is this big:\n8{'=' * pp_size}D")
        except Exception as e:
            Logger.log_add(f'Exception {e} in get_pp(), message.content: {ctx.message.content}, author: {ctx.author}')