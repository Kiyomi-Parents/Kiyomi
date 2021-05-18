from discord.ext import commands
from src.log import Logger
from src.utils import Utils
from functools import wraps


class BeatSaber(commands.Cog):
    def __init__(self, uow, tasks):
        self.uow = uow
        self.tasks = tasks

    def admin(self, ctx):
        def inner_func(func):
            @wraps(func)
            async def wrapper(self, ctx):
                if ctx.author.guild_permissions.administrator:
                    await func(self, ctx)
                else:
                    Logger.log_add(f'{ctx.author.name} doesn\'t have the necessary permission(s) to use this command. Message: {ctx.message.content}')
                    await ctx.send('You don\'t have the necessary permission(s) to use this command!')
            return wrapper
        return inner_func

    @commands.command()
    async def hello(self, ctx):
        """Greet the bot."""
        await ctx.send('Hello there!')

    @commands.command()
    @admin("self", "ctx")
    async def admintest(self, ctx):
        """Command to test if security is working"""
        await ctx.send('This message should only be seen if !admintest was called by a server admin.')

    @commands.group(invoke_without_command=True)
    async def player(self, ctx):
        """Link ScoreSaber profile to Discord member."""
        await ctx.send_help(ctx.command)

    @player.command(name="add")
    async def player_add(self, ctx, profile: str):
        """Link yourself to your ScoreSaber profile."""
        player_id = Utils.scoresaber_id_from_url(profile)

        db_guild = self.uow.guild_repo.get_guild_by_discord_id(ctx.guild.id)
        db_player = self.uow.player_repo.get_player_by_member_id(ctx.author.id)

        if db_player in db_guild.players:
            await ctx.send(f'Player **{db_player.playerName}** has already been added!')
            return

        new_player = self.uow.scoresaber.get_player(player_id)

        if new_player is None:
            await ctx.send(f'Failed to add player!')
            return

        new_player.discord_user_id = ctx.author.id

        self.uow.player_repo.add_player(new_player)
        self.uow.player_repo.add_to_guild(new_player, db_guild)

        # Get player scores and marked them sent to decrease spam
        await self.tasks.update_player_scores(new_player)
        await self.tasks.mark_all_player_scores_sent(new_player)

        # Add role to player if enabled
        if db_guild.pp_roles:
            await self.tasks.update_player_roles(db_guild, new_player)

        await ctx.send(f'Player **{new_player.playerName}** successfully added!')

    @player.command(name="remove")
    async def player_remove(self, ctx):
        """Remove the currently linked ScoreSaber profile from yourself."""
        db_player = self.uow.player_repo.get_player_by_member_id(ctx.author.id)

        if db_player is None:
            await ctx.send(f"You don't have a ScoreSaber profile linked to yourself.")
            return

        for db_guild in db_player.guilds:
            if ctx.guild.id == db_guild.discord_guild_id:
                self.uow.player_repo.remove_guild(db_player, db_guild)

                # Remove player roles
                await self.tasks.remove_player_roles(db_guild, db_player)

                # If player doesnt belong to any guilds, remove player
                if len(db_player.guilds) == 0:
                    self.uow.player_repo.remove_player(db_player)

                await ctx.send(f'Player **{db_player.playerName}** successfully removed!')
                return

        await ctx.send(f"Player **{db_player.playerName}** has already been removed or didn't exist in the first place????")

    @commands.group(invoke_without_command=True)
    @admin("self","ctx")
    async def channel(self, ctx):
        """Set the recent score notification channel for ScoreSaber scores."""
        await ctx.send_help(ctx.command)

    @channel.command(name="add")
    async def channel_add(self, ctx):
        """Set current channel as the notification channel."""
        db_guild = self.uow.guild_repo.get_guild_by_discord_id(ctx.guild.id)

        if db_guild.recent_scores_channel_id is not None:
            await ctx.send(f'Channel **{ctx.channel.name}** has already been set as the notification channel!')
            return

        self.uow.guild_repo.set_recent_score_channel_id(db_guild, ctx.channel.id)
        await self.tasks.mark_all_guild_scores_sent(db_guild)

        await ctx.send(f'Channel **{ctx.channel.name}** has successfully set as the notification channel!')

    @channel.command(name="remove")
    async def channel_remove(self, ctx):
        """Remove the currently set notification channel."""
        db_guild = self.uow.guild_repo.get_guild_by_discord_id(ctx.guild.id)

        if db_guild.recent_scores_channel_id is None:
            await ctx.send(f"There isn't a notification channel set for this Discord server.")
            return

        self.uow.guild_repo.set_recent_score_channel_id(db_guild, None)
        await ctx.send(f'Notifications channel successfully removed!')

    @commands.group(invoke_without_command=True)
    @admin("self","ctx")
    async def feature(self, ctx):
        """To add/remove feature from Discord server."""
        await ctx.send_help(ctx.command)

    @feature.command(name="add")
    async def feature_add(self, ctx, feature_flag: str):
        """Available features: ppRoles"""
        db_guild = self.uow.guild_repo.get_guild_by_discord_id(ctx.guild.id)

        if feature_flag == "ppRoles":
            self.uow.guild_repo.set_feature(db_guild, feature_flag, True)
            await self.tasks.update_all_player_roles(ctx.guild)
            await ctx.send("Enabled pp roles feature")

    @feature.command(name="remove")
    async def feature_remove(self, ctx, feature_flag: str):
        """Available features: ppRoles"""
        db_guild = self.uow.guild_repo.get_guild_by_discord_id(ctx.guild.id)

        if feature_flag == "ppRoles":
            self.uow.guild_repo.set_feature(db_guild, feature_flag, False)
            await self.tasks.remove_guild_roles(ctx.guild)
            await ctx.send("Disabled pp roles feature")

    @commands.group()
    @admin("self","ctx")
    async def update(self, ctx):
        """Run a task or run all tasks."""
        if ctx.subcommand_passed is None:
            await self.tasks.update_players(ctx.guild)
            await self.tasks.update_all_player_roles(ctx.guild)
            await self.tasks.update_players_scores(ctx.guild)
            await self.tasks.send_notifications(ctx.guild)
        elif ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @update.command(name="players")
    async def update_players(self, ctx):
        """Get the latest player information from ScoreSaber."""
        await self.tasks.update_players(ctx.guild)

    @update.command(name="roles")
    async def update_roles(self, ctx):
        """Update player roles on Discord."""
        await self.tasks.update_all_player_roles(ctx.guild)

    @update.command(name="scores")
    async def update_scores(self, ctx):
        """Get the latest recent scores for players from ScoreSaber."""
        await self.tasks.update_players_scores(ctx.guild)

    @update.command(name="notifications")
    async def update_notifications(self, ctx):
        """Send recent score notifications."""
        await self.tasks.send_notifications(ctx.guild)

    @commands.command(name="showpp")
    async def show_pp(self, ctx):
        """Gives bot permission to check the persons PP."""
        db_player = self.uow.player_repo.get_player_by_member_id(ctx.author.id)

        if db_player is None or not Utils.is_player_in_guild(db_player, ctx.guild.id):
            await ctx.send(f"**{ctx.author.name}** doesn't have a PP")
            return

        pp_size = round(db_player.pp / 100)
        await ctx.send(f"**{ctx.author.name}**'s PP is this big:\n8{'=' * pp_size}D")
