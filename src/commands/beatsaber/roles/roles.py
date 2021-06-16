class AlreadyHasRoleException(Exception):
    pass


class RoleNotFoundException(Exception):
    pass


class PermissionDenied(Exception):
    pass


class Roles:

    def __init__(self, uow, db_guild):
        self.uow = uow
        self.guild = self.uow.bot.get_guild(db_guild.discord_guild_id)
        self.db_guild = db_guild

    # TODO: Make into wrapper
    def check_permissions(self):
        guild = self.uow.bot.get_guild(self.db_guild.discord_guild_id)

        if not guild.me.guild_permissions.manage_roles and not self.uow.bot.running_tests:
            raise PermissionDenied(f"{self.uow.bot.user.name} doesn't have permission to manage roles!")

    async def give_player_role(self, db_player, db_role):
        member = await self.guild.fetch_member(db_player.discord_user_id)
        role = self.get_role(db_role)

        self.check_permissions()

        if role not in self.guild.roles:
            raise RoleNotFoundException(f"{self.db_guild} doesn't have {db_role}")

        if role in member.roles:
            if db_role not in db_player.roles:
                self.uow.player_repo.add_role(db_player, db_role)

            raise AlreadyHasRoleException(f"{db_player} already has {db_role}")

        await member.add_roles(role)
        self.uow.player_repo.add_role(db_player, db_role)

    async def remove_player_role(self, db_player, db_role):
        member = await self.guild.fetch_member(db_player.discord_user_id)
        role = self.get_role(db_role)

        self.check_permissions()

        if role not in member.roles:
            if db_role in db_player.roles:
                self.uow.player_repo.remove_role(db_player, db_role)

            raise RoleNotFoundException(f"{db_player} doesn't have {db_role}")

        await member.remove_roles(role, reason="Removed PP ranking (BOT)")
        self.uow.player_repo.remove_role(db_player, db_role)

    async def remove_player_roles(self, db_player, db_roles):
        for db_role in db_roles:
            await self.remove_player_role(db_player, db_role)

    async def remove_guild_role(self, db_role):
        if db_role not in self.db_guild.roles:
            raise RoleNotFoundException(f"{self.db_guild} doesn't have {db_role}")

        role = self.get_role(db_role)
        await role.delete(reason="Disabled PP roles feature (BOT)")
        self.uow.guild_repo.remove_role(self.db_guild, db_role)

    async def remove_guild_roles(self, db_roles):
        for db_role in db_roles:
            await self.remove_guild_role(db_role)

    def get_role(self, db_role):
        return self.guild.get_role(db_role.role_id)

    def find_guild_role(self, pp_class):
        for db_role in self.db_guild.roles:
            if self.get_role_skill_class(db_role) == pp_class:
                return db_role

        return None

    def get_guild_roles(self):
        db_roles = []

        for db_role in self.db_guild.roles:
            if self.get_role_skill_class(db_role) is not None:
                db_roles.append(db_role)

        return db_roles

    def find_player_role(self, db_player):
        for db_role in db_player.roles:
            if db_role not in self.db_guild.roles:
                continue

            if self.get_role_skill_class(db_role) is not None:
                return db_role

        return None

    def get_old_player_roles(self, db_player):
        db_roles = []

        for db_role in db_player.roles:
            if db_role not in self.db_guild.roles:
                continue

            if self.get_role_skill_class(db_role) is None:
                continue

            if self.get_role_skill_class(db_role) != self.get_player_skill_class(db_player):
                db_roles.append(db_role)

        return db_roles

    async def update_player_role(self, db_player):
        db_role = self.find_player_role(db_player)

        if db_role is None:
            await self.assign_player_role(db_player)
        else:
            player_skill_class = self.get_player_skill_class(db_player)
            role_skill_class = self.get_role_skill_class(db_role)

            if player_skill_class != role_skill_class:
                await self.assign_player_role(db_player)
                await self.remove_old_player_roles(db_player)

    async def assign_player_role(self, db_player):
        db_role = self.find_player_role(db_player)

        player_skill_class = self.get_player_skill_class(db_player)

        if db_role is not None:
            role_skill_class = self.get_role_skill_class(db_role)

            if player_skill_class == role_skill_class:
                return

        db_role = self.find_guild_role(player_skill_class)

        if db_role is None:
            db_role = await self.create_role(player_skill_class)

        await self.give_player_role(db_player, db_role)

    async def remove_old_player_roles(self, db_player):
        db_roles = self.get_old_player_roles(db_player)

        await self.remove_player_roles(db_player, db_roles)

    async def strip_player_role(self, db_player):
        db_role = self.find_player_role(db_player)

        await self.remove_player_role(db_player, db_role)

    async def strip_guild_roles(self):
        db_roles = self.get_guild_roles()

        await self.remove_guild_roles(db_roles)

    @staticmethod
    def get_role_skill_class(db_role):
        pass

    @staticmethod
    def get_player_skill_class(db_player):
        pass

    @staticmethod
    def get_role_name(pp_class):
        pass

    async def create_role(self, pp_class):
        pass
