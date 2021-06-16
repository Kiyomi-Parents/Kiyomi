from discord.ext import commands


class NoPrivateMessagesException(commands.CheckFailure):
    pass
