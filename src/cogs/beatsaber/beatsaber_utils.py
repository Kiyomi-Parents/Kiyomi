import math
import re

from src.cogs.beatsaber.feature.feature_pp_roles import FeaturePPRoles
from src.cogs.beatsaber.roles.roles_pp import RolesPP


class BeatSaberUtils:
    @staticmethod
    def scoresaber_id_from_url(url):
        pattern = re.compile(r"(https?://scoresaber\.com/u/)?(\d{16,17})")
        match = re.match(pattern, url)

        if match:
            return match.group(2)

        return None

    @staticmethod
    def get_max_score(blocks, max_score_per_block=115):
        max_score = 0

        if blocks >= 14:
            max_score += 8 * max_score_per_block * (blocks - 13)

        if blocks >= 6:
            max_score += 4 * max_score_per_block * (min(blocks, 13) - 5)

        if blocks >= 2:
            max_score += 2 * max_score_per_block * (min(blocks, 5) - 1)

        max_score += min(blocks, 1) * max_score_per_block

        return math.floor(max_score)

    @staticmethod
    def is_player_in_guild(db_player, guild_id):
        for db_guild in db_player.guilds:
            if db_guild.discord_guild_id == guild_id:
                return True

        return False

    @staticmethod
    def get_enabled_roles(uow, db_guild):
        roles_class = []

        if db_guild.pp_roles:
            roles_class.append(RolesPP(uow, db_guild))

        # Add support for these later. Need to figure out how to perform sql migrations....
        # if db_guild.rank_roles:
        #     roles_class.append(RolesRank(uow, db_guild))
        #
        # if db_guild.country_rank_roles:
        #     roles_class.append(RolesCountryRank(uow, db_guild))

        return roles_class

    @staticmethod
    def get_feature(feature_flag):
        feature_flags = [
            {
                "flag": "pp_roles",
                "feature": FeaturePPRoles
            },
            # Add support for these later. Need to figure out how to perform sql migrations....
            # {
            #     "flag": "rank_roles",
            #     "feature": FeatureRankRoles
            # },
            # {
            #     "flag": "country_rank_roles",
            #     "feature": FeatureCountryRankRoles
            # }
        ]

        for item in feature_flags:
            if item["flag"] == feature_flag:
                return item["feature"]

        return None
