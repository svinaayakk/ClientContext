from src.database import get_connection


def get_meeting_context(meeting_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            client_name,
            meeting_summary,
            timeline,
            budget,
            sentiment
        FROM meetings
        WHERE id = ?
    """, (meeting_id,))

    meeting = cursor.fetchone()

    if not meeting:
        conn.close()
        return None

    cursor.execute("""
        SELECT category, item
        FROM meeting_items
        WHERE meeting_id = ?
    """, (meeting_id,))

    items = cursor.fetchall()

    conn.close()

    context = {
        "client_name": meeting[0],
        "meeting_summary": meeting[1],
        "timeline": meeting[2],
        "budget": meeting[3],
        "sentiment": meeting[4],
        "pain_points": [],
        "requirements": [],
        "objections": [],
        "decisions": [],
        "action_items": [],
        "stakeholders": []
    }

    for category, item in items:

        if category == "pain_point":
            context["pain_points"].append(item)

        elif category == "requirement":
            context["requirements"].append(item)

        elif category == "objection":
            context["objections"].append(item)

        elif category == "decision":
            context["decisions"].append(item)

        elif category == "action_item":
            context["action_items"].append(item)

        elif category == "stakeholder":
            context["stakeholders"].append(item)

    return context


def build_client_memory(previous_context, current_context, context_update):

    memory = {
        "client_name": current_context["client_name"],
        "current_needs": [],
        "resolved_items": [],
        "new_items": [],
        "changed_items": [],
        "timeline": current_context["timeline"],
        "budget": current_context["budget"],
        "stakeholders": current_context["stakeholders"],
        "latest_sentiment": current_context["sentiment"]
    }

    # Current information identified by Gemini
    memory["current_needs"].extend(
        context_update.current
    )

    # Things that are no longer active
    memory["resolved_items"].extend(
        context_update.resolved
    )

    # Newly introduced information
    memory["new_items"].extend(
        context_update.new
    )

    # Information that changed
    memory["changed_items"].extend(
        context_update.changed
    )

    return memory