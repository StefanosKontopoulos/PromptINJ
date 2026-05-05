# PromptINJ — Trojan Prompt / Honeypot Detector

## Project Overview

Local Streamlit app that scans uploaded documents (PDF, DOCX, TXT) for hidden AI-trap instructions — tiny fonts, white text, hidden run properties, and invisible Unicode characters.

## GSD Workflow

This project uses the Get-Shit-Done (GSD) workflow.

**Current phase:** Phase 1 — Foundation
**Next command:** `/gsd-discuss-phase 1` or `/gsd-plan-phase 1`

### Workflow Commands
- `/gsd-plan-phase [N]` — Plan the next phase
- `/gsd-execute-phase [N]` — Execute a planned phase
- `/gsd-verify-work` — Verify phase deliverables
- `/gsd-progress` — Check current project state

## Tech Stack

- **Runtime:** Python 3.10+
- **UI:** Streamlit
- **PDF parsing:** PyMuPDF (`fitz`)
- **DOCX parsing:** `python-docx`
- **No external APIs** — all processing is local

## Key Architecture Decisions

- Single `app.py` file — no complex module structure
- Detection returns structured dicts: `{"method": str, "text": str, "page": int|None}`
- Session state via `st.session_state` for scan history
- UI styling deferred to Claude Design (Phase 3 produces handoff prompt)

## Detection Methods

| Method | File Types | Trigger |
|--------|-----------|---------|
| Tiny font | PDF, DOCX | size < 4pt |
| White text | PDF, DOCX | color == white |
| Hidden property | DOCX only | run.font.hidden == True |
| Invisible Unicode | All | U+200B, U+200C, U+200D, U+00AD, U+2060, U+FEFF, U+180E |

## Planning Docs

- `.planning/PROJECT.md` — project context and decisions
- `.planning/REQUIREMENTS.md` — v1 requirements with REQ-IDs
- `.planning/ROADMAP.md` — 3-phase execution roadmap
- `.planning/STATE.md` — current progress state
