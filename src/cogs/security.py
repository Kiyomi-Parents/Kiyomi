from discord.ext import commands


class Security:
    @staticmethod
    def is_running_tests():
        def check(ctx):
            return ctx.bot.running_tests

        return commands.check(check)

    @staticmethod
    def is_guild_owner():
        def check(ctx):
            if ctx.guild is None:
                return False

            return ctx.guild.owner_id == ctx.author.id

        return commands.check(check)

    @staticmethod
    def is_owner():
        return commands.is_owner()

    @staticmethod
    def can_edit_roles():
        return commands.has_permissions(manage_roles=True)

    @staticmethod
    def owner_or_permissions(**perms):
        return commands.check_any(
                commands.has_permissions(**perms),
                commands.is_owner(),
                Security.is_guild_owner(),
                Security.is_running_tests()
        )
