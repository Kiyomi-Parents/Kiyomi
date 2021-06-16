from discord import Colour

from src.commands.beatsaber.roles.roles import Roles


class RolesPP(Roles):
    def __init__(self, uow, db_guild):
        super().__init__(uow, db_guild)

    @staticmethod
    def get_role_skill_class(db_role):
        return db_role.pp_requirement

    @staticmethod
    def get_player_skill_class(db_player):
        return db_player.pp_class

    @staticmethod
    def get_role_name(pp_class):
        if pp_class < 1000:
            return f"<{pp_class} PP club"
        else:
            return f"{pp_class} PP club"

    async def create_role(self, pp_class):
        role = await self.guild.create_role(name=f"{self.get_role_name(pp_class)}", colour=Colour.random(), hoist=True,
                                            reason="PP ranking (BOT)")

        db_role = self.uow.role_repo.add_role(role)
        self.uow.role_repo.set_role_pp_requirement(db_role, pp_class)

        self.uow.guild_repo.add_role(self.db_guild, db_role)

        return db_role
