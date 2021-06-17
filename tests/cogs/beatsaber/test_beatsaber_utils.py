import unittest

from src.cogs.beatsaber.beatsaber_utils import BeatSaberUtils


class TestUtils(unittest.TestCase):

    def test_scoresaber_id_from_url(self):
        assert BeatSaberUtils.scoresaber_id_from_url("76561198399404309") == "76561198399404309"
        assert BeatSaberUtils.scoresaber_id_from_url("https://scoresaber.com/u/76561198399404309") == "76561198399404309"
        assert BeatSaberUtils.scoresaber_id_from_url("https://scoresaber.com/u/76561198399404309?page=1&sort=2") == "76561198399404309"
        assert BeatSaberUtils.scoresaber_id_from_url("2538637699496776") == "2538637699496776"
        assert BeatSaberUtils.scoresaber_id_from_url("https://scoresaber.com/u/2538637699496776") == "2538637699496776"
        assert BeatSaberUtils.scoresaber_id_from_url("https://scoresaber.com/u/2538637699496776?page=1&sort=1") == "2538637699496776"

    def test_get_max_score(self):
        assert BeatSaberUtils.get_max_score(533) == 483115
        assert BeatSaberUtils.get_max_score(1598) == 1462915
        assert BeatSaberUtils.get_max_score(1406) == 1286275
