from discord import Embed, Colour


class Message:

    @staticmethod
    def get_new_score_embed(player, score, song):
        embed = Embed()
        embed.set_author(name=player.playerName, url=player.profile_url, icon_url=player.avatar_url)
        embed.title = f"New #{score.rank} for {score.song_name_full} on {score.difficulty_name}"

        if song is not None:
            embed.description = F"Mapped by {song.author}"

        embed.add_field(name="PP", value=f"**{round(score.pp, 2)}pp** _({score.weighted_pp}pp)_")
        embed.add_field(name="Accuracy", value=f"**{score.accuracy}%**")
        embed.add_field(name="Score", value=f"{score.score}")

        if score.mods:
            embed.add_field(name="Modifiers", value=f"{score.mods}")

        embed.set_thumbnail(url=score.song_image_url)
        embed.colour = Colour.random(seed=player.playerId)
        embed.url = score.leaderboard_url

        if song is not None:
            embed.add_field(name="\u200b", value=f"[Beat Saver]({song.beatsaver_url})")
            embed.add_field(name="\u200b", value=f"[Preview Map]({song.preview_url})")

        return embed

    @staticmethod
    def get_improvement_score_embed(player, previous_score, score, song):
        embed = Embed()
        embed.set_author(name=player.playerName, url=player.profile_url, icon_url=player.avatar_url)
        embed.title = f"Improved from #{previous_score.rank} to #{score.rank} for {score.song_name_full} on {score.difficulty_name}"

        if song is not None:
            embed.description = F"Mapped by {song.author}"

        pp_improvement = round(score.pp - previous_score.pp, 2)
        weighted_pp_improvement = round(score.weighted_pp - previous_score.weighted_pp, 2)

        embed.add_field(name="PP", value=f"**{round(score.pp, 2)}pp** +{pp_improvement}pp\n_({score.weighted_pp}pp +{weighted_pp_improvement}pp)_")

        accuracy_improvement = round(score.accuracy - previous_score.accuracy, 2)
        embed.add_field(name="Accuracy", value=f"**{score.accuracy}%** _+{accuracy_improvement}%_")

        score_improvement = score.score - previous_score.score
        embed.add_field(name="Score", value=f"{score.score} _+{score_improvement}_")

        if score.mods:
            embed.add_field(name="Modifiers", value=f"{score.mods}")

        embed.set_thumbnail(url=score.song_image_url)
        embed.colour = Colour.random(seed=player.playerId)
        embed.url = score.leaderboard_url

        if song is not None:
            embed.add_field(name="\u200b", value=f"[Beat Saver]({song.beatsaver_url})")
            embed.add_field(name="\u200b", value=f"[Preview Map]({song.preview_url})")

        return embed

    @staticmethod
    def get_song_embed(song):
        embed = Embed()

        embed.set_author(name=song.author, url=song.author_url)
        embed.title = f"{song.name}"

        embed.add_field(name="Rating", value=f"{song.rating}%")
        embed.add_field(name="Downloads", value=f"{song.downloads}")
        embed.add_field(name="Length", value=f"{song.length}")
        embed.add_field(name="BPM", value=f"{song.bpm}")

        embed.add_field(name="difficulties", value=" ".join(f"**{diff}**" for diff in song.difficulties_short))

        # Should make a simple website that redirects the user to the right links
        # discord doesn't want to make app links clickable
        # This will include OneClick links and beatmap download links
        embed.add_field(name="\u200b", value=f"[Preview Map]({song.preview_url})")

        embed.set_thumbnail(url=song.cover_url)
        embed.colour = Colour.random(seed=song.author_id)
        embed.url = song.beatsaver_url

        return embed
