from src.commands.beatsaber.feature.feature import Feature
from src.commands.beatsaber.roles import RolesCountryRank


class FeatureCountryRankRoles(Feature):
    def __init__(self, uow, db_guild):
        super().__init__(uow, db_guild, "country_rank_roles")
        self.roles = RolesCountryRank(uow, db_guild)

    async def on_enable(self):
        await self.update_guild_roles()

    async def on_disable(self):
        await self.remove_guild_roles()

    async def update_guild_roles(self):
        for db_player in self.db_guild.players:
            await self.roles.assign_player_role(db_player)

    async def remove_guild_roles(self):
        await self.roles.strip_guild_roles()
