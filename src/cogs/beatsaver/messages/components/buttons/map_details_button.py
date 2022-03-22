import discord
import pybeatsaver
from pyee import AsyncIOEventEmitter

from src.cogs.beatsaver.messages.components.beatsaver_component import BeatSaverComponent
from src.cogs.beatsaver.messages.components.embeds.map_details_embed import MapDetailsEmbed
from src.cogs.beatsaver.storage import Beatmap
from src.kiyomi import Kiyomi


class MapDetailsButton(BeatSaverComponent, discord.ui.Button):
    def __init__(self, bot: Kiyomi, beatmap: Beatmap, events: AsyncIOEventEmitter):
        BeatSaverComponent.__init__(self, bot, events, beatmap)
        discord.ui.Button.__init__(self,
            label="Map details",
            style=discord.enums.ButtonStyle.primary,
            custom_id=str(f"map_details_button_{beatmap.id}"),
        )

        self.beatmap_difficulty = beatmap.latest_version.difficulties[-1].difficulty

        self.register_events()

    def register_events(self):
        @self.events.on("on_difficulty_update")
        async def update_embed(interaction: discord.Interaction, beatmap_difficulty: pybeatsaver.Difficulty):
            print("end before")
            self.beatmap_difficulty = beatmap_difficulty
            await interaction.response.edit_message(embed=self.get_embed())
            print("end after")

    def get_embed(self):
        return MapDetailsEmbed(self.bot, self.beatmap, self.beatmap_difficulty)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.get_embed())
