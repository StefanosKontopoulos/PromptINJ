"""
PromptINJ — Trojan Prompt / Honeypot Detector
Cloud version: file upload only (no folder scanner).
"""

import io

import docx  # python-docx — DOCX scanning
from docx.shared import Pt, RGBColor
import fitz  # PyMuPDF — PDF scanning
import streamlit as st
from theme_css import THEME_CSS

INVISIBLE_CHARS = {
    "​": "U+200B zero-width space",
    "‌": "U+200C zero-width non-joiner",
    "‍": "U+200D zero-width joiner",
    "­": "U+00AD soft hyphen",
    "⁠": "U+2060 word joiner",
    "﻿": "U+FEFF zero-width no-break space / BOM",
    "᠎": "U+180E Mongolian vowel separator",
}

st.set_page_config(
    page_title="PromptINJ",
    page_icon="\U0001f50d",
    layout="centered",
)
st.markdown(THEME_CSS, unsafe_allow_html=True)

if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

with st.sidebar:
    st.header("Settings")
    threshold = st.slider(
        "Near-white sensitivity",
        min_value=200,
        max_value=254,
        value=230,
        help=(
            "RGB channel threshold for near-white detection. "
            "Lower = more sensitive (catches light greys). "
            "Higher = only flags near-pure white."
        ),
    )
    st.divider()
    st.header("Scan History")
    if st.session_state.scan_history:
        for entry in reversed(st.session_state.scan_history):
            if entry["status"] == "safe":
                hist_badge = "✅ Safe"
            elif entry["status"] == "threat":
                count = len(entry["findings"])
                hist_badge = f"\U0001f6a8 {count} finding{'s' if count != 1 else ''}"
            else:
                hist_badge = "⚠ Error"
            st.markdown(f"**{entry['filename']}**  \n{hist_badge}")
            st.divider()
    else:
        st.caption("No files scanned yet.")


# ===========================================================================
# Detection helpers
# ===========================================================================

def _near_white_confidence(color_int, threshold):
    if color_int < 0:
        return None
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    if not (r >= threshold and g >= threshold and b >= threshold):
        return None
    return "High" if (r >= 250 and g >= 250 and b >= 250) else "Medium"


def _min_confidence(*confs):
    return "Medium" if "Medium" in confs else "High"


# ===========================================================================
# Detection functions
# ===========================================================================

def detect_invisible_unicode(text):
    findings = []
    for char, name in INVISIBLE_CHARS.items():
        count = text.count(char)
        if count > 0:
            idx = text.find(char)
            context = text[max(0, idx - 20): idx + 20].replace(char, f"[{name}]")
            findings.append({
                "method": "Invisible Unicode",
                "text": f"{count}× {name} — ...{context}...",
                "page": None,
                "confidence": "High",
            })
    return findings


def scan_txt(uploaded_file):
    try:
        text = uploaded_file.read().decode("utf-8", errors="replace")
        findings = detect_invisible_unicode(text)
        return {"status": "threat" if findings else "safe", "filename": uploaded_file.name, "findings": findings}
    except Exception as exc:
        return {"status": "error", "filename": uploaded_file.name, "findings": [], "error": str(exc)}


def scan_pdf(uploaded_file, threshold):
    findings = []
    try:
        raw = uploaded_file.read()
        doc = fitz.open(stream=raw, filetype="pdf")
        grouped = {}
        for page_num, page in enumerate(doc, start=1):
            page_dict = page.get_text("dict")
            for block in page_dict.get("blocks", []):
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        if not text:
                            continue
                        size = span.get("size", 999.0)
                        color = span.get("color", -1)
                        methods, confs = [], []
                        if size < 4.0:
                            methods.append("Tiny font")
                            confs.append("High")
                        nw_conf = _near_white_confidence(color, threshold)
                        if nw_conf:
                            methods.append("Near-white text")
                            confs.append(nw_conf)
                        if methods:
                            key = (", ".join(methods), page_num)
                            span_conf = _min_confidence(*confs)
                            entry = grouped.setdefault(key, {"fragments": [], "confidence": "High"})
                            entry["fragments"].append(text)
                            if span_conf == "Medium":
                                entry["confidence"] = "Medium"
        for (method, page_num), grp in grouped.items():
            findings.append({"method": method, "text": " ".join(grp["fragments"]), "page": page_num, "confidence": grp["confidence"]})
        full_text = "".join(p.get_text() for p in doc)
        findings.extend(detect_invisible_unicode(full_text))
        doc.close()
        return {"status": "threat" if findings else "safe", "filename": uploaded_file.name, "findings": findings}
    except Exception as exc:
        return {"status": "error", "filename": uploaded_file.name, "findings": [], "error": str(exc)}


