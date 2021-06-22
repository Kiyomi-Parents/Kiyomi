from src.cogs.beatsaber.feature.feature import Feature
from src.cogs.beatsaber.roles.roles_country_rank import RolesCountryRank


class FeatureCountryRankRoles(Feature):
    def __init__(self, uow, db_guild):
        super().__init__(uow, db_guild, "country_rank_roles")
        self.roles = RolesCountryRank(uow, db_guild)

    async def on_enable(self):
        for db_player in self.db_guild.players:
            await self.roles.assign_player_role(db_player)

    async def on_disable(self):
        await self.roles.strip_guild_roles()
