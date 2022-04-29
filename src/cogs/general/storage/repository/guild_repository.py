from typing import Optional, List

from sqlalchemy.orm import Query

from ..model.guild import Guild
from src.kiyomi.database import BaseRepository


class GuildRepository(BaseRepository[Guild]):
    async def query_by_id(self, entry_id: int) -> Query:
        async with self.session.begin():
            return await self.session.query(Guild) \
                .filter(Guild.id == entry_id)

    async def get_all(self) -> Optional[List[Guild]]:
        async with self.session.begin():
            return await self.session.query(Guild) \
                .all()
