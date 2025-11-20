# --------------------------
# Premium Streamlit UI for AI Testcase Generator (Final Clean Version)
# --------------------------

import streamlit as st
import json
import google.generativeai as genai
import pandas as pd
import numpy as np
import zipfile
import io
import re
import logging
from pathlib import Path
from config import Config

# -----------------------------------------------------------------------------
# App Config & Setup
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Testcase Generator",
    layout="wide",
    page_icon="🧪"
)

Config.ensure_dirs()
genai.configure(api_key=Config.GEMINI_API_KEY)

logger = logging.getLogger("streamlit_app")
logger.setLevel(logging.INFO)


# -----------------------------------------------------------------------------
# Custom Premium CSS – Glassmorphism, Gradients, Modern UI
# -----------------------------------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Page background */
.stApp {
    background: linear-gradient(135deg, #0a0f1c 0%, #111927 40%, #0a0f1c 100%);
    color: #e6eef6 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(10, 15, 28, 0.65);
    backdrop-filter: blur(18px);
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #dbeafe !important;
}

/* Glass Cards */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 24px rgba(0,0,0,0.25);
}

/* Section headers */
.section-title {
    font-size: 28px;
    font-weight: 700;
    margin-top: 8px;
    margin-bottom: 8px;
    color: #c7d2fe;
}

/* Gradient buttons */
.stButton>button {
    background: linear-gradient(135deg, #6366f1, #ec4899);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 16px;
    font-weight: 600;
    font-size: 16px;
    transition: 0.2s ease-in-out;
}
.stButton>button:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #7c3aed, #db2777);
}

/* Editor textarea */
textarea {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 15px !important;
}

/* Expander header */
.streamlit-expanderHeader {
    font-size: 18px;
    color: #a5b4fc !important;
    font-weight: 600 !important;
}

/* Metrics */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04);
    padding: 14px 20px;
    border-radius: 12px;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Gemini Helper Functions
# -----------------------------------------------------------------------------

def call_gemini(model, prompt, json_output=False, temperature=0.2):
    """Call Gemini model and return text or JSON."""
    m = genai.GenerativeModel(model)

    try:
        if json_output:
            resp = m.generate_content(
                prompt,
                generation_config={"temperature": temperature, "response_mime_type": "application/json"}
            )
        else:
            resp = m.generate_content(prompt, generation_config={"temperature": temperature})

        return getattr(resp, "text", "")
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        raise


def extract_numbered(text):
    return re.findall(r"^\s*\d+\.\s+(.+)$", text, re.MULTILINE)


def try_parse_json(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        raise RuntimeError("Invalid JSON returned by model.")


def generate_scenarios(model, context, n, temp):
    prompt = f"""
Generate {n} QA test scenarios.

CONTEXT:
\"\"\"{context}\"\"\"

Rules:
- Only numbered lines (1., 2., 3.)
- No explanation
"""
    raw = call_gemini(model, prompt, temperature=temp)
    return extract_numbered(raw)


def generate_testcase(model, context, scenario, temp):
    prompt = f"""
Generate a detailed QA TESTCASE in pure JSON.

CONTEXT:
\"\"\"{context}\"\"\"

SCENARIO:
\"\"\"{scenario}\"\"\"

JSON must include:
- title
- priority_id
- custom_preconds
- custom_steps_separated[]:
    - content
    - expected
Return ONLY JSON.
"""
    raw = call_gemini(model, prompt, json_output=True, temperature=temp)
    return try_parse_json(raw)


# -----------------------------------------------------------------------------
# Sidebar – Clean Version
# -----------------------------------------------------------------------------

st.sidebar.title("⚙️ Configuration")

st.sidebar.markdown("### Model")
st.sidebar.success("Gemini 2.5 Flash (default)")
model_choice = "models/gemini-2.5-flash"

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2)
num_scenarios = st.sidebar.slider("Number of Scenarios", 1, 20, 5)
export_formats = st.sidebar.multiselect("Export Formats", ["JSON", "CSV", "Markdown"], default=["JSON", "CSV"])


# -----------------------------------------------------------------------------
# Layout: Two Columns
# -----------------------------------------------------------------------------

left, right = st.columns([1, 2])


# ===============================
# LEFT PANEL — Context + Editing
# ===============================
with left:
    st.markdown("<h2 class='section-title'>📘Module Context</h2>", unsafe_allow_html=True)

    context_text = st.text_area(
        "",
        height=260, 
        placeholder="Describe your feature/module here..."
    )

    uploaded = st.file_uploader("Upload context (.txt)", type=["txt"])
    if uploaded:
        context_text = uploaded.read().decode("utf-8")
        st.success("Context loaded!")

    if st.button("Generate Scenarios"):
        if not context_text.strip():
            st.error("Please enter context.")
        else:
            try:
                scenarios = generate_scenarios(model_choice, context_text, num_scenarios, temperature)
                st.session_state["scenarios"] = scenarios
                st.session_state.pop("testcases", None)
                st.success("Scenarios generated!")
            except Exception as e:
                st.error(f"Error: {e}")

    # Scenario Editor
    if "scenarios" in st.session_state:
        st.markdown("<h2 class='section-title'>✍️ Edit Scenarios</h2>", unsafe_allow_html=True)

        edited_list = []

        for idx, sc in enumerate(st.session_state["scenarios"]):
            with st.expander(f"Scenario {idx+1}", expanded=True):
                txt = st.text_area(
                    "",
                    value=sc,
                    height=140,
                    key=f"sc_{idx}",
                    placeholder="Modify scenario..."
                )
                edited_list.append(txt)

        if st.button("💾 Save Changes"):
            st.session_state["scenarios"] = edited_list
            st.success("Changes saved!")


