from discord import Colour

from src.cogs.beatsaber.roles.roles import Roles


class RolesCountryRank(Roles):

    @staticmethod
    def get_role_skill_class(db_role):
        return db_role.country_rank_requirement

    @staticmethod
    def get_player_skill_class(db_player):
        return db_player.country_rank_class

    @staticmethod
    def get_role_name(skill_class):
        if skill_class < 100:
            return f"Country TOP {skill_class}+"

        return f"Country TOP {skill_class}"

    async def create_role(self, skill_class):
        role = await self.guild.create_role(name=f"{self.get_role_name(skill_class)}",
                                            colour=Colour.random(),
                                            hoist=True,
                                            reason="Country TOP ranking (BOT)")

        db_role = self.uow.role_repo.add_role(role)
        self.uow.role_repo.set_role_country_rank_requirement(db_role, skill_class)

        self.uow.guild_repo.add_role(self.db_guild, db_role)

        return db_role
