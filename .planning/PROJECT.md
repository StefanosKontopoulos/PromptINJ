# PromptINJ — Trojan Prompt / Honeypot Detector

## What This Is

A local Streamlit app that scans uploaded assignment files (PDF, DOCX, TXT) for hidden text professors may embed to catch students using AI. It detects tiny fonts, white-colored text, hidden run properties, and invisible Unicode characters, then shows the exact extracted content so students know what trap instructions were present before they start working.

## Core Value

A student uploads a file and immediately knows whether it contains hidden AI-trap instructions — and if so, sees exactly what those instructions say.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] User can upload PDF, DOCX, and TXT files via drag-and-drop
- [ ] App detects tiny font text (< 4pt) in PDFs and DOCX files
- [ ] App detects white-colored text in PDFs and DOCX files
- [ ] App detects hidden run property in DOCX files
- [ ] App detects invisible Unicode characters (zero-width spaces, soft hyphens, etc.) in all file types
- [ ] App displays exact hidden text content when threats are found
- [ ] App shows clear safe/threat visual feedback (st.success / st.error)
- [ ] TXT files are always safe (no hidden metadata) but still scanned for Unicode tricks
- [ ] Session scan history lists all files processed with their result

### Out of Scope

- Cloud/hosted deployment — local-only tool, no server needed
- Account system or persistent storage — session memory only, no disk writes
- Batch multi-file parallel processing — single file per upload, history tracked in-session
- Steganography or image-embedded text detection — out of scope for v1

## Context

- Target user: students who receive assignment PDFs/DOCX from professors and want to verify the file is clean before using AI assistance
- Tech stack decided upfront: Python, Streamlit, PyMuPDF (`fitz`), `python-docx`
- Detection methods specified by user; Unicode detection added in v1 after questioning
- Local-only deployment keeps the tool simple — no auth, no cloud costs, no privacy concerns
- Invisible Unicode watermarks (zero-width spaces, soft hyphens, zero-width non-joiners) are increasingly used alongside visual tricks

## Constraints

- **Tech Stack**: Python + Streamlit + PyMuPDF + python-docx — no substitutions
- **Deployment**: Local only (`streamlit run app.py`) — no web hosting in v1
- **Privacy**: Files must never leave the user's machine — no external API calls for file content
- **Simplicity**: Single `app.py` file — no complex module structure needed for this scope

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Add Unicode detection to v1 | Zero-width tricks are common in real-world prompt injection; costs little to add | — Pending |
| Session-only scan history | No disk I/O, no privacy risk, simple state via `st.session_state` | — Pending |
| TXT always safe for visual tricks | TXT has no formatting metadata; Unicode scan still applied | — Pending |

---
*Last updated: 2026-05-05 after initialization*

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state
