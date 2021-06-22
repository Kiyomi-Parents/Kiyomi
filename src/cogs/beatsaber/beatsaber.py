from discord.ext import commands
from termcolor import colored

from src.cogs.beatsaber.actions import PlayerExistsException, PlayerNotFoundException, \
    GuildRecentChannelExistsException, GuildRecentChannelNotFoundException, GuildNotFoundException, SongNotFound
from src.cogs.beatsaber.beatsaber_utils import BeatSaberUtils
from src.cogs.beatsaber.feature.feature import FeatureFlagException, FeatureFlagNotFoundException
from src.cogs.beatsaber.message import Message
from src.cogs.security import Security
from src.log import Logger


class BeatSaber(commands.Cog):
    def __init__(self, uow, tasks, actions):
        self.uow = uow
        self.tasks = tasks
        self.actions = actions

    def cog_check(self, ctx):
        db_guild = self.uow.guild_repo.get_guild_by_id(ctx.guild.id)

        if db_guild is None:
            self.uow.guild_repo.add_guild(ctx.guild)

        return True

    async def cog_before_invoke(self, ctx):
        Logger.log(self.qualified_name,
                   f"{colored(ctx.author.name, 'blue')} executed command "
                   f"{colored(ctx.message.content, 'blue')} in "
                   f"{colored(ctx.channel.name, 'blue')} at "
                   f"{colored(ctx.guild.name, 'blue')}")

        await ctx.trigger_typing()

    @commands.group(invoke_without_command=True)
    async def player(self, ctx):
        """Link ScoreSaber profile to Discord member."""
        await ctx.send_help(ctx.command)

    @player.command(name="add")
    async def player_add(self, ctx, profile: str):
        """Link yourself to your ScoreSaber profile."""
        scoresaber_id = BeatSaberUtils.scoresaber_id_from_url(profile)

        try:
            db_player = await self.actions.add_player(ctx.guild.id, ctx.author.id, scoresaber_id)
            await ctx.send(f"Successfully linked **{db_player.playerName}** ScoreSaber profile!")
        except (PlayerExistsException, PlayerNotFoundException) as error:
            await ctx.send(error)

    @player.command(name="remove")
    async def player_remove(self, ctx):
        """Remove the currently linked ScoreSaber profile from yourself."""
        try:
            await self.actions.remove_player(ctx.guild.id, ctx.author.id)
            await ctx.send("Successfully unlinked your ScoreSaber account!")
        except (PlayerNotFoundException, GuildNotFoundException) as error:
            await ctx.send(error)

    @commands.group(invoke_without_command=True)
    @Security.owner_or_permissions(administrator=True)
    async def channel(self, ctx):
        """Set the recent score notification channel for ScoreSaber scores."""
        await ctx.send_help(ctx.command)

    @channel.command(name="add")
    async def channel_add(self, ctx):
        """Set current channel as the notification channel."""
        try:
            self.actions.add_recent_channel(ctx.guild.id, ctx.channel.id)
            await ctx.send(f"Channel **{ctx.channel.name}** has successfully set as the notification channel!")
        except GuildRecentChannelExistsException as error:
            await ctx.send(error)

    @channel.command(name="remove")
    async def channel_remove(self, ctx):
        """Remove the currently set notification channel."""
        try:
            self.actions.remove_recent_channel(ctx.guild.id)
            await ctx.send("Notifications channel successfully removed!")
        except GuildRecentChannelNotFoundException as error:
            await ctx.send(error)

    @commands.group(invoke_without_command=True)
    @Security.owner_or_permissions(administrator=True)
    async def feature(self, ctx):
        """To add/remove feature from Discord server."""
        await ctx.send_help(ctx.command)

    @feature.command(name="enable")
    async def feature_enable(self, ctx, feature_flag: str):
        """Available features: pp_roles"""
        try:
            await self.actions.enable_feature(ctx.guild.id, feature_flag)
            await ctx.send(f"Enabled {feature_flag} feature!")
        except (FeatureFlagNotFoundException, FeatureFlagException) as error:
            await ctx.send(error)

    @feature.command(name="disable")
    async def feature_disable(self, ctx, feature_flag: str):
        """Available features: pp_roles"""
        try:
            await self.actions.disable_feature(ctx.guild.id, feature_flag)
            await ctx.send(f"Disabled {feature_flag} feature!")
        except (FeatureFlagNotFoundException, FeatureFlagException) as error:
            await ctx.send(error)

    @commands.group()
    @Security.owner_or_permissions(administrator=True)
    async def update(self, ctx):
        """Run a task or run all tasks."""
        if ctx.subcommand_passed is None:
            db_guild = self.uow.guild_repo.get_guild_by_id(ctx.guild.id)

            await self.tasks.update_players(db_guild)
            await self.tasks.update_all_player_roles(db_guild)
            await self.tasks.update_players_scores(db_guild)
            await self.tasks.send_notifications(db_guild)
        elif ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @update.command(name="players")
    async def update_players(self, ctx):
        """Get the latest player information from ScoreSaber."""
        await self.actions.update_players(ctx.guild.id)

    @update.command(name="roles")
    async def update_roles(self, ctx):
        """Update player roles on Discord."""
        await self.actions.update_all_player_roles(ctx.guild.id)

    @update.command(name="scores")
    async def update_scores(self, ctx):
        """Get the latest recent scores for players from ScoreSaber."""
        await self.actions.update_players_scores(ctx.guild.id)

    @update.command(name="notifications")
    async def update_notifications(self, ctx):
        """Send recent score notifications."""
        await self.actions.send_notifications(ctx.guild.id)

    @commands.command(name="showpp")
    async def show_pp(self, ctx):
        """Gives bot permission to check the persons PP."""
        db_player = self.uow.player_repo.get_player_by_member_id(ctx.author.id)

        if db_player is None or not BeatSaberUtils.is_player_in_guild(db_player, ctx.guild.id) or db_player.pp == 0:
            await ctx.send(f"**{ctx.author.name}** doesn't have a PP")
            return

        pp_size = round(db_player.pp / 100)
        await ctx.send(f"**{ctx.author.name}**'s PP is this big:\n8{'=' * pp_size}D")

    @commands.command(aliases=["bsr", "song"])
    async def map(self, ctx, key: str):
        """Displays song info."""
        try:
            db_song = await self.actions.get_song(key)
            guild_leaderboard = await self.actions.get_guild_leaderboard(ctx.guild.id, db_song.key)

            song_embed = Message.get_song_embed(db_song)
            await ctx.send(embed=song_embed)

            if guild_leaderboard is not None:
                guild_leaderboard_embed = Message.get_leaderboard_embed(guild_leaderboard)
                await ctx.send(embed=guild_leaderboard_embed)
        except SongNotFound as error:
            await ctx.send(error)

    @commands.command(aliases=["recentmap", "recent_song", "recent_map"], invoke_without_command=True)
    async def recentsong(self, ctx, index:int=1):
        """Displays your most recent score"""
        db_player = self.uow.player_repo.get_player_by_member_id(ctx.author.id)
        if db_player is None:
            await ctx.send("Player not found!")
            return
        if index <= 0:
            index += 1
        try:
            db_scores = self.uow.score_repo.get_player_recent_scores(db_player)
            if db_scores is None:
                await ctx.send("No scores found!")
                return
            db_score = db_scores[index-1]
            score_embed = Message.get_score_embed(db_player, db_score)
            await ctx.send(embed=score_embed)
        except IndexError as e:
            await ctx.send("Song argument too large")