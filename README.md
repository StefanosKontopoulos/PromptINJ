# PromptINJ

**Trojan Prompt / Honeypot Detector**

A local forensic tool that scans assignment files for hidden AI-trap instructions professors may embed to catch students using AI assistants. Upload a file — know in seconds whether it's clean.

---

## What it detects

| Method | File types | Description |
|--------|-----------|-------------|
| Tiny font | PDF, DOCX | Text rendered below 4pt — invisible to the naked eye |
| Near-white text | PDF, DOCX | Text colored white or near-white (#E6E6E6+) against a white background |
| Hidden property | DOCX | Runs with `font.hidden = True` set in Word's XML |
| Invisible Unicode | PDF, DOCX, TXT | Zero-width spaces, soft hyphens, and other non-printing characters |

Each finding is rated **🔴 High** or **🟡 Medium** confidence and shows the exact extracted text.

---

## How to run

**Requirements:** Python 3.10+

```bash
git clone https://github.com/StefanosKontopoulos/PromptINJ.git
cd PromptINJ
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`. Everything runs locally — no files leave your machine.

---

## Features

- **Drag-and-drop upload** — scan individual PDF, DOCX, or TXT files
- **Folder scanner** — paste a folder path (or use the 📁 picker) to scan all supported files at once
- **Confidence scoring** — High for definitive traps, Medium for ambiguous near-white colors
- **Adjustable sensitivity** — slider in the sidebar controls the near-white detection threshold
- **Session scan history** — sidebar tracks all files scanned in the current session
- **No internet required** — fully offline, no accounts, no APIs

---

## Tech stack

- [Streamlit](https://streamlit.io) — UI
- [PyMuPDF](https://pymupdf.readthedocs.io) — PDF parsing
- [python-docx](https://python-docx.readthedocs.io) — DOCX parsing

---

## Support

Found a bug or a detection method that should be added?
→ [Submit a report](https://docs.google.com/forms/d/e/1FAIpQLSfCUYYuoeH3Jv0TlJtZl_0BVxN7hZtbg5U75woTTcYngCWl3Q/viewform)

---

## License

MIT
