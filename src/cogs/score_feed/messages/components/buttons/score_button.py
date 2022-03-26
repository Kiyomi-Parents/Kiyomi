import discord
from discord import Embed

from src.cogs.score_feed.messages.components.embeds.score_embed import ScoreEmbed
from src.cogs.score_feed.messages.components.score_feed_component import ScoreFeedComponent
from src.cogs.scoresaber.storage.model.score import Score
from src.kiyomi import Kiyomi


class ScoreButton(ScoreFeedComponent, discord.ui.Button):
    def __init__(self, bot: Kiyomi, parent, score: Score, previous_score: Score):
        ScoreFeedComponent.__init__(self, bot, parent, score, previous_score)
        discord.ui.Button.__init__(
            self,
            custom_id=f"score:button:score:{score.id}",
            label="Score details",
            style=discord.enums.ButtonStyle.primary,
        )

    def get_embed(self) -> Embed:
        return ScoreEmbed(self.bot, self.parent.guild, self.score, self.previous_score)

    async def callback(self, interaction: discord.Interaction):
        self.parent.embed = self.get_embed
        await self.parent.update()
