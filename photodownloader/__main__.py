import os.path
import sys
from typing import List

from photodownloader.src.photo import Photo
from photodownloader.src.photos_client import PhotosClient

CLIENT_SECRETS_FILE_NAME = "client_secrets.json"


def download_photos(photos_client: PhotosClient, backup_folder_path: str, photos: List[Photo]):
    downloaded_photos = 0
    skipped_photos = 0
    error_photos = 0

    for photo in photos:
        try:
            was_downloaded = photos_client.download_photo(backup_folder_path, photo)
        except Exception as e:
            print(f"Error while downloading photo {photo.filename}: {e}")
            error_photos += 1
            continue

        if was_downloaded:
            downloaded_photos += 1
        else:
            skipped_photos += 1

    print("")
    print(f"{downloaded_photos} photos downloaded")
    print(f"{skipped_photos} photos skipped")
    print(f"{error_photos} photos encountered errors")


def main():
    if len(sys.argv) == 1:
        backup_folder_path = ""
    elif len(sys.argv) == 2:
        backup_folder_path = sys.argv[1]
    else:
        print("Incorrect number of arguments.")
        sys.exit(1)

    os.makedirs(backup_folder_path, exist_ok=True)
    print(f"Backing up to location '{backup_folder_path}'")
    photos_client = PhotosClient(CLIENT_SECRETS_FILE_NAME)

    photos = photos_client.get_photos()

    print(f"Found {len(photos)} photos to process...")
    download_photos(photos_client, backup_folder_path, photos)


if __name__ == "__main__":
    main()
