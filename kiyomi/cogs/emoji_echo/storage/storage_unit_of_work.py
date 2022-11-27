from sqlalchemy.ext.asyncio import AsyncSession

from .repository.echo_emoji_repository import EchoEmojiRepository
from kiyomi import BaseStorageUnitOfWork


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.echo_emojis = EchoEmojiRepository(self._session)
