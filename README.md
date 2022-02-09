# google-photos-downloader

![tox workflow](https://github.com/Tyler-Yates/google-photos-downloader/actions/workflows/tox-workflow.yml/badge.svg)

Simple Python application to save Pictures from Google Photos.

## Authentication

Fetching the user's files requires authentication, so you will need to set up OAuth flow.

1. Create a new project in [Google Cloud Platform](https://console.cloud.google.com/apis/dashboard).
2. Add the "Photos Library API" to your project with ".../auth/photoslibrary.readonly" scope.
3. Configure the OAuth consent screen to "External" User Type
4. Create a new OAuth credential.
5. Add your desired Google account as a test user for your application.
6. Save the client secrets JSON file to the root of this repository with the name `client_secrets.json`.
7. This file is in `.gitignore` so it should not be committed to the repository.

## Local Setup

In a terminal, go to the root of this repository.

Create a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

Install requirements:
```
pip install -r requirements.txt
```

## Running

Run the program from the root of the repository:
```
python3 -m photodownloader <backup-directory>
```

Open the link and accept the authentication request.
The program will save the credential to disk as a file called `credentials.pickle`.
This file is in `.gitignore` so it should not be committed to the repository.

On future executions of this program, the `credentials.pickle` file will be loaded, so you should not need to go through
the OAuth flow again until it expires.
