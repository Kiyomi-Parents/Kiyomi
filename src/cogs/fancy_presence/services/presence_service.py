from typing import List, Optional

import discord
from discord import BaseActivity

from src.log import Logger
from .fancy_presence_service import FancyPresenceService
from ..storage.model.presence import Presence


class PresenceService(FancyPresenceService):
    running_tasks: List[str] = []
    static_presence: Optional[Presence] = None

    def get_activity(self, presence: Presence) -> BaseActivity:
        return presence.activity_class(name=presence.activity_text)

    def get_task_activity(self) -> BaseActivity:
        tasks = " • ".join(self.running_tasks)

        return discord.Game(tasks)

    def get_idle_activity(self) -> BaseActivity:
        presence = self.uow.presences.get_random()

        return self.get_activity(presence)

    # Maybe needs a debouncer?
    async def update_status(self):
        activity = None

        if self.static_presence is not None:
            activity = self.get_activity(self.static_presence)
        elif self.running_tasks:
            activity = self.get_task_activity()
        else:
            activity = self.get_idle_activity()

        await self.bot.change_presence(activity=activity)

        Logger.log("Fancy Presence", f"Set presence to: {activity}")

    async def add_task(self, task_text: str):
        if task_text not in self.running_tasks:
            self.running_tasks.append(task_text)

        await self.update_status()

    async def remove_task(self, task_text: str):
        self.running_tasks.remove(task_text)

        await self.update_status()

    async def set_presence(self, presence: Presence):
        self.static_presence = presence

        await self.update_status()

    async def reset_presence(self):
        self.static_presence = None

        await self.update_status()
