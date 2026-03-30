from pytube import Playlist, YouTube

url = "https://www.youtube.com/playlist?list=PLP4CSgl7K7or84AAhr7zlLNpghEnKWu2c"
pl = Playlist(url)

# get the latest video (first in the list)
latest_video_url = pl.video_urls[0]
video = YouTube(latest_video_url)

print("Title:", video.title)
print("Upload date:", video.publish_date)
print("Description (first 300 chars):")
print(video.description[:300])