from src.cogs.beatsaber.feature.feature import Feature


class FeatureGuildSnipes(Feature):
    def __init__(self, uow, db_guild):
        super().__init__(uow, db_guild, "guild_snipes")
