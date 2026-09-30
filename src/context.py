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

        # Current state
        "current_needs": [],
        "timeline": current_context["timeline"],
        "budget": current_context["budget"],
        "stakeholders": current_context["stakeholders"],
        "latest_sentiment": current_context["sentiment"],

        # Change history
        "resolved_items": context_update.resolved,
        "new_items": context_update.new,
        "changed_items": context_update.changed
    }

    # Start with the latest meeting's requirements.
    memory["current_needs"].extend(
        current_context["requirements"]
    )

    # Add important current items identified by the comparison.
    for item in context_update.current:

        if item not in memory["current_needs"]:
            memory["current_needs"].append(item)

    return memory