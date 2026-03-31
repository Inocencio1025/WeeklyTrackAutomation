import datetime
from youtube_api.api import get_authenticated_service, get_video_by_index, get_playlist_name
from ui.ui import display_video_info, main_menu
from data.data import load_data, save_data
from youtube_api.parser import parse_description

def main():
    # grab prev user data
    data = load_data()
    last_added = data.get("last_added", "Never")
    dest_playlist_id = data.get("dest_playlist_id")

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
                print("Adding BEST tracks... (not implemented yet)")
                for t in video_tracks["best"]:
                    add_to_playlist(youtube, dest_playlist_id, t["url"])

                last_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data["last_added"] = last_added
                save_data(data)

        elif choice == "2":
            print("Browsing MEH/WORSE tracks...")

            print("_____MEH tracks_____")
            for t in video_tracks["meh"]:
                print(t["title"], "-", t["url"])

            print("_____WORST tracks_____")
            for t in video_tracks["worst"]:
                print(t["title"], "-", t["url"])

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