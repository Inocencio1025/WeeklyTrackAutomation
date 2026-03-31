import os
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_FILE = "token.json"
CREDS_FILE = "credentials.json"

def get_authenticated_service():
    """Authenticate and return a YouTube API client"""
    creds = None
    # Load saved credentials if they exist
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Refresh or login if credentials are invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for next time
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    
    # Return authenticated YouTube API client
    return build("youtube", "v3", credentials=creds)


def add_to_playlist(youtube, playlist_id, video_id):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    ).execute()

def get_playlist_name(youtube, playlist_id):
    request = youtube.playlists().list(
        part="snippet",
        id=playlist_id
    )
    response = request.execute()
    return response["items"][0]["snippet"]["title"]

def get_video_by_index(youtube, playlist_id, index):
    """Fetch a video at a specific index (0 = latest)"""
    
    page_token = None
    current_index = 0

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token
        )
        response = request.execute()

        items = response["items"]

        for item in items:
            if current_index == index:
                return item["snippet"]
            current_index += 1

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return None  # index out of range


def extract_video_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None