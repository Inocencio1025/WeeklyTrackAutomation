import os
import re

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# =========================
# CONFIG
# =========================
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN_FILE = "token.json"
CREDS_FILE = "credentials.json"


# =========================
# AUTHENTICATION
# =========================
def get_authenticated_service():
    """
    Authenticate the user with OAuth and return a YouTube API client.

    - Loads saved credentials if available
    - Refreshes them if expired
    - Otherwise runs a browser login flow
    - Saves credentials for future use
    """
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


# =========================
# PLAYLIST ACTIONS
# =========================
def add_to_playlist(youtube, playlist_id, video_id):
    """
    Add a video to a playlist.

    Args:
        youtube: Authenticated YouTube API client
        playlist_id: Target playlist ID
        video_id: ID of the video to add
    """
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
    """
    Retrieve the name (title) of a playlist.

    Args:
        youtube: Authenticated YouTube API client
        playlist_id: Playlist ID

    Returns:
        str: Playlist title
    """
    request = youtube.playlists().list(
        part="snippet",
        id=playlist_id
    )
    response = request.execute()

    return response["items"][0]["snippet"]["title"]


# =========================
# VIDEO FETCHING
# =========================
def get_video_by_index(youtube, playlist_id, index):
    """
    Fetch a video from a playlist by its index.

    Notes:
        - Index 0 = most recent video (top of playlist)
        - Iterates through pages (50 items at a time)

    Args:
        youtube: Authenticated YouTube API client
        playlist_id: Playlist ID
        index: Zero-based index

    Returns:
        dict | None: Video snippet if found, else None
    """
    page_token = None
    current_index = 0  # Tracks position across paginated results

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token
        )
        response = request.execute()
        items = response["items"]

        # Walk through current page
        for item in items:
            if current_index == index:
                return item["snippet"]
            current_index += 1

        # Move to next page if available
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return None  # Index out of range


# =========================
# UTILITIES
# =========================
def extract_video_id(url):
    """
    Extract the YouTube video ID from a URL.

    Supports basic '?v=' format only.

    Args:
        url: YouTube URL

    Returns:
        str | None: Video ID if found
    """
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None