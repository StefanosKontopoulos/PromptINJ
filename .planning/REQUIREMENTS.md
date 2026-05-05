# Requirements: PromptINJ — Trojan Prompt / Honeypot Detector

**Defined:** 2026-05-05
**Core Value:** Student uploads a file and immediately knows whether it contains hidden AI-trap instructions — and if so, sees exactly what those instructions say.

## v1 Requirements

### Upload

- [ ] **UPLD-01**: User can upload PDF, DOCX, and TXT files via drag-and-drop interface
- [ ] **UPLD-02**: User can upload multiple files at once in a single batch
- [ ] **UPLD-03**: App warns user if any uploaded file exceeds 10MB

### Detection — PDF

- [ ] **PDF-01**: App flags PDF text spans with font size < 4.0 as suspicious
- [ ] **PDF-02**: App flags PDF text spans with white color (integer value 16777215) as suspicious

### Detection — DOCX

- [ ] **DOCX-01**: App flags DOCX text runs where `run.font.hidden` is True as suspicious
- [ ] **DOCX-02**: App flags DOCX text runs with font size < 4pt as suspicious
- [ ] **DOCX-03**: App flags DOCX text runs with white font color (RGB FFFFFF) as suspicious

### Detection — All File Types

- [ ] **UNIC-01**: App scans all file types for invisible Unicode characters (U+200B zero-width space, U+200C ZWNJ, U+200D ZWJ, U+00AD soft hyphen, U+2060 word joiner, U+FEFF BOM/zero-width no-break space, U+180E Mongolian vowel separator)
- [ ] **UNIC-02**: TXT files are treated as safe for visual tricks (no font/color metadata) but still scanned for Unicode anomalies

### Results UI

- [ ] **RSLT-01**: App displays `st.success` banner when no threats detected in a file
- [ ] **RSLT-02**: App displays `st.error` banner when threats detected in a file
- [ ] **RSLT-03**: App shows the exact extracted suspicious text string when threats are found
- [ ] **RSLT-04**: App labels each finding with the detection method that triggered it (e.g., "Tiny font", "White text", "Hidden property", "Invisible Unicode")
- [ ] **RSLT-05**: App maintains a session scan history (st.session_state) listing all files processed with their threat/safe status

### Error Handling

- [ ] **ERRH-01**: App handles corrupted or unreadable files gracefully and shows a descriptive error message
- [ ] **ERRH-02**: App shows a warning banner if an uploaded file exceeds 10MB

### Design Handoff

- [ ] **DSGN-01**: After backend is complete, provide a detailed Claude Design prompt for UI/visual theming of the Streamlit app

## v2 Requirements

### Advanced Detection

- **ADV-01**: Detect font color matching the page background (non-white backgrounds)
- **ADV-02**: Detect text with opacity set near zero
- **ADV-03**: Detect overlapping text layers in PDFs (text placed behind images)

### Export & Reporting

- **RPT-01**: User can export scan results as a PDF report
- **RPT-02**: User can copy scan results to clipboard

### UX Enhancements

- **UX-01**: Drag-and-drop highlights drop zone on hover
- **UX-02**: Progress bar for large file scanning

## Out of Scope

| Feature | Reason |
|---------|--------|
| Cloud/hosted deployment | Local-only tool; no auth or server infrastructure needed for v1 |
| Persistent storage across sessions | No disk writes; session state only — privacy by design |
| Image steganography detection | High complexity, different domain — defer to v2+ |
| Account/user system | Single-user local tool |
| Real-time collaboration | Out of scope for this use case |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| UPLD-01 | Phase 1 | Pending |
| UPLD-02 | Phase 1 | Pending |
| UPLD-03 | Phase 1 | Pending |
| PDF-01 | Phase 2 | Pending |
| PDF-02 | Phase 2 | Pending |
| DOCX-01 | Phase 2 | Pending |
| DOCX-02 | Phase 2 | Pending |
| DOCX-03 | Phase 2 | Pending |
| UNIC-01 | Phase 2 | Pending |
| UNIC-02 | Phase 2 | Pending |
| RSLT-01 | Phase 3 | Pending |
| RSLT-02 | Phase 3 | Pending |
| RSLT-03 | Phase 3 | Pending |
| RSLT-04 | Phase 3 | Pending |
| RSLT-05 | Phase 3 | Pending |
| ERRH-01 | Phase 2 | Pending |
| ERRH-02 | Phase 1 | Pending |
| DSGN-01 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 18 total
- Mapped to phases: 18
- Unmapped: 0 ✓

---
*Requirements defined: 2026-05-05*
*Last updated: 2026-05-05 after initial definition*
