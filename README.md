# ClientContext

AI-powered conversational intelligence system that extracts, tracks, and retrieves evolving client context across business meetings using LLMs.

## Overview

ClientContext analyzes business meeting transcripts and converts unstructured conversations into structured client intelligence.

The system can:

- Extract client requirements, pain points, objections, decisions, action items, timelines, budgets, and stakeholders.
- Store meeting information in SQLite.
- Compare information across multiple meetings.
- Identify what is still active, resolved, newly introduced, or changed.
- Build an evolving client memory.
- Answer questions about the client using meeting context.
- Provide meeting-level evidence supporting generated answers.

The project focuses on building reliable LLM-powered conversation intelligence rather than simply generating summaries.

---

## Problem

Important information from business conversations is often scattered across multiple meetings.

For example, a client may:

- introduce a requirement in one meeting,
- raise an objection in another,
- resolve that objection later,
- and introduce a new requirement several weeks afterward.

A simple meeting summarizer treats each conversation independently.

ClientContext instead maintains an evolving representation of the client's context across meetings.

---

## Architecture

                Business Meeting Transcript
                           |
                           v
                  +------------------+
                  |   LLM Analysis   |
                  +------------------+
                           |
                           v
                 Structured Pydantic
                      Output
                           |
                           v
                    SQLite Database
                           |
                           v
              +-----------------------+
              | Meeting Context       |
              | Retrieval             |
              +-----------------------+
                           |
                           v
              +-----------------------+
              | Cross-Meeting         |
              | Context Comparison    |
              +-----------------------+
                           |
                           v
                  Client Memory
                           |
                           v
                 Question Answering
                           |
                           v
              Evidence-Grounded Answer
