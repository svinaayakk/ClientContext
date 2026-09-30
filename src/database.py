import sqlite3

DB_PATH = "database/clientcontext.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT UNIQUE,
            client_name TEXT NOT NULL,
            meeting_summary TEXT,
            timeline TEXT,
            budget TEXT,
            sentiment TEXT
        )
    """)

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


def meeting_exists(source_file):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM meetings
        WHERE source_file = ?
    """, (source_file,))

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


def save_meeting(meeting, source_file):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO meetings
        (
            source_file,
            client_name,
            meeting_summary,
            timeline,
            budget,
            sentiment
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        source_file,
        meeting.client_name,
        meeting.meeting_summary,
        meeting.timeline,
        meeting.budget,
        meeting.sentiment
    ))

    meeting_id = cursor.lastrowid

    categories = {
        "pain_point": meeting.pain_points,
        "requirement": meeting.requirements,
        "objection": meeting.objections,
        "decision": meeting.decisions,
        "action_item": meeting.action_items,
        "stakeholder": meeting.stakeholders
    }

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