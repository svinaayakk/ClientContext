ClientContext

-AI-Powered Client Intelligence System

ClientContext is an LLM-based system that extracts and tracks important client information across multiple business meetings.

It helps identify client requirements, pain points, objections, decisions, action items, and changes in requirements over time.

-Key Features

- Structured extraction of meeting information using an LLM
- Pydantic-based structured outputs
- SQLite storage for meeting data
- Cross-meeting context comparison
- Client memory for tracking new, resolved, and changed requirements
- Evidence-based Q&A over stored meeting context
- Basic evaluation using manually defined ground truth

## System Workflow


Meeting Transcript
        ↓
LLM Analysis
        ↓
Structured Pydantic Output
        ↓
SQLite Database
        ↓
Cross-Meeting Context Comparison
        ↓
Client Memory
        ↓
Question Answering + Evidence


Tech Stack
Python
Gemini API
Pydantic
SQLite
python-dotenv


Project Structure
ClientContext/
│
├── data/
│   └── transcripts/
│
├── database/
│   └── clientcontext.db
│
├── evaluation/
│   ├── ground_truth.py
│   └── evaluator.py
│
├── src/
│   ├── models.py
│   ├── llm.py
│   ├── database.py
│   ├── context.py
│   └── prompts.py
│
├── main.py
├── check_models.py
├── requirements.txt
└── README.md


Example

The system processes multiple meetings with the same client and tracks how their requirements evolve.
For example:

Meeting 1
→ Zone-level delivery dashboard
→ Delivery delay visibility
→ Data integration concern

Meeting 2
→ Salesforce integration added
→ Data integration concern resolved

Meeting 3
→ Daily delay alerts
→ Zone-level cancellation alerts
→ Salesforce integration remains important

The system can then answer questions such as:

What are Ananya's current requirements after the latest meeting?

and return an answer together with supporting meeting evidence.

Evaluation

The project includes a small evaluation framework using manually defined ground-truth concepts for selected meeting transcripts.
The evaluation measures extraction recall for important fields and checks for known unsupported extractions.
The evaluation is intended for basic error analysis rather than as a statistically representative benchmark.

Limitations
Uses synthetic meeting transcripts rather than real client conversations.
The current system does not use a vector database or embedding-based retrieval.
Evaluation is based on a small manually created ground-truth dataset.
LLM outputs can vary between runs.
Future Improvements
Add larger and more diverse evaluation datasets
Improve semantic retrieval across a larger meeting history
Add richer evidence retrieval
Add a lightweight dashboard for exploring client context
Add support for more complex conversation formats