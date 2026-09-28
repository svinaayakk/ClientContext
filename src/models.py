from pydantic import BaseModel
from typing import List, Optional


class MeetingAnalysis(BaseModel):
    client_name: str
    meeting_summary: str

    pain_points: List[str]
    requirements: List[str]
    objections: List[str]
    decisions: List[str]
    action_items: List[str]

    timeline: Optional[str] = None
    budget: Optional[str] = None
    stakeholders: List[str]

    sentiment: Optional[str] = None


if __name__ == "__main__":
    meeting = MeetingAnalysis(
        client_name="Acme Corp",
        meeting_summary="Client wants automated reporting.",
        pain_points=["Manual reporting"],
        requirements=["Automated dashboards"],
        objections=[],
        decisions=[],
        action_items=["Send proposal"],
        timeline="February",
        budget=None,
        stakeholders=["CTO"],
        sentiment="Positive"
    )

    print(meeting)

class ContextUpdate(BaseModel):
    current: List[str]
    resolved: List[str]
    new: List[str]
    changed: List[str]

class Evidence(BaseModel):
    meeting_id: int
    text: str


class ClientAnswer(BaseModel):
    answer: str
    evidence: List[Evidence]