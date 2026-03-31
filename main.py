import datetime

from youtube_api.api import (
    add_to_playlist,
    extract_video_id,
    get_authenticated_service,
    get_video_by_index,
    get_playlist_name,
)
from ui.ui import display_video_info, main_menu
from data.data import load_data, save_data
from youtube_api.parser import parse_description


def main():
    """
    Main program loop.

    Handles:
    - Loading user data
    - Navigating playlist videos (weekly roundups)
    - Adding tracks to a destination playlist
    - Preventing duplicates within a session
    - Updating saved state
    """

    # =========================
    # INITIAL SETUP
    # =========================
    data = load_data()

    last_added = data.get("last_added", "Never")
    dest_playlist_id = data.get("dest_playlist_id")

    added_this_session = set()  # Prevent duplicate adds per run

    youtube = get_authenticated_service()

    # Source playlist (weekly roundup)
    source_playlist_id = "PLP4CSgl7K7or84AAhr7zlLNpghEnKWu2c"

    # Track current position in playlist (0 = latest)
    current_index = 0

    # Load initial video
    video = get_video_by_index(youtube, source_playlist_id, current_index)

    # Parse tracks from description
    video_tracks = parse_description(video["description"])

    # =========================
    # DESTINATION PLAYLIST SETUP
    # =========================
    if dest_playlist_id:
        try:
            playlist_name = get_playlist_name(youtube, dest_playlist_id)
        except Exception:
            playlist_name = "Invalid playlist"
            dest_playlist_id = None
    else:
        playlist_name = "Not set"

    # =========================
    # MAIN LOOP
    # =========================
    while True:
        # Re-parse in case video changed
        video_tracks = parse_description(video["description"])

        display_video_info(current_index, video, playlist_name, last_added)
        main_menu()

        choice = input("Select an option: ")

        # =========================
        # 1. ADD BEST TRACKS
        # =========================
        if choice == "1":
            if not dest_playlist_id:
                print("Set a destination playlist first.")
            else:
                print("Adding BEST tracks...")

                for t in video_tracks["best"]:
                    video_id = extract_video_id(t["url"])

                    if video_id:
                        if video_id not in added_this_session:
                            add_to_playlist(youtube, dest_playlist_id, video_id)
                            added_this_session.add(video_id)
                            print(f"Added: {t['title']}")
                        else:
                            print(f"Skipped (already added this session): {t['title']}")

                # Update last added timestamp
                last_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data["last_added"] = last_added
                save_data(data)

        # =========================
        # 2. BROWSE MEH/WORST
        # =========================
        elif choice == "2":
            combined = []

            print("\n_____MEH tracks_____")
            for i, t in enumerate(video_tracks["meh"], start=1):
                print(f"{i}. {t['title']}")
                combined.append(t)

            offset = len(combined)

            print("\n_____WORST tracks_____")
            for i, t in enumerate(video_tracks["worst"], start=offset + 1):
                print(f"{i}. {t['title']}")
                combined.append(t)

            # Selection loop
            while True:
                pick = input("\nEnter track number to add (blank to finish): ").strip()

                if not pick:
                    print("Finished adding tracks.\n")
                    break

                if not pick.isdigit():
                    print("Please enter a valid number.")
                    continue

                idx = int(pick) - 1

                if 0 <= idx < len(combined):
                    video_id = extract_video_id(combined[idx]["url"])

                    if video_id not in added_this_session:
                        add_to_playlist(youtube, dest_playlist_id, video_id)
                        added_this_session.add(video_id)
                        print(f"Added: {combined[idx]['title']}")
                    else:
                        print(f"Skipped (already added this session): {combined[idx]['title']}")
                else:
                    print("Invalid track number.")

            else:
                # ⚠️ This never runs (see notes below)
                print("No track added.")

        # =========================
        # 3. PREVIOUS ROUNDUP
        # =========================
        elif choice == "3":
            current_index += 1
            video = get_video_by_index(youtube, source_playlist_id, current_index)

            if not video:
                print("No previous video.")
                current_index -= 1  # Stay at last valid index

        # =========================
        # 4. NEXT ROUNDUP
        # =========================
        elif choice == "4":
            if current_index == 0:
                print("Already at latest video.")
                continue

            current_index -= 1
            video = get_video_by_index(youtube, source_playlist_id, current_index)

            if not video:
                print("No next video.")
                current_index += 1  # Stay at last valid index

        # =========================
        # 5. CHANGE DESTINATION PLAYLIST
        # =========================
        elif choice == "5":
            new_id = input("Enter playlist ID: ").strip()

            if new_id:
                try:
                    playlist_name = get_playlist_name(youtube, new_id)
                    dest_playlist_id = new_id

                    data["dest_playlist_id"] = new_id
                    save_data(data)

                except Exception:
                    print("Invalid playlist ID.")

        # =========================
        # EXIT
        # =========================
        else:
            print("Exiting...")
            break

        print("\n")


if __name__ == "__main__":
    main()