from typing import Optional, Generic, TypeVar

import discord
from discord import Embed

from src.cogs.scoresaber.messages.components.embeds.improvement_score_embed import (
    ImprovementScoreEmbed,
)
from src.cogs.scoresaber.messages.components.embeds.score_embed import ScoreEmbed
from src.cogs.scoresaber.storage.model.score import Score
from src.kiyomi import Kiyomi
from src.kiyomi.base_component import BaseComponent
from src.kiyomi.base_view import BaseView

T = TypeVar("T", bound=BaseView)


class ScoreButton(BaseComponent[T], discord.ui.Button, Generic[T]):
    def __init__(self, bot: Kiyomi, parent: T, score: Score, previous_score: Optional[Score]):
        self.score = score
        self.previous_score = previous_score

        BaseComponent.__init__(self, bot, parent)
        discord.ui.Button.__init__(
            self,
            custom_id=f"score:button:score:{score.id}",
            label="Score details",
            style=discord.enums.ButtonStyle.primary,
        )

    async def get_embed(self) -> Embed:
        if self.previous_score is not None:
            return ImprovementScoreEmbed(self.bot, self.parent.guild, self.score, self.previous_score)

        return ScoreEmbed(self.bot, self.parent.guild, self.score)

    async def callback(self, interaction: discord.Interaction):
        self.parent.embed = self.get_embed
        await self.parent.update(interaction, button_clicked=self)
