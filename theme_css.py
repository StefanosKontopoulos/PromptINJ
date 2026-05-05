"""
PromptINJ — forensic-inspector chrome.

Paste the THEME_CSS block below into app.py immediately after
st.set_page_config(...) like so:

    st.set_page_config(...)
    st.markdown(THEME_CSS, unsafe_allow_html=True)

Semantic st.success / st.error / st.warning colors are intentionally
left untouched.
"""

THEME_CSS = """
<style>
:root {
  --pi-accent: #2D6BE4;
  --pi-muted:  #7A8FAD;
  --pi-border: #262C36;
  --pi-panel:  #161A21;
}

/* Compact, centered column */
[data-testid="stAppViewContainer"] .main .block-container {
  max-width: 760px;
  padding-top: 3.5rem;
}

/* Title */
[data-testid="stAppViewContainer"] h1 {
  font-weight: 700;
  letter-spacing: -0.01em;
}

/* Caption — uppercase forensic tag */
[data-testid="stCaptionContainer"], .st-emotion-cache-1jicfl2 {
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  color: var(--pi-muted) !important;
  font-size: 12px !important;
}

/* Sidebar header */
[data-testid="stSidebar"] h2 {
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 13px;
  color: var(--pi-muted);
  font-weight: 600;
}

/* Sidebar dividers tighter */
[data-testid="stSidebar"] hr {
  margin: 0.6rem 0;
  border-top-color: var(--pi-border) !important;
}

/* File uploader — dashed forensic frame, square corners */
[data-testid="stFileUploader"] section {
  border: 1px dashed #323A47;
  background: var(--pi-panel);
  border-radius: 0;
  padding: 24px;
  transition: border-color 0.15s, background 0.15s;
}
[data-testid="stFileUploader"] section:hover {
  border-color: rgba(45, 107, 228, 0.45);
  background: #181D26;
}
[data-testid="stFileUploader"] button {
  border-radius: 0 !important;
  border: 1px solid #323A47 !important;
  background: transparent !important;
  color: #FAFAFA !important;
}
[data-testid="stFileUploader"] button:hover {
  border-color: var(--pi-accent) !important;
  color: var(--pi-accent) !important;
}

/* Expanders — square, file-card feel */
[data-testid="stExpander"] {
  border: 1px solid var(--pi-border);
  border-radius: 0;
  background: var(--pi-panel);
  margin-bottom: 6px;
}
[data-testid="stExpander"] summary {
  font-size: 13.5px;
}
[data-testid="stExpander"] summary:hover {
  background: #1F242C;
}

/* st.code — left accent rule + monospace */
[data-testid="stCodeBlock"] pre,
pre code {
  background: #0A0C12 !important;
  border-left: 2px solid var(--pi-accent);
  border-radius: 0 !important;
  font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace !important;
  font-size: 12.5px !important;
  line-height: 1.6 !important;
}

/* Divider */
hr { border-top-color: var(--pi-border) !important; }

/* Banners — keep semantic colors but square the corners */
[data-testid="stAlert"] {
  border-radius: 0 !important;
  border-left-width: 3px !important;
}

/* Hide Streamlit chrome for app-like feel */
#MainMenu, footer {
  visibility: hidden;
}
</style>
"""
