import hashlib
from typing import List, Dict

from .active_zone import ActiveZone


class ProfilePicture:
    name: str
    file_path: str
    active_zones: List[ActiveZone] = []

    def __init__(self, data: Dict):
        self.name = data["name"]
        self.file_path = data["file_path"]

        if "active_zones" in data:
            for active_zone in data["active_zones"]:
                self.active_zones.append(ActiveZone(active_zone))

    @property
    def hash(self) -> str:
        with open(self.file_path, "rb") as file:
            sha1_hash = hashlib.sha1(file.read())
            return sha1_hash.hexdigest()
