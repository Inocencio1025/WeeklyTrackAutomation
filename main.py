import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scope gives access to read/modify your YouTube playlists
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Files to store OAuth credentials
TOKEN_FILE = "token.json"      # saved access & refresh tokens
CREDS_FILE = "credentials.json" # client secrets from Google Cloud

creds = None

# Load saved credentials if they exist to avoid logging in every time
if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

# If no valid credentials, refresh them or run OAuth login flow
if not creds or not creds.valid:
    # If creds exist but expired, refresh automatically
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        # Run OAuth flow in browser (first-time login)
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

    # Save credentials for next time so we don't have to log in again
    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())

# Build YouTube API client with authenticated credentials
youtube = build("youtube", "v3", credentials=creds)

# Playlist ID you want to track (Fantano playlist in this case)
playlist_id = "PLP4CSgl7K7or84AAhr7zlLNpghEnKWu2c"

# Prepare API request to get the latest video from the playlist
request = youtube.playlistItems().list(
    part="snippet",       # Get video info like title, publish date, thumbnails
    playlistId=playlist_id,
    maxResults=1          # Only fetch the most recent video
)
response = request.execute()  # Execute the API request

# Extract snippet info from the first (latest) video
video = response["items"][0]["snippet"]

print("Title:", video["title"])
print("Published at:", video["publishedAt"])
print("Video ID:", video["resourceId"]["videoId"])