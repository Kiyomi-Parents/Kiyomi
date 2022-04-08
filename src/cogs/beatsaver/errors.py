from src.kiyomi.errors import CogException


class BeatSaverCogException(CogException):
    pass


class BeatmapNotFound(BeatSaverCogException):
    pass


class BeatmapKeyNotFound(BeatmapNotFound):
    def __init__(self, beatmap_key: str):
        self.beatmap_key = beatmap_key

    def __str__(self):
        return f"Could not find a beatmap using key {self.beatmap_key}"


class BeatmapHashNotFound(BeatmapNotFound):
    def __init__(self, beatmap_hash: str):
        self.beatmap_hash = beatmap_hash

    def __str__(self):
        return f"Could not find a beatmap using hash {self.beatmap_hash}"
