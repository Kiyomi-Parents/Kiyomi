from discord.ext import commands
from sqlalchemy import create_engine
from termcolor import colored

from src.cogs.beatsaber.actions import PlayerExistsException, PlayerNotFoundException, \
    GuildRecentChannelExistsException, GuildRecentChannelNotFoundException, GuildNotFoundException, Actions
from src.cogs.beatsaber.beatsaber_utils import BeatSaberUtils
from src.cogs.beatsaber.feature.feature import FeatureFlagException, FeatureFlagNotFoundException
from src.cogs.security import Security
from src.cogs.beatsaber.tasks import Tasks
from src.log import Logger
from src.storage.database import Database
from src.storage.uow import UnitOfWork


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
            await ctx.send(f'Successfully linked **{db_player.playerName}** ScoreSaber profile!')
        except (PlayerExistsException, PlayerNotFoundException) as e:
            await ctx.send(e)

    @player.command(name="remove")
    async def player_remove(self, ctx):
        """Remove the currently linked ScoreSaber profile from yourself."""
        try:
            await self.actions.remove_player(ctx.guild.id, ctx.author.id)
            await ctx.send(f'Successfully unlinked your ScoreSaber account!')
        except (PlayerNotFoundException, GuildNotFoundException) as e:
            await ctx.send(e)

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
            await ctx.send(f'Channel **{ctx.channel.name}** has successfully set as the notification channel!')
        except GuildRecentChannelExistsException as e:
            await ctx.send(e)

    @channel.command(name="remove")
    async def channel_remove(self, ctx):
        """Remove the currently set notification channel."""
        try:
            self.actions.remove_recent_channel(ctx.guild.id)
            await ctx.send(f'Notifications channel successfully removed!')
        except GuildRecentChannelNotFoundException as e:
            await ctx.send(e)

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
        except (FeatureFlagNotFoundException, FeatureFlagException) as e:
            await ctx.send(e)

    @feature.command(name="disable")
    async def feature_disable(self, ctx, feature_flag: str):
        """Available features: pp_roles"""
        try:
            await self.actions.disable_feature(ctx.guild.id, feature_flag)
            await ctx.send(f"Disabled {feature_flag} feature!")
        except (FeatureFlagNotFoundException, FeatureFlagException) as e:
            await ctx.send(e)

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
        db_guild = self.uow.guild_repo.get_guild_by_id(ctx.guild.id)
        await self.tasks.update_players(db_guild)

    @update.command(name="roles")
    async def update_roles(self, ctx):
        """Update player roles on Discord."""
        db_guild = self.uow.guild_repo.get_guild_by_id(ctx.guild.id)
        await self.tasks.update_all_player_roles(db_guild)

    @update.command(name="scores")
    async def update_scores(self, ctx):
        """Get the latest recent scores for players from ScoreSaber."""
        db_guild = self.uow.guild_repo.get_guild_by_id(ctx.guild.id)
        await self.tasks.update_players_scores(db_guild)

    @update.command(name="notifications")
    async def update_notifications(self, ctx):
        """Send recent score notifications."""
        db_guild = self.uow.guild_repo.get_guild_by_id(ctx.guild.id)
        await self.tasks.send_notifications(db_guild)

    @commands.command(name="showpp")
    async def show_pp(self, ctx):
        """Gives bot permission to check the persons PP."""
        db_player = self.uow.player_repo.get_player_by_member_id(ctx.author.id)

        if db_player is None or not BeatSaberUtils.is_player_in_guild(db_player, ctx.guild.id) or db_player.pp == 0:
            await ctx.send(f"**{ctx.author.name}** doesn't have a PP")
            return

        pp_size = round(db_player.pp / 100)
        await ctx.send(f"**{ctx.author.name}**'s PP is this big:\n8{'=' * pp_size}D")


def setup(bot):
    database = Database(create_engine('sqlite:///bot.db', echo=False))
    uow = UnitOfWork(bot, database)
    tasks = Tasks(uow)
    actions = Actions(uow, tasks)

    tasks.update_players.start()
    tasks.update_all_player_roles.start()
    tasks.update_players_scores.start()
    tasks.send_notifications.start()

    bot.add_cog(BeatSaber(uow, tasks, actions))
