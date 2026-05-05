# PromptINJ

**Trojan Prompt / Honeypot Detector**

A forensic tool that scans assignment files for hidden AI-trap instructions professors may embed to catch students using AI assistants. Upload a file — know in seconds whether it's clean.

**[→ Try it online](https://promptinj.streamlit.app)** · No install needed

---

## What it detects

| Method | File types | Description |
|--------|-----------|-------------|
| Tiny font | PDF, DOCX | Text rendered below 4pt — invisible to the naked eye |
| Near-white text | PDF, DOCX | Text colored white or near-white against a white background |
| Hidden property | DOCX | Runs with `font.hidden = True` set in Word's XML |
| Invisible Unicode | PDF, DOCX, TXT | Zero-width spaces, soft hyphens, and other non-printing characters |

Each finding is rated **🔴 High** or **🟡 Medium** confidence and shows the exact extracted text.

---

## Use it

### Online (easiest)
Visit **[promptinj.streamlit.app](https://promptinj.streamlit.app)** — no install, works in any browser.
> Files are processed on Streamlit's servers and are not stored or logged. For full privacy, run locally.

### Local (full privacy + folder scanner)

**Requirements:** Python 3.10+

```bash
git clone https://github.com/StefanosKontopoulos/PromptINJ.git
cd PromptINJ
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`. Files never leave your machine.

---

## Features

| | Online | Local |
|--|:--:|:--:|
| Drag-and-drop file upload | ✅ | ✅ |
| Confidence scoring (High / Medium) | ✅ | ✅ |
| Adjustable near-white sensitivity | ✅ | ✅ |
| Session scan history | ✅ | ✅ |
| Folder scanner (scan all files at once) | ❌ | ✅ |
| Files stay on your machine | ❌ | ✅ |

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
