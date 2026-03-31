import datetime

def display_video_info(index, video, playlist_name, last_added):
    print(f"Index: {index}")
    print(f"Title: {video['title']}")
    print(f"Published at: {video['publishedAt']}")
    print(f"Playlist: {playlist_name}")
    print(f"Last time best tracks added: {last_added}\n")

def main_menu():
    print("1. Add BEST tracks")
    print("2. Browse MEH/WORSE tracks")
    print("3. Load previous roundup")
    print("4. Change destination playlist")
    print("5. Quit")