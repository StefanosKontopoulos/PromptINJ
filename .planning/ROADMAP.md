# Roadmap: PromptINJ — Trojan Prompt / Honeypot Detector

**Milestone:** v1.0 — Local Streamlit app with full hidden-text detection
**Granularity:** Coarse (3 phases)
**Requirements covered:** 18 / 18 ✓

---

## Phase Overview

| # | Phase | Goal | Requirements | Plans |
|---|-------|------|--------------|-------|
| 1 | Foundation | Scaffold the app with file upload, dependency config, and size validation | UPLD-01, UPLD-02, UPLD-03, ERRH-02 | 1 |
| 2 | Detection Engine | Implement all detection logic across PDF, DOCX, TXT, and Unicode scanning | PDF-01, PDF-02, DOCX-01, DOCX-02, DOCX-03, UNIC-01, UNIC-02, ERRH-01 | 2 |
| 3 | Results UI & Handoff | Wire detection results into the UI, add scan history, and produce the Claude Design prompt | RSLT-01, RSLT-02, RSLT-03, RSLT-04, RSLT-05, DSGN-01 | 2 |

---

## Phase 1: Foundation

**Goal:** Scaffold the Streamlit app with multi-file drag-and-drop upload, requirements.txt, and file size validation. App runs but detection is stubbed.

**Requirements:** UPLD-01, UPLD-02, UPLD-03, ERRH-02

**Plans:**
- `01-01`: Project scaffold — `app.py` skeleton, `requirements.txt`, Streamlit file uploader accepting .pdf/.docx/.txt, 10MB size warning, basic layout structure

**Success Criteria:**
1. `streamlit run app.py` launches without errors
2. User can drag-and-drop multiple files of supported types
3. File exceeding 10MB triggers a warning banner
4. Unsupported file type is rejected at upload
5. App layout renders cleanly with title and upload zone

**UI hint:** yes

---

## Phase 2: Detection Engine

**Goal:** Implement all detection methods — PDF (tiny font, white text), DOCX (hidden property, tiny font, white text), and invisible Unicode scanning for all file types. Each returns a structured result dict.

**Requirements:** PDF-01, PDF-02, DOCX-01, DOCX-02, DOCX-03, UNIC-01, UNIC-02, ERRH-01

**Plans:**
- `02-01`: PDF and TXT detectors — `scan_pdf()` using PyMuPDF iterating pages/blocks/lines/spans; `scan_txt()` as pass-through + Unicode scan; shared `detect_invisible_unicode()` utility
- `02-02`: DOCX detector — `scan_docx()` using python-docx iterating paragraphs and runs, flagging hidden/tiny/white runs; integrate Unicode scan; unified `scan_file()` dispatcher; error handling for corrupted files

**Success Criteria:**
1. `scan_pdf()` returns findings for a PDF with white text or sub-4pt spans
2. `scan_docx()` returns findings for a DOCX with hidden, tiny, or white-colored runs
3. `scan_txt()` returns safe with no visual findings
4. `detect_invisible_unicode()` detects zero-width space in any text
5. Corrupted file raises a handled exception with descriptive message
6. Each finding dict includes `method`, `text`, and `page` (where applicable)

---

## Phase 3: Results UI & Design Handoff

**Goal:** Wire detection results into the Streamlit UI — safe/threat banners, exact text display, threat type labels, session scan history. Produce the Claude Design handoff prompt.

**Requirements:** RSLT-01, RSLT-02, RSLT-03, RSLT-04, RSLT-05, DSGN-01

**Plans:** 2 plans

Plan files:
- [ ] 03-01-PLAN.md — Results UI: per-file st.success/st.error banners, expandable findings list with method labels and extracted text, sidebar scan history
- [ ] 03-02-PLAN.md — Claude Design handoff: write claude_design_prompt.md covering all components, visual style, CSS injection pattern, and deliverables

**Success Criteria:**
1. Safe file shows green `st.success` banner
2. Threat file shows red `st.error` banner with finding count
3. Each finding shows method label ("Tiny font", "White text", "Hidden property", "Invisible Unicode") and the exact text
4. Sidebar scan history lists all scanned files with safe/threat badge
5. Claude Design prompt is complete, accurate, and ready to paste

---

## Milestone Gate: v1.0

**All phases complete when:**
- [ ] App runs locally with `streamlit run app.py`
- [ ] All three file types produce correct results
- [ ] All four detection methods trigger on known test cases
- [ ] Session history persists across multiple file uploads
- [ ] Claude Design prompt delivered
