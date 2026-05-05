---
plan: 02-02
phase: 2
status: complete
commit: 240af57
---

# Summary: Plan 02-02 — DOCX Detector and Dispatcher

## What Was Built

Added to `app.py`:
- `import docx` and `from docx.shared import Pt, RGBColor`
- `scan_docx(uploaded_file)` — iterates `document.paragraphs → para.runs`, detecting:
  - Hidden property (`run.font.hidden == True`) — DOCX-01
  - Tiny font (`run.font.size < Pt(4)`, i.e. < 50800 EMU) — DOCX-02
  - White font color (`run.font.color.rgb == RGBColor(0xFF, 0xFF, 0xFF)`) — DOCX-03
  - Invisible Unicode on concatenated paragraph text — UNIC-01
- Real `scan_file()` dispatcher — replaced stub with extension routing + `seek(0)` reset

## Key Files

### Modified
- `app.py` — 73 net lines added

## Implementation Notes

- `run.font.color.rgb` wrapped in `try/except` — raises `AttributeError` for theme colors
- `scan_file()` calls `seek(0)` before routing to guarantee scanners read from byte 0 (Streamlit's `getvalue()` size-check leaves position at EOF)
- Stub removed: `"status": "pending"` no longer present

## Self-Check: PASSED

- [x] `import docx` present
- [x] `from docx.shared import Pt, RGBColor` present
- [x] `def scan_docx(` present
- [x] `docx.Document(io.BytesIO(data))` present
- [x] `run.font.hidden` present (DOCX-01)
- [x] `run.font.size < Pt(4)` present (DOCX-02)
- [x] `RGBColor(0xFF, 0xFF, 0xFF)` present (DOCX-03)
- [x] `uploaded_file.seek(0)` present (dispatcher)
- [x] `"status": "pending"` absent (stub removed)
- [x] Syntax valid
