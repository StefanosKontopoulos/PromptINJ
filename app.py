"""
PromptINJ — Trojan Prompt / Honeypot Detector
Scans uploaded assignment files for hidden AI-trap instructions.
"""

import io
import os

import docx  # python-docx — DOCX scanning (DOCX-01, DOCX-02, DOCX-03)
from docx.shared import Pt, RGBColor
import fitz  # PyMuPDF — PDF scanning (PDF-01, PDF-02)
import streamlit as st
from theme_css import THEME_CSS

# ---------------------------------------------------------------------------
# Invisible Unicode characters used in prompt injection watermarks (UNIC-01)
# Keys are the actual code points so str.count() and str.find() work directly.
# ---------------------------------------------------------------------------
INVISIBLE_CHARS = {
    "​": "U+200B zero-width space",
    "‌": "U+200C zero-width non-joiner",
    "‍": "U+200D zero-width joiner",
    "­": "U+00AD soft hyphen",
    "⁠": "U+2060 word joiner",
    "﻿": "U+FEFF zero-width no-break space / BOM",
    "᠎": "U+180E Mongolian vowel separator",
}

# ---------------------------------------------------------------------------
# Page configuration — must be the first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="PromptINJ",
    page_icon="\U0001f50d",  # 🔍 as escape to keep file ASCII-safe
    layout="centered",
)
st.markdown(THEME_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state initialisation
# Each entry: {"filename": str, "status": "safe"|"threat"|"error", "findings": list}
# ---------------------------------------------------------------------------
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

# ---------------------------------------------------------------------------
# Sidebar — session scan history (RSLT-05)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Scan History")
    if st.session_state.scan_history:
        for entry in reversed(st.session_state.scan_history):
            if entry["status"] == "safe":
                badge = "✅ Safe"
            elif entry["status"] == "threat":
                count = len(entry["findings"])
                badge = f"\U0001f6a8 {count} finding{'s' if count != 1 else ''}"
            else:
                badge = "⚠ Error"
            st.markdown(f"**{entry['filename']}**  \n{badge}")
            st.divider()
    else:
        st.caption("No files scanned yet.")

# ===========================================================================
# Detection functions — all defined before the upload loop that calls them
# ===========================================================================


def detect_invisible_unicode(text):
    """
    Scan text for invisible Unicode characters used in prompt injection.
    Returns a list of finding dicts (method, text, page=None).  (UNIC-01)
    """
    findings = []
    for char, name in INVISIBLE_CHARS.items():
        count = text.count(char)
        if count > 0:
            idx = text.find(char)
            context = text[max(0, idx - 20) : idx + 20].replace(
                char, f"[{name}]"
            )
            findings.append(
                {
                    "method": "Invisible Unicode",
                    "text": f"{count}× {name} — ...{context}...",
                    "page": None,
                }
            )
    return findings


def scan_txt(uploaded_file):
    """
    TXT files have no formatting metadata — safe for visual tricks (UNIC-02).
    Still scanned for invisible Unicode characters (UNIC-01).
    """
    try:
        text = uploaded_file.read().decode("utf-8", errors="replace")
        findings = detect_invisible_unicode(text)
        return {
            "status": "threat" if findings else "safe",
            "filename": uploaded_file.name,
            "findings": findings,
        }
    except Exception as exc:
        return {
            "status": "error",
            "filename": uploaded_file.name,
            "findings": [],
            "error": str(exc),
        }


def scan_pdf(uploaded_file):
    """
    Scan a PDF for hidden text:
      - Font size < 4pt   (PDF-01)
      - White text color  (PDF-02, integer 16777215 == 0xFFFFFF)
    Also runs invisible Unicode scan on the full extracted text.  (UNIC-01)
    """
    findings = []
    try:
        data = uploaded_file.read()
        doc = fitz.open(stream=data, filetype="pdf")
        # Group span text by (method, page) so full sentences appear together
        grouped = {}  # (method, page_num) -> [text fragments]
        for page_num, page in enumerate(doc, start=1):
            page_dict = page.get_text("dict")
            for block in page_dict.get("blocks", []):
                if block.get("type") != 0:  # 0 = text block
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        if not text:
                            continue
                        size = span.get("size", 999.0)
                        color = span.get("color", -1)
                        methods = []
                        if size < 4.0:       # PDF-01
                            methods.append("Tiny font")
                        if color == 16777215:  # PDF-02: 0xFFFFFF white
                            methods.append("White text")
                        if methods:
                            key = (", ".join(methods), page_num)
                            grouped.setdefault(key, []).append(text)
        for (method, page_num), fragments in grouped.items():
            findings.append({"method": method, "text": " ".join(fragments), "page": page_num})
        # Unicode scan on full document text
        full_text = "".join(page.get_text() for page in doc)
        findings.extend(detect_invisible_unicode(full_text))
        doc.close()
        return {
            "status": "threat" if findings else "safe",
            "filename": uploaded_file.name,
            "findings": findings,
        }
    except Exception as exc:
        return {
            "status": "error",
            "filename": uploaded_file.name,
            "findings": [],
            "error": str(exc),
        }


def scan_docx(uploaded_file):
    """
    Scan a DOCX for hidden text runs using three detection methods:
      - Hidden property (run.font.hidden == True)           DOCX-01
      - Tiny font (run.font.size < Pt(4), i.e. < 50800 EMU) DOCX-02
      - White font color (RGB #FFFFFF)                       DOCX-03
    Also runs invisible Unicode scan on concatenated text.   UNIC-01
    """
    findings = []
    try:
        data = uploaded_file.read()
        document = docx.Document(io.BytesIO(data))
        full_text_parts = []
        for para in document.paragraphs:
            for run in para.runs:
                text = run.text
                if not text.strip():
                    continue
                full_text_parts.append(text)
                # Hidden property (DOCX-01)
                if run.font.hidden:
                    findings.append(
                        {"method": "Hidden property", "text": text, "page": None}
                    )
                # Tiny font — size is in EMU; Pt(4) == 50800 EMU (DOCX-02)
                if run.font.size is not None and run.font.size < Pt(4):
                    findings.append(
                        {"method": "Tiny font", "text": text, "page": None}
                    )
                # White font color (DOCX-03)
                try:
                    if (
                        run.font.color is not None
                        and run.font.color.type is not None
                        and run.font.color.rgb == RGBColor(0xFF, 0xFF, 0xFF)
                    ):
                        findings.append(
                            {"method": "White text", "text": text, "page": None}
                        )
                except Exception:
                    pass  # color.rgb raises for theme colors — skip gracefully
        # Unicode scan on concatenated paragraph text
        findings.extend(detect_invisible_unicode(" ".join(full_text_parts)))
        return {
            "status": "threat" if findings else "safe",
            "filename": uploaded_file.name,
            "findings": findings,
        }
    except Exception as exc:
        return {
            "status": "error",
            "filename": uploaded_file.name,
            "findings": [],
            "error": str(exc),
        }


def scan_file(uploaded_file):
    """
    Route an uploaded file to the correct scanner based on extension.
    Resets the file read position before dispatching (seek(0)) so scanners
    always read from the beginning regardless of prior .getvalue() calls.
    Returns a result dict: {status, filename, findings, error?}
    """
    uploaded_file.seek(0)
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return scan_pdf(uploaded_file)
    if name.endswith(".docx"):
        return scan_docx(uploaded_file)
    if name.endswith(".txt"):
        return scan_txt(uploaded_file)
    return {
        "status": "error",
        "filename": uploaded_file.name,
        "findings": [],
        "error": f"Unsupported file type: {uploaded_file.name}",
    }


# ===========================================================================
# UI
# ===========================================================================

st.title("PromptINJ")
st.caption("Trojan Prompt / Honeypot Detector")

st.markdown(
    "Upload assignment files to check for hidden text that could be used to "
    "manipulate AI assistants. Supports **PDF**, **DOCX**, and **TXT**."
)

st.divider()

# ---------------------------------------------------------------------------
# File uploader  (UPLD-01, UPLD-02)
# ---------------------------------------------------------------------------
uploaded_files = st.file_uploader(
    "Drop files here or click to browse",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    help="Accepted formats: PDF, Word (.docx), plain text (.txt)",
)

# ---------------------------------------------------------------------------
# Per-file processing loop
# ---------------------------------------------------------------------------
if uploaded_files:
    for uploaded_file in uploaded_files:

        # Size gate (UPLD-03 / ERRH-02): warn and skip oversized files
        size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        if size_mb > 10:
            st.warning(
                f"⚠ {uploaded_file.name} exceeds 10 MB ({size_mb:.1f} MB). "
                "Large files may be slow to process."
            )
            continue

        # Run detection
        result = scan_file(uploaded_file)

        # Record in session scan history (RSLT-05)
        st.session_state.scan_history.append(result)

        # Per-file results display (RSLT-01, RSLT-02, RSLT-03, RSLT-04)
        if result["status"] == "safe":
            st.success(f"✅ **{result['filename']}** — No threats detected.")

        elif result["status"] == "threat":
            count = len(result["findings"])
            st.error(
                f"\U0001f6a8 **{result['filename']}** — {count} finding{'s' if count != 1 else ''} detected."
            )
            for finding in result["findings"]:
                page_label = f" (page {finding['page']})" if finding["page"] else ""
                with st.expander(f"{finding['method']}{page_label}"):
                    st.code(finding["text"], language=None)

        else:  # status == "error"
            st.warning(
                f"⚠ **{result['filename']}** — Could not scan: {result.get('error', 'Unknown error')}"
            )

else:
    st.markdown(
        "<div style='text-align:center; color:#888; padding:2rem 0;'>"
        "No files uploaded yet."
        "</div>",
        unsafe_allow_html=True,
    )
