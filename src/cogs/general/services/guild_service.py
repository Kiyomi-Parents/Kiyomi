from typing import List

import discord
from discord import NotFound

from src.kiyomi import BaseService
from ..storage import StorageUnitOfWork
from ..errors import GuildNotFoundException
from ..storage.model.guild import Guild
from ..storage.repository.guild_repository import GuildRepository


class GuildService(BaseService[Guild, GuildRepository, StorageUnitOfWork]):
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

    async def register_guilds(self, guilds: List[discord.Guild]) -> List[Guild]:
        return [await self.register_guild(guild) for guild in guilds]

    async def register_guild(self, discord_guild: discord.Guild) -> Guild:
        return await self.repository.upsert(Guild(discord_guild.id, discord_guild.name))

    async def unregister_guild(self, guild_id: int):
        await self.repository.remove_by_id(guild_id)

    async def upsert_guild(self, guild_id: int) -> discord.Guild:
        discord_guild = await self.get_discord_guild(guild_id)
        await self.repository.upsert(Guild(discord_guild.id, discord_guild.name))

        return discord_guild
