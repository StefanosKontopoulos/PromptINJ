---
plan: 02-01
phase: 2
status: complete
commit: 25b7177
---

# Summary: Plan 02-01 — PDF and TXT Detectors

## What Was Built

Added to `app.py`:
- `import fitz` (PyMuPDF)
- `INVISIBLE_CHARS` dict with all 7 UNIC-01 codepoints as literal characters
- `detect_invisible_unicode(text)` — shared utility, returns finding dicts
- `scan_txt(uploaded_file)` — UTF-8 decode, Unicode-only scan (safe for visual tricks)
- `scan_pdf(uploaded_file)` — PyMuPDF span iteration, tiny font + white text + Unicode

## Key Files

### Modified
- `app.py` — 133 net lines added

## Implementation Notes

- Used literal invisible chars as INVISIBLE_CHARS keys (not escape sequences) so `str.count()` and `str.find()` work without any conversion
- `page_icon` changed from emoji literal to `\U0001f50d` escape to keep ASCII safety; same for the loop's `st.info` emoji
- `fitz.open(stream=data, filetype="pdf")` used (not filename path) since we have bytes from Streamlit's in-memory uploader
- `scan_file()` stub intentionally retained — replaced in 02-02

## Self-Check: PASSED

- [x] `import fitz` present
- [x] `INVISIBLE_CHARS` with all 7 chars present
- [x] `def detect_invisible_unicode(` present
- [x] `def scan_txt(` present
- [x] `def scan_pdf(` present
- [x] `size < 4.0` present (PDF-01)
- [x] `color == 16777215` present (PDF-02)
- [x] Syntax valid
