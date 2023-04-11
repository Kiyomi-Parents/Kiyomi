import sys
import traceback
from typing import Union, Optional, TYPE_CHECKING

from discord import Interaction
from discord.ext.commands import Context

from ..utils import Utils
from .error_embed import ErrorEmbed

if TYPE_CHECKING:
    from ..kiyomi import Kiyomi


async def handle_global_error(
    bot: "Kiyomi",
    error: Exception,
    ctx: Optional[Union[Context["Kiyomi"], Interaction]] = None,
    print_to_console: Optional[bool] = False
):
    if print_to_console:
        print_error_to_console(error)

    await send_owners_dm_with_stacktrace(bot, error)

    if ctx is not None:
        await send_unexpected_exception(ctx)


def get_formatted_exception(error: Exception):
    return "".join(traceback.format_exception(type(error), error, error.__traceback__))


async def send_owners_dm_with_stacktrace(bot: "Kiyomi", error: Exception):
    stacktrace = get_formatted_exception(error)
    text = f"```python\n{stacktrace}```"

    for owner in await bot.owners:
        if len(text) > 2000:
            await owner.send(file=Utils.text_to_file(stacktrace, "tmp_stacktrace.py"))
        else:
            await owner.send(text)


async def send_unexpected_exception(ctx: Union[Context["Kiyomi"], Interaction]):
    error_embed = ErrorEmbed("Something went horribly wrong, Kiyomi has fallen out of her box!")

    await send_exception(ctx, embed=error_embed, ephemeral=True)


async def send_exception(ctx: Union[Context["Kiyomi"], Interaction], **options):
    if isinstance(ctx, Context):
        await ctx.send(**options)
    elif isinstance(ctx, Interaction):
        if ctx.is_expired() or ctx.response.is_done():
            await ctx.followup.send(**options)
        else:
            await ctx.response.send_message(**options)


def print_error_to_console(error: Exception):
    traceback.print_exception(error.__class__, error, error.__traceback__, file=sys.stderr)
    print(get_formatted_exception(error))
