from discord.ext import commands

from src.cogs.security import Security


class General(commands.Cog):
    async def cog_before_invoke(self, ctx):
        await ctx.trigger_typing()

    @commands.command()
    async def hello(self, ctx):
        """Greet the bot."""
        await ctx.send('Hello there!')

    @commands.command(name="admintest")
    @Security.owner_or_permissions(administrator=True)
    async def admin_test(self, ctx):
        """Command to test if security is working"""
        await ctx.send('This message should only be seen if !admintest was called by a server admin.')


def setup(bot):
    bot.add_cog(General())
