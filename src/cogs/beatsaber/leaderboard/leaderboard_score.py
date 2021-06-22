from src.storage.model import Player, Score


class LeaderboardScore:

    def __init__(self, db_player: Player, db_score: Score):
        self.db_player = db_player
        self.db_score = db_score
