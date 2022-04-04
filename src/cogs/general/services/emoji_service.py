from .general_service import GeneralService
from ..storage.model.emoji import Emoji


class EmojiService(GeneralService):

    async def register_emoji(self, guild_id: int, emoji_id: int, emoji_name: str) -> Emoji:
        emoji = self.uow.emojis.add(Emoji(guild_id, emoji_id, emoji_name))
        self.uow.save_changes()

        return emoji

    async def unregister_emoji(self, guild_id: int, emoji_id: int) -> Emoji:
        emoji = self.uow.emojis.get_by_guild_id_and_id(guild_id, emoji_id)

        if emoji is not None:
            self.uow.emojis.remove(emoji)

        return emoji
