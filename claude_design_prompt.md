Paste this entire prompt into Claude Design to theme the PromptINJ Streamlit app.

---

# PromptINJ — Claude Design Handoff Prompt

## Section 1 — App Purpose and Target User

PromptINJ is a local Python/Streamlit security tool that scans uploaded documents (PDF, DOCX, TXT) for hidden AI-trap instructions professors may embed to catch students using AI. Students run it locally with `streamlit run app.py` — no cloud deployment, no accounts, no external APIs. The app must feel trustworthy and precise: a forensic inspector, not a web product.

---

## Section 2 — Streamlit Components Inventory

Every component currently used in `app.py` after all phases are complete:

| Component | Usage in app |
|-----------|-------------|
| `st.set_page_config` | Sets page title "PromptINJ", icon 🔍, layout centered |
| `st.title` | App name heading at top of main column |
| `st.caption` | Subtitle "Trojan Prompt / Honeypot Detector" under title |
| `st.markdown` | Introductory paragraph explaining supported formats; empty-state "No files uploaded yet." text; sidebar empty-state caption |
| `st.divider` | Horizontal rule below intro paragraph; separators between sidebar history entries |
| `st.file_uploader` | Drag-and-drop zone accepting .pdf, .docx, .txt; multiple files allowed |
| `st.success` | Green banner: safe file result ("No threats detected.") |
| `st.error` | Red banner: threat file result with finding count |
| `st.warning` | Yellow banner: oversized file (>10 MB) warning; scan error message |
| `st.expander` | Collapsible section per finding — header is detection method label + optional page number |
| `st.code` | Renders exact extracted suspicious text inside each expander (language=None) |
| `st.sidebar` | Contains "Scan History" header and reverse-chronological list of all scanned files |
| `st.header` | "Scan History" label at top of sidebar (inside st.sidebar context) |
| `st.session_state` | Stores scan_history list across reruns — no visual output itself |

---

## Section 3 — Desired Visual Style

**Aesthetic:** Professional security-tool / CLI inspector feel. Think a tool a developer or student trusts to give accurate results, not a playful consumer web app. Minimal chrome, data-forward, no decorative elements.

**Color options — provide BOTH and let Claude Design choose:**

**Option A — Dark theme (preferred):**
- Page background: `#0E1117` (near-black)
- Sidebar background: `#1A1D23` (dark grey)
- Text: `#FAFAFA`
- Accent (interactive elements, borders): `#2D6BE4` (electric blue)
- Muted text: `#7A8FAD`

**Option B — Light theme:**
- Page background: `#F0F4F8`
- Sidebar background: `#E2E8F0`
- Headings: `#1E3A5F` (dark navy)
- Accent: `#2D6BE4` (electric blue)
- Muted text: `#64748B`

**Accent color:** A single confident color for interactive elements. Suggested: `#2D6BE4` (electric blue) — signals "security scanner" not "SaaS product". Avoid warm tones; cool blues and teals read as technical.

**Typography:**
- Finding text (inside `st.code`): already monospaced by Streamlit — leave as-is
- All other text: clean sans-serif (Streamlit default `sans serif` or `Inter`)
- App title: slightly larger weight, not decorative

**Status banners:** Keep Streamlit's native `st.success` / `st.error` / `st.warning` semantic colors (green/red/yellow) — only restyle the surrounding area, not the banners themselves. These colors carry meaning.

**File uploader zone:** Should look like a terminal drop zone — dashed border in accent color, low-contrast background, minimal visual weight. No rounded buttons or marketing feel.

---

## Section 4 — CSS Injection Pattern

Streamlit theming uses two mechanisms, in priority order:

**1. `.streamlit/config.toml`** (global palette — set this first):

```toml
[theme]
base = "dark"
primaryColor = "#2D6BE4"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#1A1D23"
textColor = "#FAFAFA"
font = "sans serif"
```

**2. `st.markdown("<style>...</style>", unsafe_allow_html=True)`** — component-level overrides injected immediately after `st.set_page_config(...)` in `app.py`:

