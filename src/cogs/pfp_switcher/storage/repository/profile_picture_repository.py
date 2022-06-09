import json
from os import path
from typing import List, Dict, Optional

from src.kiyomi.base_repository import BaseRepository, TEntity
from ..model.profile_picture import ProfilePicture


class ProfilePictureRepository(BaseRepository):
    _current_pfp_file = "src/cogs/pfp_switcher/current_pfp.json"
    _config_file = "src/cogs/pfp_switcher/profile_pictures.json"

    @staticmethod
    def _load_file(file_path: str) -> Dict:
        if not path.isfile(file_path):
            return {}

        with open(file_path, "r") as file:
            data = file.read()
            if not data.isspace():
                return json.loads(data)

        return {}

    def _load_all(self, group: str) -> List[ProfilePicture]:
        data = self._load_file(self._config_file)
        profile_pictures = []

        for item in data[group]:
            profile_pictures.append(ProfilePicture(item))

        return profile_pictures

    def get_default(self) -> ProfilePicture:
        data = self._load_file(self._config_file)
        return ProfilePicture(data["default"])

    def get_all_seasonal(self) -> List[ProfilePicture]:
        return self._load_all("seasonal")

    def get_all_events(self) -> List[ProfilePicture]:
        return self._load_all("events")

    def get_current_hash(self) -> Optional[str]:
        data = self._load_file(self._current_pfp_file)

        if "current" in data and not data["current"].isspace():
            return data["current"]

        return None

    def set_current_hash(self, pfp_hash: str):
        with open(self._current_pfp_file, "w+") as file:
            data = {"current": pfp_hash}
            json.dump(data, file, indent=4)

    async def get_by_id(self, entity_id: int) -> Optional[TEntity]:
        raise NotImplemented()

    async def get_all(self) -> List[TEntity]:
        raise NotImplemented()

    async def exists(self, entity_id: int) -> bool:
        raise NotImplemented()

    async def add(self, entity: TEntity) -> TEntity:
        raise NotImplemented()

    async def add_all(self, entities: List[TEntity]) -> List[TEntity]:
        raise NotImplemented()

    async def remove(self, entity: TEntity) -> TEntity:
        raise NotImplemented()

    async def remove_by_id(self, entity_id: int) -> Optional[TEntity]:
        raise NotImplemented()

    async def upsert(self, entity: TEntity) -> TEntity:
        raise NotImplemented()

    async def update(self, entity_id: int, values: Dict[str, any]) -> TEntity:
        raise NotImplemented()

    async def update_entity(self, entity: TEntity) -> TEntity:
        raise NotImplemented()
