import sqlite3

DB_PATH = "database/clientcontext.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Stores information about each meeting
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            meeting_summary TEXT,
            timeline TEXT,
            budget TEXT,
            sentiment TEXT
        )
    """)

    # Stores lists extracted from each meeting
    # e.g. pain points, requirements, objections, etc.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meeting_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_id INTEGER,
            category TEXT,
            item TEXT,
            FOREIGN KEY (meeting_id) REFERENCES meetings(id)
        )
    """)

    conn.commit()
    conn.close()


def save_meeting(meeting):
    conn = get_connection()
    cursor = conn.cursor()

    # Save main meeting information
    cursor.execute("""
        INSERT INTO meetings
        (
            client_name,
            meeting_summary,
            timeline,
            budget,
            sentiment
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        meeting.client_name,
        meeting.meeting_summary,
        meeting.timeline,
        meeting.budget,
        meeting.sentiment
    ))

    # Get ID of the meeting we just inserted
    meeting_id = cursor.lastrowid

    # Information that can contain multiple items
    categories = {
        "pain_point": meeting.pain_points,
        "requirement": meeting.requirements,
        "objection": meeting.objections,
        "decision": meeting.decisions,
        "action_item": meeting.action_items,
        "stakeholder": meeting.stakeholders
    }

    # Save each individual item
    for category, items in categories.items():

        for item in items:

            cursor.execute("""
                INSERT INTO meeting_items
                (
                    meeting_id,
                    category,
                    item
                )
                VALUES (?, ?, ?)
            """, (
                meeting_id,
                category,
                item
            ))

    conn.commit()
    conn.close()

    return meeting_id