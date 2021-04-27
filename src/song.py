class Song:

    def __init__(self, songJson):
        self.metadata = songJson["metadata"]
        self.stats = songJson["stats"]
        self.description = songJson["description"]
        self.deletedAt = songJson["deletedAt"]
        self._id = songJson["_id"]
        self.key = songJson["key"]
        self.name = songJson["name"]
        self.uploader = songJson["uploader"]
        self.hash = songJson["hash"]
        self.uploaded = songJson["uploaded"]
        self.directDownload = songJson["directDownload"]
        self.downloadURL = songJson["downloadURL"]
        self.coverURL = songJson["coverURL"]

    @property
    def beatsaver_url(self):
        return f"https://beatsaver.com/beatmap/{self.key}"

    @property
    def preview_url(self):
        return f"https://skystudioapps.com/bs-viewer/?id={self.key}"
