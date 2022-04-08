import discord
from discord import SlashCommandGroup, Option

from src.cogs.fancy_presence.fancy_presence_cog import FancyPresenceCog
from src.cogs.fancy_presence.storage.model.presence import Presence
from src.kiyomi import permissions


class FancyPresence(FancyPresenceCog):
    status = SlashCommandGroup(
            "status", "Commands related to Kiyomi's status",
            **permissions.is_bot_owner_and_admin_guild()
    )

    @status.command(name="update", **permissions.is_bot_owner_and_admin_guild())
    async def status_update(self, ctx: discord.ApplicationContext):
        """Force update status"""

        await self.presence_service.update_status()

        await ctx.respond("Status force updated!", ephemeral=True)

    @status.command(name="set", **permissions.is_bot_owner_and_admin_guild())
    async def status_set(
            self,
            ctx: discord.ApplicationContext,
            text: Option(
                    str,
                    "Text to display as status"
            )
    ):
        """Force status text"""

        await self.presence_service.set_presence(Presence(0, text))

        await ctx.respond("Status updated!", ephemeral=True)

    @status.command(name="reset", **permissions.is_bot_owner_and_admin_guild())
    async def status_set(
            self,
            ctx: discord.ApplicationContext
    ):
        """Reset forced status"""

        await self.presence_service.reset_presence()

        await ctx.respond("Status updated!", ephemeral=True)
