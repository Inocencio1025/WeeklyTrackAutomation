import datetime
from youtube_api.api import add_to_playlist, extract_video_id, get_authenticated_service, get_video_by_index, get_playlist_name
from ui.ui import display_video_info, main_menu
from data.data import load_data, save_data
from youtube_api.parser import parse_description

def main():
    # grab user data
    data = load_data()
    last_added = data.get("last_added", "Never")
    dest_playlist_id = data.get("dest_playlist_id")
    added_this_session = set() # to prevent adding duplicates 

    youtube = get_authenticated_service()
    source_playlist_id = "PLP4CSgl7K7or84AAhr7zlLNpghEnKWu2c"

    # index to weekly track roundup playlist
    current_index = 0;
    
    # grab weekly track roundup video
    video = get_video_by_index(youtube, source_playlist_id, current_index)

    # loads lists for best, meh, and worst tracks
    video_tracks = parse_description(video["description"])

    # set playlist name safely
    if dest_playlist_id:
        try:
            playlist_name = get_playlist_name(youtube, dest_playlist_id)
        except Exception:
            playlist_name = "Invalid playlist"
            dest_playlist_id = None
    else:
        playlist_name = "Not set"

    while True:
        video_tracks = parse_description(video["description"])
        
        display_video_info(current_index, video, playlist_name, last_added)
        main_menu()
        choice = input("Select an option: ")

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
                last_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data["last_added"] = last_added
                save_data(data)

        elif choice == "2":
            print("Browsing MEH/WORSE tracks...")

            combined = []

            # Number MEH tracks
            print("\n_____MEH tracks_____")
            for i, t in enumerate(video_tracks["meh"], start=1):
                print(f"{i}. {t['title']}")
                combined.append(t)  # keep track of all tracks

            offset = len(combined)  # start WORST numbering after MEH

            # Number WORST tracks
            print("\n_____WORST tracks_____")
            for i, t in enumerate(video_tracks["worst"], start=offset+1):
                print(f"{i}. {t['title']}")
                combined.append(t)

            # Let user pick
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
                print("No track added.")

        elif choice == "3":  # Load previous roundup
            current_index += 1
            video = get_video_by_index(youtube, source_playlist_id, current_index)
            
            if not video:
                print("No more previous videos.")
                current_index -= 1  # stay at last valid

        elif choice == "4":
            new_id = input("Enter playlist ID: ").strip()
            if new_id:
                try:
                    playlist_name = get_playlist_name(youtube, new_id)
                    dest_playlist_id = new_id
                    data["dest_playlist_id"] = new_id
                    save_data(data)
                except Exception:
                    print("Invalid playlist ID.")

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again.")

        print("\n")

if __name__ == "__main__":
    main()