import re

def parse_description(description: str):
    sections = {
        "best": [],
        "meh": [],
        "worst": []
    }

    current_section = None
    track_title = None

    lines = description.splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        lower = line.lower()

        # More robust section detection
        if "best tracks" in lower:
            current_section = "best"
            continue
        elif "meh" in lower:
            current_section = "meh"
            continue
        elif "worst tracks" in lower:
            current_section = "worst"
            continue

        if current_section:
            if line.startswith("http"):
                if track_title:
                    sections[current_section].append({
                        "title": track_title,
                        "url": line
                    })
                    track_title = None
            else:
                track_title = line

    return sections