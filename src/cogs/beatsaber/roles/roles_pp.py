from discord import Colour

from src.cogs.beatsaber.roles.roles import Roles


class RolesPP(Roles):

    @staticmethod
    def get_role_skill_class(db_role):
        return db_role.pp_requirement

    @staticmethod
    def get_player_skill_class(db_player):
        return db_player.pp_class

    @staticmethod
    def get_role_name(skill_class):
        if skill_class < 1000:
            return f"<{skill_class} PP club"

        return f"{skill_class} PP club"

    async def create_role(self, skill_class):
        role = await self.guild.create_role(name=f"{self.get_role_name(skill_class)}", colour=Colour.random(), hoist=True,
                                            reason="PP ranking (BOT)")

        db_role = self.uow.role_repo.add_role(role)
        self.uow.role_repo.set_role_pp_requirement(db_role, skill_class)

        self.uow.guild_repo.add_role(self.db_guild, db_role)

        return db_role
