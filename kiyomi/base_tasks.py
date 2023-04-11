import asyncio
from typing import Generic, TypeVar

from discord.backoff import ExponentialBackoff
from discord.ext.tasks import Loop

from .error.error_utils import handle_global_error
from .service import BaseServiceUnitOfWork
from .kiyomi import Kiyomi

TServiceUOW = TypeVar("TServiceUOW", bound=BaseServiceUnitOfWork)


class BaseTasks(Generic[TServiceUOW]):
    def __init__(self, bot: Kiyomi, service_uow: TServiceUOW):
        self.bot = bot
        self.service_uow = service_uow

        for name in dir(self):
            if name.startswith("_"):
                continue

            task = getattr(self, name)

            if not isinstance(task, Loop):
                continue

            task.add_exception_type(Exception)
            task.error(self._on_error)
            task.after_loop(self._after_loop(task))
            task.reconnect = False

    async def _on_error(self, *args):
        error: Exception = args[1]
        await handle_global_error(self.bot, error, print_to_console=False)

    def _after_loop(self, task: Loop):
        backoff = ExponentialBackoff()
        async def wrapper(inner_self, *args):
            await inner_self.service_uow.close()

            if task.failed():
                await asyncio.sleep(backoff.delay())
                task.restart()

        return wrapper
