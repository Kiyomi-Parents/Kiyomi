from discord import Colour

from src.commands.beatsaber.roles.roles import Roles


class RolesCountryRank(Roles):
    def __init__(self, uow, db_guild):
        super().__init__(uow, db_guild)

    @staticmethod
    def get_role_skill_class(db_role):
        return db_role.country_rank_requirement

    @staticmethod
    def get_player_skill_class(db_player):
        return db_player.country_rank_class

    @staticmethod
    def get_role_name(country_rank_class):
        if country_rank_class < 100:
            return f"Country TOP {country_rank_class}+"
        else:
            return f"Country TOP {country_rank_class}"

    async def create_role(self, country_rank_class):
        role = await self.guild.create_role(name=f"{self.get_role_name(country_rank_class)}", colour=Colour.random(),
                                            hoist=True,
                                            reason="Country TOP ranking (BOT)")

        db_role = self.uow.role_repo.add_role(role)
        self.uow.role_repo.set_role_country_rank_requirement(db_role, country_rank_class)

        self.uow.guild_repo.add_role(self.db_guild, db_role)

        return db_role
