from src.llm import analyze_meeting
from src.database import create_tables, save_meeting
from src.context import get_meeting_context


# Create database tables
create_tables()


# -----------------------------
# Process Meeting 1
# -----------------------------

with open("data/transcripts/zomato_1.txt", "r") as file:
    transcript_1 = file.read()

result_1 = analyze_meeting(transcript_1)

meeting_id_1 = save_meeting(result_1)

print("\nMeeting 1 saved!")
print("Meeting ID:", meeting_id_1)


# -----------------------------
# Process Meeting 2
# -----------------------------

with open("data/transcripts/zomato_2.txt", "r") as file:
    transcript_2 = file.read()

result_2 = analyze_meeting(transcript_2)

meeting_id_2 = save_meeting(result_2)

print("\nMeeting 2 saved!")
print("Meeting ID:", meeting_id_2)


# -----------------------------
# Retrieve Meeting 2 context
# -----------------------------

context = get_meeting_context(meeting_id_2)

print("\n===== MEETING 2 CONTEXT =====")

for key, value in context.items():
    print(f"\n{key.upper()}:")
    print(value)