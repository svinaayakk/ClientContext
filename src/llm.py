import os

from dotenv import load_dotenv
from google import genai

from .models import MeetingAnalysis, ContextUpdate, ClientAnswer


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_meeting(transcript: str) -> MeetingAnalysis:

    prompt = f"""
You analyze business meeting transcripts.

Extract useful information from the conversation.

IMPORTANT:
- Do not invent information.
- Only use information explicitly mentioned in the transcript.
- If something is not mentioned, return an empty list or null.
- Identify the client/contact name from the transcript when possible.
- Preserve the meaning of what the participants said.

Extract:
- client name
- meeting summary
- pain points
- requirements
- objections
- decisions
- action items
- timeline
- budget
- stakeholders
- sentiment

Here is the meeting transcript:

--- TRANSCRIPT ---

{transcript}

--- END TRANSCRIPT ---
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": MeetingAnalysis,
        },
    )

    return MeetingAnalysis.model_validate_json(response.text)


def compare_context(previous_context, current_context) -> ContextUpdate:

    prompt = f"""
You are maintaining the long-term memory of a business client.

Compare the PREVIOUS meeting with the CURRENT meeting and determine
how the client's business context has evolved.

Your job is NOT to simply compare text.
You must reason about the meaning, status, and evolution of each issue.

CLASSIFICATION RULES:

CURRENT:
- Information that is still active or relevant in the current meeting.
- A previous requirement should remain CURRENT if the client still
  indicates that they want or need it.
- Similar wording should be recognized as the same underlying topic.

RESOLVED:
- A previous pain point, objection, concern, or requirement that the
  client explicitly says has been solved, completed, or is no longer
  a concern.
- If the current meeting explicitly says a previous concern is resolved,
  it MUST NOT appear in CURRENT.

NEW:
- A genuinely new requirement, concern, pain point, objection, or
  business need introduced in the current meeting.
- Only classify something as NEW if it represents a genuinely different
  underlying need that did not already exist in the previous meeting.
- A changed version of an existing requirement is NOT NEW.

CHANGED:
- Information that existed previously but has materially changed.
- Examples include:
  - changed scope
  - changed status
  - changed priority
  - changed timing
  - changed frequency
  - changed implementation approach
  - changed level of detail
- If a current requirement refers to the same underlying requirement as
  a previous requirement but changes its timing, scope, priority, frequency,
  or implementation detail, classify it as CHANGED rather than NEW.
- The new wording of a changed requirement must NOT be listed under NEW.

IMPORTANT:

1. Compare meaning, not exact wording.
2. Do not treat synonyms as new information.
3. Do not duplicate the same underlying issue across CURRENT and NEW.
4. If something is explicitly resolved, place it in RESOLVED only.
5. Do not keep a resolved issue in CURRENT.
6. Do not invent information that is not supported by either meeting.
7. Keep each item concise and understandable without additional context.
8. NEW and CHANGED must be mutually exclusive for the same underlying concept.
9. If a previous requirement is modified in the current meeting, report
   the modification under CHANGED and do not report the modified version
   as NEW.
10. A genuinely new requirement should appear under NEW only if there is
    no corresponding underlying requirement in the previous meeting.

IMPORTANT EXAMPLE:

Previous requirement:
"Real-time delay alerts"

Current requirement:
"Daily delay alerts"

Correct classification:

CHANGED:
"Delay alerts changed from real-time to daily"

NEW:
Nothing for the delay-alert requirement.

Another example:

Previous requirement:
"Delivery performance dashboard"

Current requirement:
"Delivery performance dashboard with Salesforce integration"

Correct classification:

CHANGED:
"Dashboard scope expanded to include Salesforce integration"

NEW:
Nothing for the existing dashboard requirement.

If the current meeting introduces:
"Cancellation rate increase alerts per zone"

and this did not exist previously, then:

NEW:
"Cancellation rate increase alerts per zone"

Do not place the same underlying concept in both NEW and CHANGED.

PREVIOUS MEETING:

{previous_context}


CURRENT MEETING:

{current_context}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ContextUpdate,
        },
    )

    return ContextUpdate.model_validate_json(response.text)

def answer_client_question(question, client_memory, meeting_contexts):

    formatted_contexts = []

    for meeting_id, context in meeting_contexts:
        formatted_contexts.append({
            "meeting_id": meeting_id,
            "context": context
        })

    prompt = f"""
You are a business conversation intelligence assistant.

Answer the user's question using ONLY the client memory and meeting
contexts provided below.

IMPORTANT RULES:
- Do not invent information.
- Do not use outside knowledge.
- Prefer the latest meeting when information has changed.
- If an older issue was explicitly resolved, do not present it as current.
- Keep the answer concise and business-focused.
- Every important claim should be supported by evidence from a meeting.
- Evidence meeting_id MUST be one of the meeting IDs explicitly provided below.
- Never invent, infer, or change a meeting_id.
- Evidence text should be a short, faithful statement of what was
  actually mentioned in that meeting.
- Do not create evidence that is not supported by the meeting context.
- If the question concerns a change between meetings, use evidence
  from the relevant meetings.

CLIENT MEMORY:

{client_memory}


MEETING CONTEXTS:

{formatted_contexts}


USER QUESTION:

{question}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ClientAnswer,
        },
    )

    return ClientAnswer.model_validate_json(response.text)