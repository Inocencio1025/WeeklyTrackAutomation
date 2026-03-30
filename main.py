from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# scopes needed: read playlist items + modify your playlists
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# OAuth flow
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
credentials = flow.run_console()

youtube = build("youtube", "v3", credentials=credentials)

# replace with Fantano playlist ID
playlist_id = "PLP4CSgl7K7or84AAhr7zlLNpghEnKWu2c"

# fetch latest video
request = youtube.playlistItems().list(
    part="snippet",
    playlistId=playlist_id,
    maxResults=1
)
response = request.execute()

video = response["items"][0]["snippet"]
print("Title:", video["title"])
print("Published at:", video["publishedAt"])
print("Video ID:", video["resourceId"]["videoId"])