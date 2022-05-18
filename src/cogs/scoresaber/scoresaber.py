from typing import Optional

import discord
from discord import app_commands, Interaction, AppCommandType
from discord.app_commands import Transform, CommandInvokeError

from src.cogs.general import GeneralAPI
from .services import PlayerService, ScoreService
from .errors import MemberPlayerNotFoundInGuildException
from .messages.views.score_view import ScoreView
from .scoresaber_cog import ScoreSaberCog
from src.kiyomi import permissions, Kiyomi
from .transformers.scoresaber_player_id_transformer import ScoreSaberPlayerIdTransformer


class ScoreSaber(ScoreSaberCog, name="Score Saber"):
    def __init__(self, bot: Kiyomi, player_service: PlayerService, score_service: ScoreService):
        super().__init__(bot, player_service, score_service)

        # Workaround until @app_commands.context_menu() supports self in function parameters
        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name="Refresh Score Saber Profile",
                callback=self.refresh,
                type=AppCommandType.user,
            )
        )

    player = app_commands.Group(name="player", description="Link ScoreSaber profile to Discord member")

    @player.command(name="add")
    @app_commands.describe(profile="Score Saber profile URL")
    async def player_add(self, ctx: Interaction, profile: Transform[str, ScoreSaberPlayerIdTransformer]):
        """Link yourself to your ScoreSaber profile."""
        self.bot.events.emit("register_member", ctx.user)

        guild_player = await self.player_service.add_player_with_checks(ctx.guild_id, ctx.user.id, profile)

        await ctx.response.send_message(
            f"Successfully linked **{guild_player.player.name}** ScoreSaber profile!",
            ephemeral=True,
        )

    @player.command(name="remove")
    async def player_remove(self, ctx: Interaction):
        """Remove the currently linked ScoreSaber profile from yourself."""

        await self.player_service.remove_player_with_checks(ctx.guild_id, ctx.user.id)
        await ctx.response.send_message("Successfully unlinked your ScoreSaber account!", ephemeral=True)

    @app_commands.command(name="showpp")
    async def show_pp(self, ctx: Interaction):
        """Gives bot permission to check the persons PP."""
        guild_player = await self.player_service.get_guild_player(ctx.guild.id, ctx.user.id)

        if guild_player.player.pp == 0:
            await ctx.response.send_message(f"**{ctx.user.name}** doesn't have a PP")
            return

        pp_size = round(guild_player.player.pp / 100)
        await ctx.response.send_message(f"**{ctx.user.name}**'s PP is this big:\n8{'=' * pp_size}D")

    @show_pp.error
    async def show_pp_error(self, ctx: Interaction, error: Exception):
        if isinstance(error, MemberPlayerNotFoundInGuildException):
            return await error.handle(ctx=ctx, message=f"**{ctx.user.name}** doesn't have a PP")

    @app_commands.command(name="recent")
    @app_commands.rename(member="user")
    @app_commands.describe(member="Discord user", count="Amount of scores to post")
    async def recent_scores(self, ctx: Interaction, member: Optional[discord.Member], count: Optional[int]):
        """Displays your most recent scores"""
        # TODO: Just refactor this entire thing.
        if member is None:
            member = ctx.user

        guild_player = await self.player_service.get_guild_player(ctx.guild.id, member.id)

        if 0 >= count >= 3:
            await ctx.response.send_message("Score count has to be between 0 and 3")
            return

        scores = await self.score_service.get_recent_scores(guild_player.player.id, count)

        if scores is None or len(scores) == 0:
            await ctx.response.send_message("No scores found!")
            return

        for score in scores:
            previous_score = await self.score_service.get_previous_score(score)

            score_view = ScoreView(self.bot, ctx.guild, score, previous_score)
            await score_view.respond(ctx)

    @recent_scores.error
    async def recent_scores_error(self, ctx: Interaction, error: Exception):
        if isinstance(error, CommandInvokeError):
            error = error.original

        if isinstance(error, MemberPlayerNotFoundInGuildException):
            return await error.handle(
                ctx=ctx,
                message=f"%member_id% doesn't have a Score Saber profile linked",
            )

    @app_commands.command(name="manual-add")
    @app_commands.describe(
        member_id="Discord member ID",
        player_id="Score Saber player ID",
        guild_id="Discord guild ID",
    )
    @permissions.is_bot_owner_and_admin_guild()
    async def manual_add_player(self, ctx: Interaction, member_id: int, player_id: str, guild_id: Optional[int]):
        """Add a Score Saber profile manually"""

        if guild_id is None:
            guild_id = ctx.guild_id

        if member_id is None:
            await ctx.response.send_message(f"Please specify a member!", ephemeral=True)
            return

        general = self.bot.get_cog_api(GeneralAPI)
        member = await general.get_discord_member(guild_id, member_id)
        self.bot.events.emit("register_member", member)

        guild_player = await self.player_service.register_player(guild_id, member_id, player_id)

        await ctx.response.send_message(
            f"Successfully linked Score Saber profile {guild_player.player.name} to member {guild_player.member.name} in guild {guild_player.guild.name}",
            ephemeral=True,
        )

    @app_commands.command(name="manual-remove")
    @app_commands.describe(
        member_id="Discord member ID",
        player_id="Score Saber player ID",
        guild_id="Discord guild ID",
    )
    @permissions.is_bot_owner_and_admin_guild()
    async def manual_remove_player(self, ctx: Interaction, member_id: int, player_id: str, guild_id: Optional[int]):
        """Remove a Score Saber profile manually"""
        if guild_id is None:
            guild_id = ctx.guild_id

        if member_id is None:
            await ctx.response.send_message(f"Please specify a member!", ephemeral=True)
            return

        guild_player = await self.player_service.remove_player(guild_id, member_id, player_id)

        await ctx.response.send_message(
            f"Successfully unlinked Score Saber profile {guild_player.player.name} from member {guild_player.member.name} in guild {guild_player.guild.name}!",
            ephemeral=True,
        )

    @manual_remove_player.error
    async def manual_remove_player_error(self, ctx: Interaction, error: Exception):
        if isinstance(error, CommandInvokeError):
            error = error.original

        if isinstance(error, MemberPlayerNotFoundInGuildException):
            return await error.handle(
                ctx=ctx,
                message=f"%member_id% doesn't have a Score Saber profile %player_id% linked in guild %guild_id%.",
            )

    # @app_commands.context_menu(name="Refresh Score Saber Profile")
    @permissions.is_bot_owner()
    async def refresh(self, ctx: Interaction, member: discord.Member):
        guild_player = await self.player_service.get_guild_player(ctx.guild_id, member.id)

        await self.player_service.update_player(guild_player.player)
        await self.score_service.update_player_scores(guild_player.player)

        await ctx.response.send_message(
            f"Updated {member.name}'s Score Saber profile ({guild_player.player.name})",
            ephemeral=True,
        )
