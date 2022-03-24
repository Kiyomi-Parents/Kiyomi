import discord
from discord import Embed

from src.cogs.beatsaver.messages.components.beatsaver_component import BeatSaverComponent
from src.cogs.beatsaver.messages.components.embeds.map_details_embed import MapDetailsEmbed
from src.cogs.beatsaver.storage import Beatmap
from src.kiyomi import Kiyomi


class MapDetailsButton(BeatSaverComponent, discord.ui.Button):
    def __init__(self, bot: Kiyomi, parent, beatmap: Beatmap):
        BeatSaverComponent.__init__(self, bot, parent, beatmap)
        discord.ui.Button.__init__(
            self,
            custom_id=f"map:detail:button:beatmap:{beatmap.id}",
            label="Map details",
            style=discord.enums.ButtonStyle.primary,
        )

    def get_embed(self) -> Embed:
        return MapDetailsEmbed(self.bot, self.parent.guild, self.beatmap, self.parent.beatmap_characteristic, self.parent.beatmap_difficulty)

    async def callback(self, interaction: discord.Interaction):
        self.parent.embed = self.get_embed
        await self.parent.update()