```python
st.markdown("""
<style>
/* Drop zone styling */
[data-testid="stFileUploadDropzone"] {
    border: 2px dashed #2D6BE4;
    border-radius: 8px;
    background-color: #1A1D23;
}

/* Sidebar header */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #7A8FAD;
}

/* Sidebar dividers */
section[data-testid="stSidebar"] hr {
    border-color: #2A2D35;
    margin: 0.5rem 0;
}

/* Code blocks inside expanders */
[data-testid="stExpander"] [data-testid="stCode"] {
    font-size: 0.85rem;
    background-color: #161920;
}

/* App title */
[data-testid="stAppViewContainer"] h1 {
    letter-spacing: -0.02em;
}
</style>
""", unsafe_allow_html=True)
```

**Where to place:** This `st.markdown(...)` call goes immediately after `st.set_page_config(...)` at the top of `app.py`, before any other Streamlit calls.

---

## Section 5 — Section-by-Section Layout Description

Walking through the app top to bottom as a designer sees it:

1. **Page header area** — `st.title("PromptINJ")` + `st.caption("Trojan Prompt / Honeypot Detector")`. Centered at top. The title should feel like a tool name stamp, not a brand headline. Caption is muted, small.

2. **Introduction text** — One short paragraph via `st.markdown`. Muted color, not competing with the upload zone. Explains supported formats (PDF, DOCX, TXT).

3. **Divider** — `st.divider()`. Thin separator line, low-contrast.

4. **File upload zone** — `st.file_uploader(...)`. Primary interactive element. When no files are uploaded, this is the visual focus of the entire page. Should have a dashed border and terminal feel. Label: "Drop files here or click to browse".

5. **Results area** — Appears below the upload zone after files are scanned. Each file gets its own result block:
   - `st.success` banner (green) — safe files
   - `st.error` banner (red) with finding count — threat files
   - `st.warning` banner (yellow) — errors or oversized files
   - Below each `st.error`: one `st.expander` per finding. Visual separation between result blocks when multiple files are scanned.

6. **Finding expander** — `st.expander(label)` where label = method name (e.g., "Tiny font", "White text (page 2)", "Invisible Unicode"). When expanded: contains `st.code(text, language=None)` showing the exact extracted suspicious text. Should look like a forensics report entry — clinical, not decorated.

7. **Sidebar** — `st.sidebar` persists across all scans. Contains:
   - `st.header("Scan History")` at top — styled small and uppercase (see CSS above)
   - For each scan (newest first): filename in bold + status badge on next line (`✅ Safe` / `🚨 N findings` / `⚠ Error`)
   - `st.divider()` between entries
   - When empty: muted `st.caption("No files scanned yet.")`

8. **Empty state** — When no files are uploaded yet, the results area shows a centered muted text block: "No files uploaded yet." Rendered via `st.markdown` with inline CSS (already in app).

---

## Section 6 — What NOT to Change

- **Do not rename or restructure any Python variables or Streamlit calls.** CSS selectors must match existing Streamlit-generated `data-testid` attributes.
- **Do not add new Streamlit components** — only style existing ones listed in Section 2.
- **Do not override the semantic colors** of `st.success` (green), `st.error` (red), `st.warning` (yellow) — these carry meaning and must remain distinguishable at a glance.
- **Do not add animations, transitions, or hover effects** — this is a functional forensic tool, not a marketing page.
- **Do not use a custom font that requires an external CDN** — the app is local-only with no internet connectivity assumed.
- **Do not change `layout="centered"` in `st.set_page_config`** — the centered layout is intentional.

---

## Section 7 — Deliverables Requested from Claude Design

Please return:

1. **Updated `.streamlit/config.toml`** — complete `[theme]` block with all required keys filled in with your chosen palette (dark or light from Section 3 options).

2. **The `st.markdown("<style>...</style>")` CSS block** — ready to paste immediately after `st.set_page_config(...)` in `app.py`. Include all component selectors from Section 4 plus any additional ones you add for expanders, code blocks, or sidebar entries.

3. **Any additional per-component CSS selectors** you identify as needed for the file uploader hover state, expander open/closed states, or sidebar entry layout.

4. **A brief rationale** (2–3 sentences) explaining the color palette choices — why these colors serve a security-tool aesthetic and work for the target user (students doing a quick pre-work check).

---

*App tech stack: Python 3.10+, Streamlit, PyMuPDF, python-docx. Run locally with `streamlit run app.py`.*