def scan_docx(uploaded_file, threshold):
    findings = []
    try:
        raw = uploaded_file.read()
        document = docx.Document(io.BytesIO(raw))
        full_text_parts = []
        grouped = {}
        for para in document.paragraphs:
            for run in para.runs:
                text = run.text
                if not text.strip():
                    continue
                full_text_parts.append(text)
                if run.font.hidden:
                    grouped.setdefault("Hidden property", {"fragments": [], "confidence": "High"})["fragments"].append(text)
                if run.font.size is not None and run.font.size < Pt(4):
                    grouped.setdefault("Tiny font", {"fragments": [], "confidence": "High"})["fragments"].append(text)
                try:
                    if run.font.color is not None and run.font.color.type is not None:
                        rgb = run.font.color.rgb
                        r, g, b = rgb.red, rgb.green, rgb.blue
                        if r >= threshold and g >= threshold and b >= threshold:
                            conf = "High" if (r >= 250 and g >= 250 and b >= 250) else "Medium"
                            entry = grouped.setdefault("Near-white text", {"fragments": [], "confidence": "High"})
                            entry["fragments"].append(text)
                            if conf == "Medium":
                                entry["confidence"] = "Medium"
                except Exception:
                    pass
        for method, grp in grouped.items():
            findings.append({"method": method, "text": " ".join(grp["fragments"]), "page": None, "confidence": grp["confidence"]})
        findings.extend(detect_invisible_unicode(" ".join(full_text_parts)))
        return {"status": "threat" if findings else "safe", "filename": uploaded_file.name, "findings": findings}
    except Exception as exc:
        return {"status": "error", "filename": uploaded_file.name, "findings": [], "error": str(exc)}


def scan_file(file_obj, threshold):
    file_obj.seek(0)
    name = file_obj.name.lower()
    if name.endswith(".pdf"):
        return scan_pdf(file_obj, threshold)
    if name.endswith(".docx"):
        return scan_docx(file_obj, threshold)
    if name.endswith(".txt"):
        return scan_txt(file_obj)
    return {"status": "error", "filename": file_obj.name, "findings": [], "error": f"Unsupported file type: {file_obj.name}"}


def display_result(result):
    if result["status"] == "safe":
        st.success(f"✅ **{result['filename']}** — No threats detected.")
    elif result["status"] == "threat":
        count = len(result["findings"])
        st.error(f"\U0001f6a8 **{result['filename']}** — {count} finding{'s' if count != 1 else ''} detected.")
        for finding in result["findings"]:
            page_label = f" (page {finding['page']})" if finding.get("page") else ""
            confidence = finding.get("confidence", "High")
            conf_badge = "🔴 High" if confidence == "High" else "🟡 Medium"
            with st.expander(f"{finding['method']}{page_label} — {conf_badge}"):
                st.code(finding["text"], language=None)
    else:
        st.warning(f"⚠ **{result['filename']}** — Could not scan: {result.get('error', 'Unknown error')}")


# ===========================================================================
# UI
# ===========================================================================

st.title("PromptINJ")
st.caption("Trojan Prompt / Honeypot Detector")
st.markdown(
    "Upload assignment files to check for hidden text that could be used to "
    "manipulate AI assistants. Supports **PDF**, **DOCX**, and **TXT**."
)

st.markdown(
    """
    <div style="
        background: #1A1D23;
        border-left: 3px solid #2D6BE4;
        padding: 0.6rem 1rem;
        font-size: 12px;
        color: #7A8FAD;
        margin-bottom: 0.5rem;
    ">
        Files are processed on Streamlit's servers and are not stored or logged.
        For full privacy, run the app locally —
        <a href="https://github.com/StefanosKontopoulos/PromptINJ" target="_blank"
           style="color: #2D6BE4;">see GitHub</a>.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

uploaded_files = st.file_uploader(
    "Drop files here or click to browse",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    help="Accepted formats: PDF, Word (.docx), plain text (.txt)",
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        if size_mb > 10:
            st.warning(
                f"⚠ {uploaded_file.name} exceeds 10 MB ({size_mb:.1f} MB). "
                "Large files may be slow to process."
            )
            continue
        result = scan_file(uploaded_file, threshold)
        st.session_state.scan_history.append(result)
        display_result(result)
else:
    st.markdown(
        "<div style='text-align:center; color:#888; padding:2rem 0;'>"
        "No files uploaded yet."
        "</div>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------
SUPPORT_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfCUYYuoeH3Jv0TlJtZl_0BVxN7hZtbg5U75woTTcYngCWl3Q/viewform"
GITHUB_URL = "https://github.com/StefanosKontopoulos/PromptINJ"

st.markdown("---")
st.markdown(
    f"""
    <div style="display:flex;justify-content:space-between;align-items:flex-start;padding:1.5rem 0 0.5rem 0;gap:2rem;">
        <div style="flex:2;">
            <div style="font-family:'JetBrains Mono',ui-monospace,monospace;font-size:11px;letter-spacing:0.14em;text-transform:uppercase;color:#7A8FAD;margin-bottom:0.4rem;">About</div>
            <div style="font-size:13px;color:#FAFAFA;font-weight:600;margin-bottom:0.3rem;">PromptINJ</div>
            <div style="font-size:12px;color:#7A8FAD;line-height:1.6;">
                A forensic tool for detecting hidden AI-trap instructions<br>
                embedded in assignment files. No data is stored or logged.
            </div>
        </div>
        <div style="flex:1;">
            <div style="font-family:'JetBrains Mono',ui-monospace,monospace;font-size:11px;letter-spacing:0.14em;text-transform:uppercase;color:#7A8FAD;margin-bottom:0.6rem;">Links</div>
            <div style="display:flex;flex-direction:column;gap:0.4rem;">
                <a href="{GITHUB_URL}" target="_blank" style="font-size:12.5px;color:#2D6BE4;text-decoration:none;">⬡ GitHub — Source code</a>
                <a href="{SUPPORT_URL}" target="_blank" style="font-size:12.5px;color:#2D6BE4;text-decoration:none;">✉ Support — Report an issue</a>
            </div>
        </div>
    </div>
    <div style="font-size:11px;color:#3A4556;padding-top:1rem;font-family:'JetBrains Mono',ui-monospace,monospace;">
        stefankontopoulos@gmail.com
    </div>
    """,
    unsafe_allow_html=True,
)
