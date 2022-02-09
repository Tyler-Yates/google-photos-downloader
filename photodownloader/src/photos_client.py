import os
import pickle
from typing import Optional, Iterator

import google_auth_httplib2
import google_auth_oauthlib.flow
import googleapiclient.discovery
import httplib2
import requests
from google.auth.credentials import Credentials
from google.auth.exceptions import RefreshError

from photodownloader.src.photo import Photo

MAX_RESULTS = 100

CREDENTIALS_FILE = "credentials.pickle"

API_SERVICE_NAME = "photoslibrary"
API_VERSION = "v1"
SCOPES = ["https://www.googleapis.com/auth/photoslibrary.readonly"]

FILE_PREFIXES_TO_SKIP = frozenset(["GOPR"])


class PhotosClient:
    def __init__(self, client_secrets_file_name: str):
        self.file_id_to_path = dict()

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        self.credentials: Optional[Credentials] = None

        # See if the credentials are already saved locally
        if os.path.exists(CREDENTIALS_FILE):
            print("Loading credentials from file...")
            with open(CREDENTIALS_FILE, mode="rb") as credentials_file:
                self.credentials = pickle.load(credentials_file)

        # Try to refresh the token first
        self.refresh_token()

        # If we do not have credentials then we need to fetch them from scratch
        if not self.credentials or not self.credentials.valid:
            # Get credentials and create an API client
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file_name, SCOPES)
            self.credentials = flow.run_local_server()

            # Save the credentials for the next run
            with open(CREDENTIALS_FILE, "wb") as f:
                print("Saving Credentials for future use...")
                pickle.dump(self.credentials, f)

        # Create the Drive client
        self.photos_api = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, credentials=self.credentials, static_discovery=False
        )

    def refresh_token(self):
        if self.credentials and self.credentials.expired and self.credentials.refresh_token:
            # We have expired credentials so we can just refresh them
            print("Refreshing access token...")
            http = httplib2.Http()
            request = google_auth_httplib2.Request(http)
            try:
                self.credentials.refresh(request)
            except RefreshError:
                print("Refresh token has expired. Must generate a new one.")

    @staticmethod
    def _photo_already_exists(backup_folder_path: str, photo: Photo) -> bool:
        subdirectories = [x[0] for x in os.walk(os.path.join(backup_folder_path, str(photo.creation_year)))]
        for subdirectory in subdirectories:
            file_path = os.path.join(subdirectory, photo.filename)
            if os.path.exists(file_path):
                return True

        return False

    def download_photo(self, backup_folder_path: str, photo: Photo) -> bool:
        """
        Downloads the given photo only if it has not already been downloaded.
        The year the photo was created will be used to create sub-folders under the backup folder.

        Args:
            backup_folder_path: The folder to use for backups. A folder for each year will be created.
            photo: The given photo

        Returns:
            True if the photo was downloaded, False if it was skipped
        """
        for prefix in FILE_PREFIXES_TO_SKIP:
            if photo.filename.startswith(prefix):
                print(f"Skipping file {photo.filename} due to prefix match.")
                return False

        photo_year_folder = os.path.join(backup_folder_path, str(photo.creation_year))
        os.makedirs(photo_year_folder, exist_ok=True)

        if self._photo_already_exists(backup_folder_path, photo):
            print(f"Photo {photo.filename} for year {photo.creation_year} already exists. Skipping.")
            return False

        photo_path = os.path.join(photo_year_folder, photo.filename)
        print(f"Path {photo_path} does not exist. Downloading...")
        response = requests.get(
            photo.download_url, allow_redirects=True, headers={"Authorization": f"Bearer {self.credentials.token}"}
        )
        with open(photo_path, "wb") as output_file:
            output_file.write(response.content)
        return True

    def get_photos(self) -> Iterator[Photo]:
        page = 1
        request = self.photos_api.mediaItems().list(pageSize=MAX_RESULTS)
        response = request.execute()
        while response is not None:
            print(f"Loaded page {page}...")
            page += 1
            for photo_json in response["mediaItems"]:
                photo = Photo(photo_json)
                yield photo

            if response.get("nextPageToken"):
                response = (
                    self.photos_api.mediaItems()
                    .list(pageSize=MAX_RESULTS, pageToken=response["nextPageToken"])
                    .execute()
                )
            else:
                response = None
