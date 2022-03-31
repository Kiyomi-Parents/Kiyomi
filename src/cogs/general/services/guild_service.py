import discord

from .general_service import GeneralService
from ..errors import GuildNotFoundException
from ..storage.model.guild import Guild


class GuildService(GeneralService):
    async def get_discord_guild(self, guild_id: int) -> discord.Guild:
        discord_guild = self.bot.get_guild(guild_id)

        if discord_guild is None:
            discord_guild = await self.bot.fetch_guild(guild_id)

        if discord_guild is None:
            raise GuildNotFoundException(f"Could not find guild with id {guild_id}")

        return discord_guild

    def register_guild(self, discord_guild: discord.Guild):
        guild = self.uow.guilds.get_by_id(discord_guild.id)

        if guild is None:
            self.uow.guilds.add(Guild(discord_guild.id, discord_guild.name))
