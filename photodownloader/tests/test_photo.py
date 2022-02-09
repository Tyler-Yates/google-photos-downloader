from photodownloader.src.photo import Photo


class TestPhoto:
    def test_photo_image_json(self):
        photo_id = "some-id"
        creation_time = "2022-02-08T03:58:10Z"
        photo_json = {
            "id": photo_id,
            "productUrl": "https://photos.google.com/lr/photo/some-photo-id",
            "baseUrl": "https://lh3.googleusercontent.com/lr/some-id",
            "mimeType": "image/jpeg",
            "mediaMetadata": {"creationTime": creation_time, "width": "2939", "height": "1653", "photo": {}},
            "filename": "photo01.jpg",
        }
        photo = Photo(photo_json)

        assert photo_id == photo.id
        assert creation_time == photo.creation_time
        assert 2022 == photo.creation_year
        assert photo.download_url.endswith("=d")

    def test_photo_video_json(self):
        photo_id = "some-id"
        creation_time = "2021-02-08T03:58:10Z"
        photo_json = {
            "id": photo_id,
            "productUrl": "https://photos.google.com/lr/photo/some-photo-id",
            "baseUrl": "https://lh3.googleusercontent.com/lr/some-id",
            "mimeType": "video/mp4",
            "mediaMetadata": {"creationTime": creation_time, "width": "2939", "height": "1653", "photo": {}},
            "filename": "photo01.jpg",
        }
        photo = Photo(photo_json)

        assert photo_id == photo.id
        assert creation_time == photo.creation_time
        assert 2021 == photo.creation_year
        assert photo.download_url.endswith("=dv")
