import unittest

from src.cogs.beatsaber.api.errors import NotFoundException
from src.cogs.beatsaber.api.scoresaber import ScoreSaber


class TestScoreSaber(unittest.TestCase):
    valid_player_id = "76561198029447509"
    invalid_player_id = "656119802447509"

    def setUp(self):
        self.scoresaber = ScoreSaber()

    def test_get_player_valid(self):
        player = self.scoresaber.get_player(self.valid_player_id)
        self.assertTrue(player.playerId == self.valid_player_id)

    def test_get_player_invalid(self):
        self.assertRaises(NotFoundException, self.scoresaber.get_player, self.invalid_player_id)

    def test_get_recent_scores_valid(self):
        scores = self.scoresaber.get_recent_scores(self.valid_player_id)
        self.assertGreater(len(scores), 0)

    def test_get_recent_scores_invalid(self):
        self.assertRaises(NotFoundException, self.scoresaber.get_recent_scores, self.invalid_player_id)
