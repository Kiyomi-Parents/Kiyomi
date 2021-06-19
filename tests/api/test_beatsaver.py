import unittest

from src.api import BeatSaver, NotFoundException


class TestBeatSaver(unittest.TestCase):
    _valid_song_hash = "4BBDAA1004A00EEB9C8D9432640E1C7D490B46D9"
    _invalid_song_hash = "4BDAA104A00E32EB9CD941132640E1C7490B4932"
    _valid_song_key = "19487"
    _invalid_song_key = "153423234235"

    def setUp(self):
        self.beatsaver = BeatSaver()

    def test_get_song_by_hash_valid(self):
        song = self.beatsaver.get_song_by_hash(self._valid_song_hash)
        self.assertEqual(song.hash, str.lower(self._valid_song_hash))

    def test_get_song_by_hash_invalid(self):
        self.assertRaises(NotFoundException, self.beatsaver.get_song_by_hash, self._invalid_song_hash)

    def test_get_song_by_key(self):
        song = self.beatsaver.get_song_by_key(self._valid_song_key)

        self.assertEqual(song.key, self._valid_song_key)

    def test_get_song_by_key_invalid(self):
        self.assertRaises(NotFoundException, self.beatsaver.get_song_by_key, self._invalid_song_key)