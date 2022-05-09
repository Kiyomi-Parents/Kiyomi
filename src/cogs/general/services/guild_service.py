import discord
from discord import NotFound

from .general_service import GeneralService
from ..errors import GuildNotFoundException
from ..storage.model.guild import Guild


class GuildService(GeneralService):
    async def get_discord_guild(self, guild_id: int) -> discord.Guild:
        discord_guild = self.bot.get_guild(guild_id)

        if discord_guild is None:
            try:
                discord_guild = await self.bot.fetch_guild(guild_id)
            except NotFound:
                raise GuildNotFoundException(f"Could not find guild with id {guild_id}")

        if discord_guild is None:
            raise GuildNotFoundException(f"Could not find guild with id {guild_id}")

        return discord_guild

    async def register_guild(self, guild_id: int) -> Guild:
        guild = self.uow.guilds.get_by_id(guild_id)

        if guild is None:
            discord_guild = await self.get_discord_guild(guild_id)
            guild = self.uow.guilds.add(Guild(guild_id, discord_guild.name))

        return guild

    async def unregister_guild(self, guild_id: int):
        self.uow.guilds.remove_by_id(guild_id)
