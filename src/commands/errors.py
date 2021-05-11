from discord.ext import commands


class NoPrivateMessages(commands.CheckFailure):
    pass