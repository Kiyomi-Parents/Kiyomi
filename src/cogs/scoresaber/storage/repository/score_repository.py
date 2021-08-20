from typing import Optional, List

from pyscoresaber import ScoreSaber

from src.database import Repository
from src.log import Logger
from ..model.score import Score
from ...scoresaber_utils import ScoreSaberUtils


class ScoreRepository(Repository[Score]):

    def get_by_id(self, entry_id: int) -> Optional[Score]:
        return self._db.session.query(Score) \
            .filter(Score.id == entry_id) \
            .first()

    def get_all(self) -> Optional[List[Score]]:
        return self._db.session.query(Score) \
            .all()

    def get_by_score_id(self, score_id: int) -> Optional[Score]:
        return self._db.session.query(Score) \
            .filter(Score.score_id == score_id) \
            .first()

    def get_by_song_hash(self, song_hash: str) -> Optional[Score]:
        return self._db.session.query(Score) \
            .filter(Score.song_hash == song_hash) \
            .first()

    def get_by_player_id_and_leaderboard_id(self, player_id: int, leaderboard_id: int) -> Optional[List[Score]]:
        return self._db.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .filter(Score.leaderboard_id == leaderboard_id) \
            .all()

    def get_all_by_score_id(self, score_id: int) -> Optional[List[Score]]:
        return self._db.session.query(Score) \
            .filter(Score.score_id == score_id) \
            .all()

    def get_scores(self, scores: List[Score]):
        return self._db.session.query(Score) \
            .filter(Score.id.in_([score.id for score in scores])) \
            .all()

    # def get_leaderboard_id_by_hash(self, song_hash: str) -> Optional[int]:
    #     db_score = self._db.session.query(Score).filter(Score.song_hash == song_hash).first()
    #
    #     if db_score is not None:
    #         return db_score.leaderboard_id
    #
    #     return None

    def get_previous_score(self, score: Score) -> Optional[Score]:
        db_scores = self.get_all_by_score_id(score.score_id)
        previous_score = None

        for old_db_score in db_scores:
            if old_db_score.score >= score.score:
                continue

            if previous_score is None:
                previous_score = old_db_score
                continue

            if old_db_score.score > previous_score.score:
                previous_score = old_db_score

        return previous_score

    def get_player_scores(self, player):
        return self._db.session.query(Score).filter(Score.player_id == player.id).all()

    def get_player_scores_without_song(self, player):
        return self._db.session.query(Score) \
            .filter(Score.player_id == player.id) \
            .filter(~Score.song.has()) \
            .all()

    def get_all_player_recent_scores(self, player_id: int) -> List[Score]:
        return self._db.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .order_by(Score.time_set.desc()) \
            .all()

    def get_player_recent_score(self, player_id: int, index: int) -> Score:
        return self._db.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .order_by(Score.time_set.desc()) \
            .offset(index) \
            .first()

    def get_player_recent_scores(self, player_id: int, count: int) -> List[Score]:
        return self._db.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .order_by(Score.time_set.desc()) \
            .limit(count) \
            .all()

    def is_score_new(self, db_score: Score) -> bool:
        """Checks if the score already exists in the database by comparing scoreId and timeSet"""
        scores = self._db.session.query(Score) \
            .filter(Score.score_id == db_score.score_id) \
            .filter(Score.time_set == db_score.time_set) \
            .all()

        return 1 > len(scores)

    def update_score_pp_weight(self, db_score, player_repo):
        pos = ScoreSaberUtils.get_pos_from_pp_weight(db_score.weight)
        player = player_repo.get_player_by_internal_player_id(db_score.player_id)
        page = (pos - 1) // 8
        if type(page) != int or page < 0:
            starting_page = 0

        new_pp_weight = None
        not_found = True
        while not_found:
            page += 1
            scores_list = ScoreSaber.get_top_scores(player.player_id, page)
            for comparing_score in scores_list:
                if comparing_score.pp < db_score.pp:
                    new_pp_weight = ScoreSaberUtils.get_pp_weight_from_pos(
                        ScoreSaberUtils.get_pos_from_pp_weight(comparing_score.weight) - 1)
                    not_found = False
                    break

        db_score.weight = new_pp_weight
        self._db.commit_changes()
        Logger.log(db_score, f"Updated weight to {new_pp_weight}")

        return db_score
