import discord
from discord import SlashCommandGroup, slash_command, ApplicationCommandInvokeError, Option, ApplicationContext, \
    user_command
from discord.commands import permissions
from discord.ext import commands

from src.cogs.general import GeneralAPI
from .converters.score_saber_player_id_converter import ScoreSaberPlayerIdConverter
from .errors import MemberPlayerNotFoundInGuildException, ScoreSaberCogException
from .scoresaber_cog import ScoreSaberCog


class ScoreSaber(ScoreSaberCog, name="Score Saber"):

    @commands.Cog.listener()
    async def on_ready(self):
        await self.player_service.start_scoresaber_api_client()

    player = SlashCommandGroup(
            "player",
            "Link ScoreSaber profile to Discord member."
    )

    # TODO: Fix command concurrency. We should probably somehow do the import later?
    @player.command(name="add")
    async def player_add(
        self,
        ctx: discord.ApplicationContext,
        profile: Option(
                ScoreSaberPlayerIdConverter,
                "Score Saber profile URL"
        )
    ):
        """Link yourself to your ScoreSaber profile."""
        self.bot.events.emit("register_member", ctx.author)

        await ctx.defer()

        guild_player = await self.player_service.add_player_with_checks(
                ctx.interaction.guild_id,
                ctx.author.id,
                profile
        )

        await ctx.respond(content=f"Successfully linked **{guild_player.player.name}** ScoreSaber profile!")

    @player.command(name="remove")
    async def player_remove(self, ctx: discord.ApplicationContext):
        """Remove the currently linked ScoreSaber profile from yourself."""

        await self.player_service.remove_player_with_checks(ctx.guild.id, ctx.author.id)
        await ctx.respond("Successfully unlinked your ScoreSaber account!")

    @slash_command(name="showpp")
    async def show_pp(self, ctx: discord.ApplicationContext):
        """Gives bot permission to check the persons PP."""
        guild_player = await self.player_service.get_player_by_guild_id_and_guild_id(ctx.guild.id, ctx.author.id)

        if guild_player is None or guild_player.player.pp == 0:
            await ctx.respond(f"**{ctx.author.name}** doesn't have a PP")
            return

        pp_size = round(guild_player.player.pp / 100)
        await ctx.respond(f"**{ctx.author.name}**'s PP is this big:\n8{'=' * pp_size}D")

    # @slash_command(name="recent")
    # @Security.owner_or_permissions()
    # async def recent_scores(self, ctx: discord.ApplicationContext, discord_member: discord.Member = None, count: int = 1):
    #     """Displays your most recent scores"""
    #     if discord_member is None:
    #         discord_member = ctx.author
    #
    #     guild_player = await self.player_service.get_player_by_guild_id_and_guild_id(ctx.guild.id, discord_member.id)
    #
    #     if guild_player is None:
    #         await ctx.respond("Player not found!")
    #         return
    #
    #     if count <= 0:
    #         await ctx.respond("Score count needs to be positive!")
    #         return
    #
    #     try:
    #         scores = self.score_service.get_recent_scores(guild_player.player.id, count)
    #
    #         if scores is None:
    #             await ctx.respond("No scores found!")
    #             return
    #
    #         for score in scores:
    #             pass
    #             # TODO: FIX.
    #             # score_embed = Message.get_score_embed(guild_player.player, score)
    #             # await ctx.respond(embed=score_embed)
    #
    #     except IndexError as e:
    #         await ctx.respond("Song argument too large")

    @player.command(name="manual-add", default_permission=False)
    @permissions.is_owner()
    async def manual_add_player(
        self,
        ctx: discord.ApplicationContext,
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
            guild_id = ctx.interaction.guild_id

        if member_id is None:
            await ctx.respond(f"Please specify a member!")
            return

        general = self.uow.bot.get_cog_api(GeneralAPI)
        member = await general.get_discord_member(guild_id, member_id)
        self.bot.events.emit("register_member", member)

        guild_player = await self.player_service.add_player(guild_id, member_id, player_id)

        await ctx.respond(
                f"Successfully linked Score Saber profile {guild_player.player.name} to member {guild_player.member.name} in guild {guild_player.guild.name}"
        )

    @player.command(name="manual-remove", default_permission=False)
    @permissions.is_owner()
    async def manual_remove_player(
        self,
        ctx: discord.ApplicationContext,
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
            guild_id = ctx.interaction.guild_id

        if member_id is None:
            await ctx.respond(f"Please specify a member!")
            return

        guild_player = await self.player_service.remove_player(guild_id, member_id, player_id)

        await ctx.respond(
                f"Successfully unlinked Score Saber profile {guild_player.player.name} from member {guild_player.member.name} in guild {guild_player.guild.name}!"
        )

    @manual_remove_player.error
    async def manual_remove_player_error(self, ctx: discord.ApplicationContext, error: Exception):
        if isinstance(error, ApplicationCommandInvokeError):
            if isinstance(error.original, MemberPlayerNotFoundInGuildException):
                await ctx.respond(
                        f"{error.original.member_id} doesn't have a Score Saber profile with ID {error.original.player_id} linked in guild {error.original.guild_id}."
                )
                return

    @user_command(name="Refresh Score Saber Profile", default_permission=False)
    async def refresh(self, ctx: ApplicationContext, member: discord.Member):
        await ctx.respond(f"{ctx.author.name} just mentioned {member.mention}!")

    async def cog_command_error(self, ctx: ApplicationContext, error: Exception):
        if isinstance(error, ApplicationCommandInvokeError):
            if isinstance(error.original, ScoreSaberCogException):
                await ctx.respond(str(error.original))
                return
