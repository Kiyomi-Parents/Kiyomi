from functools import wraps

from .services import ServiceUnitOfWork
from kiyomi import BaseCog


class FancyPresenceAPI(BaseCog[ServiceUnitOfWork]):
    async def add_task(self, task_text: str):
        await self._service_uow.presences.add_task(task_text)

    async def remove_task(self, task_text: str):
        await self._service_uow.presences.remove_task(task_text)

    @staticmethod
    def presence_task(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            async with self.bot.get_cog_api(FancyPresenceAPI) as fancy_presence:
                task_text = func.__doc__

                if task_text:
                    await fancy_presence.add_task(task_text)

                result = await func(self, *args, **kwargs)

                if task_text:
                    await fancy_presence.remove_task(task_text)

            return result

        return wrapper
