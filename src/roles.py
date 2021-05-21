from discord import Colour

from src.storage.model.discord_role import DiscordRole


class Roles:

    def __init__(self, uow, db_guild, db_player):
        self.uow = uow
        self.db_guild = db_guild
        self.db_player = db_player

        self.guild = self.uow.client.get_guild(self.db_guild.discord_guild_id)
        self._member = None

    @property
    async def member(self):
        if not self._member:
            self._member = await self.guild.fetch_member(self.db_player.discord_user_id)

        return self._member

    @property
    def get_pp_range_text(self):
        if self.db_player.pp_class < 1000:
            return f"<{int(self.db_player.pp_class)} PP club"
        else:
            return f"{int(self.db_player.pp_class)} PP club"

    async def give_member_role(self, role):
        member = await self.member

        if role not in member.roles:
            await member.add_roles(role)

            db_role = self.get_db_role(role)
            self.uow.player_repo.add_role(self.db_player, db_role)

    async def remove_player_role(self, db_role):
        member = await self.member
        role = self.get_role(db_role)
        await member.remove_roles(role, reason="Removed PP ranking (BOT)")
        self.uow.player_repo.remove_role(self.db_player, db_role)

    async def remove_player_roles(self):
        for db_role in self.db_player.roles:
            if db_role.guild_id == self.db_guild.id:
                await self.remove_player_role(db_role)

    async def remove_guild_role(self, db_role):
        role = self.get_role(db_role)
        await role.delete(reason="Disabled PP roles feature (BOT)")
        self.uow.guild_repo.remove_role(self.db_guild, db_role)

    async def remove_guild_roles(self):
        for db_role in self.db_guild.roles:
            await self.remove_guild_role(db_role)

    async def remove_obsolete_player_roles(self):
        for db_role in self.db_player.roles:
            if db_role.pp_requirement != self.db_player.pp_class:
                await self.remove_player_role(db_role)

    def get_role(self, db_role):
        return self.guild.get_role(db_role.role_id)

    def get_db_role(self, role):
        for db_role in self.db_guild.roles:
            if db_role.role_id == role.id:
                return db_role

    async def get_pp_role(self):
        for db_role in self.db_guild.roles:
            if db_role.pp_requirement == self.db_player.pp_class:
                return self.get_role(db_role)

        return await self.create_role()

    def create_db_role(self, role):
        db_role = DiscordRole(role)
        db_role.pp_requirement = self.db_player.pp_class

        return db_role

    async def create_role(self):
        role = await self.guild.create_role(name=f"{self.get_pp_range_text}", colour=Colour.random(), hoist=True, reason="PP ranking (BOT)")
        db_role = self.create_db_role(role)

        self.uow.guild_repo.add_role(self.db_guild, db_role)

        return role
