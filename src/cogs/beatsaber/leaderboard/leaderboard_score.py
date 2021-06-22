from src.cogs.beatsaber.storage.model.player import Player
from src.cogs.beatsaber.storage.model.score import Score


class LeaderboardScore:

    def __init__(self, db_player: Player, db_score: Score):
        self.db_player = db_player
        self.db_score = db_score
