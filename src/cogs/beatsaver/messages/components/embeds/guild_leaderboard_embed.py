from discord import Embed

from src.cogs.beatsaver.messages.embeds.embed import BeatSaverEmbed
from src.cogs.leaderboard import LeaderboardAPI
from src.kiyomi import Kiyomi


# TODO: handle multiple difficulties somehow

# Should be inside the leaderboard cog
class GuildLeaderboardEmbed(BeatSaverEmbed):
    def __init__(self, bot: Kiyomi, beatmap_id: str):
        super().__init__(bot)

        self.beatmap_id = beatmap_id


    async def get(self):
        pass


    async def get_embed(self, guild_id: int) -> Embed:
        leaderboard = self.bot.get_cog_api(LeaderboardAPI)

        return await leaderboard.get_player_score_leaderboard_embed(guild_id, self.beatmap_id)