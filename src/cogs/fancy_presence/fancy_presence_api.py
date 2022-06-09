from functools import wraps

from src.cogs.fancy_presence.fancy_presence_cog import FancyPresenceCog


class FancyPresenceAPI(FancyPresenceCog):
    async def add_task(self, task_text: str):
        await self.presence_service.add_task(task_text)

    async def remove_task(self, task_text: str):
        await self.presence_service.remove_task(task_text)

    @staticmethod
    def presence_task(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            fancy_presence = self.bot.get_cog_api(FancyPresenceAPI)

            task_text = func.__doc__

            if task_text:
                await fancy_presence.add_task(task_text)

            result = await func(self, *args, **kwargs)

            if task_text:
                await fancy_presence.remove_task(task_text)

            return result

        return wrapper
