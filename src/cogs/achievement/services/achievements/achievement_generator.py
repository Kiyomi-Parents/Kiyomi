from abc import ABC, abstractmethod
from typing import List

from src.cogs.general.storage.model.member import Member
from src.kiyomi import Kiyomi
from .achievement import Achievement


class AchievementGenerator(ABC):
    def __init__(self, bot: Kiyomi):
        self.bot = bot

    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def get_achievements(self, member: Member) -> List[Achievement]:
        pass
