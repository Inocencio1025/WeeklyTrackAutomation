import datetime


# =========================
# DISPLAY / UI
# =========================
def display_video_info(index, video, playlist_name, last_added):
    """
    Print formatted information about a video.

    Args:
        index: Current position in the playlist (0-based)
        video: Dict containing video data (expects 'title', 'publishedAt')
        playlist_name: Name of the playlist the video belongs to
        last_added: Timestamp or label for when it was last used
    """
    print(f"\n[{index + 1}] - Title: {video['title']}")
    print(f"Published at: {video['publishedAt']}")
    print(f"Last used: {last_added}")
    print(f"Playlist: {playlist_name}\n")


def main_menu():
    """
    Display the main menu options for user interaction.

    Options:
        1 - Add BEST tracks
        2 - Browse MEH/WORSE tracks
        3 - Load previous roundup
        4 - Load next roundup
        5 - Change destination playlist
    """
    print("1. Add BEST tracks")
    print("2. Browse MEH/WORSE tracks")
    print("3. Load previous roundup")
    print("4. Load next roundup")
    print("5. Change destination playlist\n")