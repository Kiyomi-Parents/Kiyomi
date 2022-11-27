from typing import Optional

from kiyomi.cogs.general.storage.model.guild import Guild
from kiyomi.cogs.scoresaber.messages.components.embeds.score_embed import ScoreEmbed
from kiyomi.cogs.scoresaber.storage.model.score import Score
from kiyomi import Kiyomi


class ImprovementScoreEmbed(ScoreEmbed):
    def __init__(self, bot: Kiyomi, guild: Guild, score: Score, previous_score: Score):
        self.previous_score = previous_score

        super().__init__(bot, guild, score)

        self.title = f"Improved • #{previous_score.rank} ▸ #{score.rank} • {score.leaderboard.song_name_full} • {score.leaderboard.difficulty_name}"

    @property
    def get_pp(self) -> Optional[str]:
        if self.score.pp > 0:
            pp = round(self.score.pp, 2)
            output = f"**{pp} PP**"

            pp_improvement = round(self.score.pp - self.previous_score.pp, 2)

            if pp_improvement > 0:
                output += f" +{pp_improvement} PP"
            elif pp_improvement < 0:
                output += f" {pp_improvement} PP"

            weighted_pp = self.get_weighted_pp

            if weighted_pp is None:
                return f"{output}"

            return f"{output} {weighted_pp}"

        return None

    @property
    def get_weighted_pp(self) -> Optional[str]:
        if self.score.weighted_pp > 0:
            output = f"{self.score.weighted_pp} PP"

            weighted_pp_improvement = round(self.score.weighted_pp - self.previous_score.weighted_pp, 2)

            if weighted_pp_improvement > 0:
                output += f" +{weighted_pp_improvement} PP"
            elif weighted_pp_improvement < 0:
                output += f" {weighted_pp_improvement} PP"

            return f"_({output})_"

        return None

    @property
    def get_accuracy(self) -> Optional[str]:
        if self.score.accuracy is None:
            return None

        output = f"{self.score.accuracy}%"

        if self.previous_score.accuracy is None:
            return output

        accuracy_improvement = round(self.score.accuracy - self.previous_score.accuracy, 2)
        improvement_output = None

        if accuracy_improvement > 0:
            improvement_output = f"+{accuracy_improvement}%"
        elif accuracy_improvement < 0:
            improvement_output = f"{accuracy_improvement}%"

        if improvement_output is None:
            return f"**{output}**"

        return f"**{output}** {improvement_output}"

    @property
    def get_modifiers(self) -> Optional[str]:
        if self.score.modifiers is None or len(self.score.modifiers) <= 0:
            return None

        modifiers = self.score.modifiers.split(",")

        if self.previous_score.modifiers is None or len(self.previous_score.modifiers) <= 0:
            return ", ".join(modifiers)

        previous_modifiers = self.previous_score.modifiers.split(",")

        all_modifiers = []

        for modifier in modifiers:
            if modifier not in previous_modifiers:
                all_modifiers.append(f"+{modifier}")
            else:
                all_modifiers.append(f"{modifier}")

        for previous_modifier in previous_modifiers:
            if previous_modifier not in modifiers:
                all_modifiers.append(f"-{previous_modifier}")

        return ", ".join(all_modifiers)

    @staticmethod
    def get_number_improvement(current: int, previous: int) -> Optional[str]:
        if current <= 0 and previous <= 0:
            return None

        output = f"{current}"

        number_improvement = current - previous
        improvement_output = None

        if number_improvement > 0:
            improvement_output = f"+{number_improvement}"
        elif number_improvement < 0:
            improvement_output = f"{number_improvement}"

        if improvement_output is None:
            return f"**{output}**"

        return f"**{output}** {improvement_output}"

    @property
    def get_bad_cuts(self) -> Optional[str]:
        return self.get_number_improvement(self.score.bad_cuts, self.previous_score.bad_cuts)

    @property
    def get_missed_notes(self) -> Optional[str]:
        return self.get_number_improvement(self.score.missed_notes, self.previous_score.missed_notes)

    @property
    def get_max_combo(self) -> str:
        output = f"{self.score.max_combo}"

        if self.score.full_combo:
            output += f" (FC)"

        max_combo_improvement = self.score.max_combo - self.previous_score.max_combo
        improvement_output = None

        if max_combo_improvement > 0:
            improvement_output = f"+{max_combo_improvement}"
        elif max_combo_improvement < 0:
            improvement_output = f"{max_combo_improvement}"

        if improvement_output is None:
            return f"**{output}**"

        return f"**{output}** {improvement_output}"
