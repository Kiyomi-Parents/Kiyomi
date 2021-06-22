from src.cogs.beatsaber.storage.model.discord_role import DiscordRole
from src.log import Logger


class RoleRepository:

    def __init__(self, database):
        self._db = database

    def get_role(self, role_id):
        return self._db.session.query(DiscordRole).filter(DiscordRole.role_id == role_id).first()

    def add_role(self, role):
        db_role = DiscordRole(role)
        self._db.add_entry(db_role)

        return self.get_role(role.id)

    def set_role_pp_requirement(self, db_role, pp_requirement):
        db_role.pp_requirement = pp_requirement

        self._db.commit_changes()
        Logger.log(db_role, f"Set pp_requirement to {pp_requirement}")

    def set_role_rank_requirement(self, db_role, rank_requirement):
        db_role.rank_requirement = rank_requirement

        self._db.commit_changes()
        Logger.log(db_role, f"Set rank_requirement to {rank_requirement}")

    def set_role_country_rank_requirement(self, db_role, country_rank_requirement):
        db_role.country_rank_requirement = country_rank_requirement

        self._db.commit_changes()
        Logger.log(db_role, f"Set country_rank_requirement to {country_rank_requirement}")