# ===============================
# RIGHT PANEL — Scenarios / Testcases / Metrics
# ===============================
with right:

    st.markdown("<h2 class='section-title'>📝 Generated Scenarios</h2>", unsafe_allow_html=True)

    # Show scenarios
    if "scenarios" in st.session_state:
        for i, sc in enumerate(st.session_state["scenarios"]):
            st.markdown(f"<div class='glass-card'><b>{i+1}.</b> {sc}</div>", unsafe_allow_html=True)

        if st.button("🛠 Generate Full Testcases"):
            tcs = []
            errors = []

            with st.spinner("Generating testcases..."):
                for sc in st.session_state["scenarios"]:
                    try:
                        tc = generate_testcase(model_choice, context_text, sc, temperature)
                        tcs.append(tc)
                    except Exception as e:
                        errors.append({"scenario": sc, "error": str(e)})

            st.session_state["testcases"] = tcs
            st.session_state["tc_errors"] = errors

    # Testcases Viewer
    if "testcases" in st.session_state:
        tcs = st.session_state["testcases"]

        st.markdown("<h2 class='section-title'>📦 Testcases</h2>", unsafe_allow_html=True)

        for idx, tc in enumerate(tcs):
            with st.expander(f"Testcase {idx+1}: {tc.get('title','Untitled')}"):
                t1, t2, t3 = st.tabs(["🧩 JSON", "📄 Markdown", "📋 Steps"])

                with t1:
                    st.json(tc)

                with t2:
                    md = f"### {tc['title']}\n\n"
                    md += f"**Preconditions:** {tc['custom_preconds']}\n\n"
                    md += "### Steps:\n"
                    for s in tc["custom_steps_separated"]:
                        md += f"- {s['content']} → *{s['expected']}*\n"
                    st.markdown(md)

                with t3:
                    for s in tc["custom_steps_separated"]:
                        st.markdown(
                            f"<div class='glass-card'><b>{s['content']}</b><br>→ {s['expected']}</div>",
                            unsafe_allow_html=True
                        )

        # Coverage Metrics
        st.markdown("<h2 class='section-title'>📈 Coverage Metrics</h2>", unsafe_allow_html=True)

        num_cases = len(tcs)
        num_steps = sum(len(tc["custom_steps_separated"]) for tc in tcs)
        avg_steps = num_steps / num_cases if num_cases else 0
        score = min(100.0, num_steps * 3.0)

        c1, c2, c3 = st.columns(3)
        c1.metric("Testcases", num_cases)
        c2.metric("Total Steps", num_steps)
        c3.metric("Coverage Score", f"{score:.1f}%")

        # Export ZIP
        st.markdown("<h2 class='section-title'>📤 Export</h2>", unsafe_allow_html=True)

        if st.button("📦 Create ZIP Bundle"):
            buffer = io.BytesIO()

            with zipfile.ZipFile(buffer, "w") as z:
                # JSON
                z.writestr("testcases.json", json.dumps(tcs, indent=4))

                # CSV
                rows = []
                for tc in tcs:
                    for s in tc["custom_steps_separated"]:
                        rows.append({
                            "title": tc["title"],
                            "preconditions": tc["custom_preconds"],
                            "step": s["content"],
                            "expected": s["expected"]
                        })
                df = pd.DataFrame(rows)
                z.writestr("testcases.csv", df.to_csv(index=False))

                # Markdown
                md_full = ""
                for tc in tcs:
                    md_full += f"## {tc['title']}\n"
                    md_full += f"{tc['custom_preconds']}\n\n"
                    for s in tc["custom_steps_separated"]:
                        md_full += f"- {s['content']} → {s['expected']}\n"
                    md_full += "\n---\n"
                z.writestr("testcases.md", md_full)

                # Summary
                z.writestr("summary.txt", f"Generated {num_cases} testcases.")

            buffer.seek(0)
            st.download_button(
                "⬇️ Download ZIP",
                data=buffer.getvalue(),
                file_name="testcases_bundle.zip",
                mime="application/zip"
            )

    # Errors Section
    if st.session_state.get("tc_errors"):
        st.markdown("<h2 class='section-title'>⚠️ Generation Errors</h2>", unsafe_allow_html=True)
        for err in st.session_state["tc_errors"]:
            st.error(f"Scenario:\n{err['scenario']}\n\nError:\n{err['error']}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Gemini 2.5 + Streamlit")
