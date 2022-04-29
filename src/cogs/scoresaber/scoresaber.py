import discord
from discord import app_commands, Interaction
from discord.app_commands import Transform
from discord.ext import commands

from src.cogs.general import GeneralAPI
from .errors import MemberPlayerNotFoundInGuildException
from .messages.views.score_view import ScoreView
from .scoresaber_cog import ScoreSaberCog
from src.kiyomi import permissions
from .transformers.scoresaber_player_id_transformer import ScoreSaberPlayerIdTransformer


class ScoreSaber(ScoreSaberCog, name="Score Saber"):

    @commands.Cog.listener()
    async def on_ready(self):
        await self.player_service.start_scoresaber_api_client()

    player = app_commands.Group(
            name="player",
            description="Link ScoreSaber profile to Discord member"
    )

    @player.command(name="add")
    @app_commands.describe(profile="Score Saber profile URL")
    async def player_add(
            self,
            ctx: Interaction,
            profile: Transform[str, ScoreSaberPlayerIdTransformer]
    ):
        """Link yourself to your ScoreSaber profile."""
        self.bot.events.emit("register_member", ctx.user)

        guild_player = await self.player_service.add_player_with_checks(
                ctx.guild_id,
                ctx.user.id,
                profile
        )

        await ctx.response.send_message(
                f"Successfully linked **{guild_player.player.name}** ScoreSaber profile!",
                ephemeral=True
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
    async def recent_scores(
            self,
            ctx: Interaction,
            member: discord.Member,
            count: Option(
                    int,
                    "Amount of scores to post",
                    min_value=1,
                    max_value=3,
                    default=1,
                    required=False
            )
    ):
        """Displays your most recent scores"""
        if discord_member is None:
            discord_member = ctx.user

        guild_player = await self.player_service.get_guild_player(ctx.guild.id, discord_member.id)

        if guild_player is None:
            await ctx.response.send_message("Player not found!")
            return

        if count <= 0:
            await ctx.response.send_message("Score count needs to be positive!")
            return

        try:
            scores = self.score_service.get_recent_scores(guild_player.player.id, count)

            if scores is None or len(scores) == 0:
                await ctx.response.send_message("No scores found!")
                return

            for score in scores:
                previous_score = self.score_service.get_previous_score(score)

                score_view = ScoreView(self.bot, ctx.interaction.guild, score, previous_score)
                await score_view.respond(ctx.interaction)

        except IndexError as e:
            await ctx.response.send_message("Song argument too large")

    @app_commands.command(name="manual-add")

    @permissions.is_bot_owner_and_admin_guild()
    async def manual_add_player(
            self,
            ctx: Interaction,
            member_id: Option(
                    int,
                    "Discord member ID"
            ),
            player_id: Option(
                    str,
                    "Score Saber player ID"
            ),
            guild_id: Option(
                    int,
                    "Discord guild ID",
                    required=False
            )
    ):
        """Add a Score Saber profile manually"""

        if guild_id is None:
            guild_id = ctx.guild_id

        if member_id is None:
            await ctx.response.send_message(f"Please specify a member!", ephemeral=True)
            return

        general = self.uow.bot.get_cog_api(GeneralAPI)
        member = await general.get_discord_member(guild_id, member_id)
        self.bot.events.emit("register_member", member)

        guild_player = await self.player_service.add_player(guild_id, member_id, player_id)

        await ctx.response.send_message(
                f"Successfully linked Score Saber profile {guild_player.player.name} to member {guild_player.member.name} in guild {guild_player.guild.name}",
                ephemeral=True
        )

    @slash_command(name="manual-remove", **permissions.is_bot_owner_and_admin_guild())
    async def manual_remove_player(
            self,
            ctx: Interaction,
            member_id: Option(
                    int,
                    "Discord member ID"
            ),
            player_id: Option(
                    str,
                    "Score Saber player ID"
            ),
            guild_id: Option(
                    int,
                    "Discord guild ID",
                    required=False
            )
    ):
        """Remove a Score Saber profile manually"""
        if guild_id is None:
            guild_id = ctx.guild_id

        if member_id is None:
            await ctx.response.send_message(f"Please specify a member!", ephemeral=True)
            return

        guild_player = await self.player_service.remove_player(guild_id, member_id, player_id)

        await ctx.response.send_message(
                f"Successfully unlinked Score Saber profile {guild_player.player.name} from member {guild_player.member.name} in guild {guild_player.guild.name}!",
                ephemeral=True
        )

    @manual_remove_player.error
    async def manual_remove_player_error(self, ctx: Interaction, exception: Exception):
        if isinstance(exception, ApplicationCommandInvokeError):
            error = exception.original

            if isinstance(error, MemberPlayerNotFoundInGuildException):
                return await error.handle(
                        ctx,
                        message=f"%member_id% doesn't have a Score Saber profile %player_id% " \
                                "linked in guild %guild_id%."
                )

    @user_command(name="Refresh Score Saber Profile", **permissions.is_bot_owner())
    async def refresh(self, ctx: Interaction, member: discord.Member):
        guild_player = await self.player_service.get_guild_player(ctx.guild_id, member.id)

        await self.player_service.update_player(guild_player.player)
        await self.score_service.update_player_scores(guild_player.player)

        await ctx.response.send_message(f"Updated {member.name}'s Score Saber profile ({guild_player.player.name})", ephemeral=True)
