import json
import random
from typing import List

from src.cogs.fancy_presence.storage.model.presence import Presence


class PresenceRepository:
    @staticmethod
    def _load_file() -> List[Presence]:
        presences = []

        with open("src/cogs/fancy_presence/activities.json", "r") as file:
            for item in json.load(file):
                presences.append(Presence(**item))

        return presences

    def get_all(self) -> List[Presence]:
        return self._load_file()

    def get_random(self) -> Presence:
        presences = self.get_all()

        random_index = random.randint(0, len(presences) - 1)

        return presences[random_index]
