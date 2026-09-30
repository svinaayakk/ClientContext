import os

from src.llm import analyze_meeting
from src.database import (
    create_tables,
    save_meeting,
    meeting_exists
)


TRANSCRIPT_DIR = "data/transcripts"


def process_transcript(filename):

    source_file = os.path.basename(filename)

    existing_id = meeting_exists(source_file)

    if existing_id:
        print(f"Skipping {source_file} — already processed (Meeting ID: {existing_id})")
        return existing_id

    print(f"\nAnalyzing {source_file}...")

    with open(filename, "r") as file:
        transcript = file.read()

    result = analyze_meeting(transcript)

    meeting_id = save_meeting(
        result,
        source_file
    )

    print(f"Saved {source_file} as Meeting ID: {meeting_id}")

    return meeting_id


def main():

    create_tables()

    transcripts = sorted(
        filename
        for filename in os.listdir(TRANSCRIPT_DIR)
        if filename.endswith(".txt")
    )

    if not transcripts:
        print("No transcripts found.")
        return

    print(f"Found {len(transcripts)} transcript(s).")

    for filename in transcripts:

        filepath = os.path.join(
            TRANSCRIPT_DIR,
            filename
        )

        process_transcript(filepath)


if __name__ == "__main__":
    main()