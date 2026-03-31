import re


def parse_description(description: str):
    """
    Parse a YouTube video description into categorized track lists.

    The function looks for sections labeled:
    - "Best tracks"
    - "Meh"
    - "Worst tracks"

    It assumes each track is formatted as:
        <track title>
        <url>

    Args:
        description: Full video description text

    Returns:
        dict: {
            "best":  [ { "title": str, "url": str }, ... ],
            "meh":   [ ... ],
            "worst": [ ... ]
        }
    """

    # =========================
    # INITIAL SETUP
    # =========================
    sections = {
        "best": [],
        "meh": [],
        "worst": []
    }

    current_section = None  # Tracks which section we're currently parsing
    track_title = None      # Temporarily stores a title until URL is found

    lines = description.splitlines()

    # =========================
    # MAIN PARSING LOOP
    # =========================
    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        lower = line.lower()

        # =========================
        # SECTION DETECTION
        # =========================
        if "best tracks" in lower:
            current_section = "best"
            continue

        elif "meh" in lower:
            current_section = "meh"
            continue

        elif "worst tracks" in lower:
            current_section = "worst"
            continue

        # =========================
        # TRACK EXTRACTION
        # =========================
        if current_section:
            # If line is a URL → pair with previous title
            if line.startswith("http"):
                if track_title:
                    sections[current_section].append({
                        "title": track_title,
                        "url": line
                    })
                    track_title = None  # Reset after pairing
            else:
                # Otherwise treat as a title
                track_title = line

    return sections