from typing import Dict


class Photo:
    def __init__(self, photo_json: Dict):
        self.id: str = photo_json["id"]
        self.mime_type: str = photo_json["mimeType"]
        self.filename: str = photo_json["filename"]
        self.creation_time: str = photo_json["mediaMetadata"]["creationTime"]
        self.creation_year = int(self.creation_time.split("-")[0])
        self.download_url = photo_json["baseUrl"] + "=d"
