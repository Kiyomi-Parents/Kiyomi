from typing import Optional

import discord
from discord import app_commands, Interaction, AppCommandType
from discord.app_commands import Transform, CommandInvokeError, AppCommandError
from discord.ext import commands

from kiyomi.cogs.general import GeneralAPI
from .services import ServiceUnitOfWork
from .errors import MemberPlayerNotFoundInGuildException
from .messages.views.score_view import ScoreView
from kiyomi import permissions, Kiyomi, BaseCog
from .transformers.scoresaber_player_id_transformer import ScoreSaberPlayerIdTransformer
from ..settings.storage.model.emoji_setting import EmojiSetting


class ScoreSaber(BaseCog[ServiceUnitOfWork], name="Score Saber"):
    def __init__(self, bot: Kiyomi, service_uow: ServiceUnitOfWork):
        super().__init__(bot, service_uow)

        # Workaround until @app_commands.context_menu() supports self in function parameters
        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name="Refresh Score Saber Profile",
                callback=self.refresh,
                type=AppCommandType.user,
            )
        )

    def register_events(self):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        settings = [
            # TODO: Add bot owner permissions
            EmojiSetting.create(self.bot, self.__cog_name__, "BeatSaver emoji", "beatsaver_emoji"),
        ]

        self.bot.events.emit("setting_register", settings)

    player = app_commands.Group(name="player", description="Link ScoreSaber profile to Discord member")

    @player.command(name="add")
    @app_commands.describe(profile="Score Saber profile URL")
    async def player_add(self, ctx: Interaction, profile: Transform[str, ScoreSaberPlayerIdTransformer]):
        """Link yourself to your ScoreSaber profile."""
        await ctx.response.defer()

        async with self.bot.get_cog_api(GeneralAPI) as general_api:
            await general_api.register_member(ctx.guild_id, ctx.user.id)

        guild_player = await self._service_uow.players.add_player_with_checks(ctx.guild_id, ctx.user.id, profile)
        await self._service_uow.save_changes()
        await self._service_uow.refresh(guild_player)

        await ctx.followup.send(
            f"Successfully linked **{guild_player.player.name}** ScoreSaber profile!",
        )

    @player.command(name="remove")
    async def player_remove(self, ctx: Interaction):
        """Remove the currently linked ScoreSaber profile from yourself."""
        await ctx.response.defer()

        await self._service_uow.players.remove_player_with_checks(ctx.guild_id, ctx.user.id)
        await self._service_uow.save_changes()

        await ctx.followup.send("Successfully unlinked your ScoreSaber account!")

    @app_commands.command(name="showpp")
    async def show_pp(self, ctx: Interaction):
        """Gives bot permission to check the persons PP."""
        await ctx.response.defer()

        guild_player = await self._service_uow.players.get_guild_player(ctx.guild.id, ctx.user.id)

        if guild_player.player.pp == 0:
            await ctx.followup.send(f"**{ctx.user.name}** doesn't have a PP")
            return

        pp_size = round(guild_player.player.pp / 100)
        await ctx.followup.send(f"**{ctx.user.name}**'s PP is this big:\n8{'=' * pp_size}D")

    @show_pp.error
    async def show_pp_error(self, ctx: Interaction, error: AppCommandError):
        if isinstance(error, MemberPlayerNotFoundInGuildException):
            return await error.handle(bot=self.bot, ctx=ctx, message=f"**{ctx.user.name}** doesn't have a PP")

    @app_commands.command(name="recent")
    @app_commands.rename(member="user")
    @app_commands.describe(member="Discord user", count="Amount of scores to post")
    async def recent_scores(self, ctx: Interaction, member: Optional[discord.Member], count: Optional[int]):
        """Displays your most recent scores"""
        await ctx.response.defer()

        # TODO: Somebody, please. Just refactor this entire thing. :)
        if member is None:
            member = ctx.user

        if count is None:
            count = 1

        guild_player = await self._service_uow.players.get_guild_player(ctx.guild.id, member.id)

        if 0 >= count >= 3:
            await ctx.followup.send("Score count has to be between 0 and 3")
            return

        scores = await self._service_uow.scores.get_recent_scores(guild_player.player_id, count)

        if scores is None or len(scores) == 0:
            await ctx.followup.send("No scores found!")
            return

        for score in scores:
            previous_score = await self._service_uow.scores.get_previous_score(score)

            score_view = ScoreView(self.bot, ctx.guild, score, previous_score)
            await score_view.respond(ctx)

    @recent_scores.error
    async def recent_scores_error(self, ctx: Interaction, error: AppCommandError):
        if isinstance(error, MemberPlayerNotFoundInGuildException):
            return await error.handle(
                    bot=self.bot,
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
        await ctx.response.defer(ephemeral=True)

        if guild_id is None:
            guild_id = ctx.guild_id

        if member_id is None:
            await ctx.response.send_message(f"Please specify a member!", ephemeral=True)
            return

        async with self.bot.get_cog_api(GeneralAPI) as general:
            await general.register_member(guild_id, member_id)

        guild_player = await self._service_uow.players.register_player(guild_id, member_id, player_id)
        await self._service_uow.save_changes()

        await ctx.followup.send(
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
        await ctx.response.defer(ephemeral=True)

        if guild_id is None:
            guild_id = ctx.guild_id

        if member_id is None:
            await ctx.followup.send(f"Please specify a member!", ephemeral=True)
            return

        guild_player = await self._service_uow.players.remove_player(guild_id, member_id, player_id)
        await self._service_uow.save_changes()

        await ctx.followup.send(
            f"Successfully unlinked Score Saber profile {guild_player.player.name} from member {guild_player.member.name} in guild {guild_player.guild.name}!",
            ephemeral=True,
        )

    @manual_remove_player.error
    async def manual_remove_player_error(self, ctx: Interaction, error: AppCommandError):
        if isinstance(error, CommandInvokeError):
            error = error.original

        if isinstance(error, MemberPlayerNotFoundInGuildException):
            return await error.handle(
                bot=self.bot,
                ctx=ctx,
                message=f"%member_id% doesn't have a Score Saber profile %player_id% linked in guild %guild_id%.",
            )

    # @app_commands.context_menu(name="Refresh Score Saber Profile")
    @permissions.is_bot_owner()
    async def refresh(self, ctx: Interaction, member: discord.Member):
        guild_player = await self._service_uow.players.get_guild_player(ctx.guild_id, member.id)

        await ctx.response.defer(ephemeral=True)

        await self._service_uow.players.update_player(guild_player.player)
        await self._service_uow.scores.update_player_scores(guild_player.player)
        await self._service_uow.save_changes()

        await ctx.followup.send(
            f"Updated {member.name}'s Score Saber profile ({guild_player.player.name})",
            ephemeral=True,
        )
