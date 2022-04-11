import discord
import pybeatsaver
from discord import slash_command, ApplicationContext
from matplotlib import pyplot as plt

from src.cogs.scoresaber import ScoreSaberAPI
from .scoresaber_stats_cog import ScoreSaberStatsCog


class ScoreSaberStats(ScoreSaberStatsCog):
    @slash_command()
    async def player_style_avg_acc_graph(self, ctx: ApplicationContext):
        await ctx.defer()

        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        guild_player = scoresaber.get_guild_player(ctx.interaction.guild.id, ctx.interaction.user.id)

        data = {}
        maps = 0

        for score in guild_player.player.scores:
            beatmap = score.beatmap
            if beatmap is None:
                continue

            tags = beatmap.tags
            if tags is None or len(tags) == 0:
                continue

            added_tag = False
            for tag in score.beatmap.tags:
                if tag.get_type() is pybeatsaver.EMapTagType.STYLE:
                    if tag.human_readable not in data.keys():
                        data[tag.human_readable] = []

                    if score.accuracy is not None and score.accuracy > 0:
                        data[tag.human_readable].append(score.accuracy)

                    added_tag = True

            if added_tag:
                maps += 1

        for key, values in data.items():
            data[key] = (sum(values) / len(values)) / 100

        sorted(data.keys())
        print(data)
        print("done")

        theta = self.spider_graph_service.radar_factory(len(data.keys()), frame='polygon')

        spoke_labels = data.keys()

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
        fig.subplots_adjust(top=0.85, bottom=0.05)

        ax.set_rgrids([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.])
        # ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
        # ax.set_rgrids([i / 10 for i in range(0, 10)])
        ax.set_title(guild_player.player.name, position=(0.5, 1.1), ha='center')

        line = ax.plot(theta, data.values())
        ax.fill(theta, data.values(), alpha=0.25)
        ax.set_varlabels(spoke_labels)

        file_name = f"{guild_player.player.id}_play_genre.png"
        plt.savefig(f"./tmp/{file_name}")

        with open(f"./tmp/{file_name}", "rb") as file:
            await ctx.respond(file=discord.File(file, filename=file_name))

    @slash_command()
    async def player_genre_graph(self, ctx: ApplicationContext):
        await ctx.defer()

        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        guild_player = scoresaber.get_guild_player(ctx.interaction.guild.id, ctx.interaction.user.id)

        data = {}
        maps = 0

        for score in guild_player.player.scores:
            beatmap = score.beatmap
            if beatmap is None:
                continue

            tags = beatmap.tags
            if tags is None or len(tags) == 0:
                continue

            added_tag = False
            for tag in score.beatmap.tags:
                if tag.get_type() is pybeatsaver.EMapTagType.GENRE:
                    if tag.human_readable not in data.keys():
                        data[tag.human_readable] = 0
                    data[tag.human_readable] += 1
                    added_tag = True

            if added_tag:
                maps += 1

        for key, value in data.items():
            data[key] = value / maps

        sorted(data.keys())
        print(data)
        print("done")

        theta = self.spider_graph_service.radar_factory(len(data.keys()), frame='polygon')

        spoke_labels = data.keys()

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
        fig.subplots_adjust(top=0.85, bottom=0.05)

        ax.set_rgrids([i / 10 for i in range(0, 10)], labels=None)
        ax.set_title(guild_player.player.name, position=(0.5, 1.1), ha='center')

        line = ax.plot(theta, data.values())
        ax.fill(theta, data.values(), alpha=0.25)
        ax.set_varlabels(spoke_labels)

        file_name = f"{guild_player.player.id}_play_genre.png"
        plt.savefig(f"./tmp/{file_name}")

        with open(f"./tmp/{file_name}", "rb") as file:
            await ctx.respond(file=discord.File(file, filename=file_name))

    @slash_command()
    async def player_style_graph(self, ctx: ApplicationContext):
        await ctx.defer()

        scoresaber = self.bot.get_cog_api(ScoreSaberAPI)

        guild_player = scoresaber.get_guild_player(ctx.interaction.guild.id, ctx.interaction.user.id)

        data = {}
        maps = 0

        for score in guild_player.player.scores:
            beatmap = score.beatmap
            if beatmap is None:
                continue

            tags = beatmap.tags
            if tags is None or len(tags) == 0:
                continue

            added_tag = False
            for tag in score.beatmap.tags:
                if tag.get_type() is pybeatsaver.EMapTagType.STYLE:
                    if tag.human_readable not in data.keys():
                        data[tag.human_readable] = 0
                    data[tag.human_readable] += 1
                    added_tag = True

            if added_tag:
                maps += 1


        for key, value in data.items():
            data[key] = value / maps

        sorted(data.keys())
        print(data)
        print("done")

        theta = self.spider_graph_service.radar_factory(len(data.keys()), frame='polygon')

        spoke_labels = data.keys()

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
        fig.subplots_adjust(top=0.85, bottom=0.05)

        ax.set_rgrids([i / 10 for i in range(0, 10)], labels=None)
        ax.set_title(guild_player.player.name, position=(0.5, 1.1), ha='center')

        line = ax.plot(theta, data.values())
        ax.fill(theta, data.values(), alpha=0.25)
        ax.set_varlabels(spoke_labels)

        file_name = f"{guild_player.player.id}_play_style.png"
        plt.savefig(f"./tmp/{file_name}")

        with open(f"./tmp/{file_name}", "rb") as file:
            await ctx.respond(file=discord.File(file, filename=file_name))


