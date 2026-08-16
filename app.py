"""
Streamlit UI for the multi-agent research pipeline.

Run with:
    streamlit run streamlit_app.py

Place this file at your project root (the same level as the `src/` folder)
so the import below resolves correctly. If you keep it somewhere else,
adjust the sys.path line accordingly.
"""

import os
import sys
import time
import traceback
from datetime import datetime

import streamlit as st

# --- Make sure the project root is importable -------------------------------
# Assumes this file lives at the project root, alongside `src/`.
# If you move it, point this at the folder that CONTAINS `src/`.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.pipelines.pipeline import run_research_pipeline

# --- Page config --------------------------------------------------------------
st.set_page_config(
    page_title="Research Pipeline",
    page_icon="🔎",
    layout="wide",
)

# --- Helpers -------------------------------------------------------------------
def extract_text(result) -> str:
    """Best-effort extraction of plain text from an agent/chain result."""
    if result is None:
        return ""
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        # LangGraph-style agent output with a messages list
        if "messages" in result and result["messages"]:
            last = result["messages"][-1]
            return getattr(last, "content", str(last))
        for key in ("output", "content", "text"):
            if key in result:
                return extract_text(result[key])
        return str(result)
    # Anything with a `.content` attribute (AIMessage, etc.)
    if hasattr(result, "content"):
        return result.content
    return str(result)


def init_state():
    defaults = {
        "pipeline_state": {},
        "is_running": False,
        "history": [],  # list of {topic, timestamp, state}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# --- Sidebar ---------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Pipeline")
    st.caption(
        "Search → Scrape → Write → Critique.\n\n"
        "Each stage calls the real agents from `src.agents.agent`."
    )
    st.divider()
    if st.session_state["history"]:
        st.subheader("Past runs")
        for i, run in enumerate(reversed(st.session_state["history"])):
            label = f"{run['topic'][:28]}{'…' if len(run['topic']) > 28 else ''}"
            if st.button(label, key=f"hist_{i}", use_container_width=True):
                st.session_state["pipeline_state"] = run["state"]
                st.rerun()
        if st.button("Clear history", use_container_width=True):
            st.session_state["history"] = []
            st.rerun()

# --- Header ------------------------------------------------------------------
st.title("🔎 Research Pipeline")
st.caption("Search, scrape, draft, and critique a report on any topic.")

topic = st.text_input(
    "Topic",
    placeholder="e.g. The impact of quantum computing on cryptography",
    label_visibility="collapsed",
)

run_clicked = st.button(
    "Run pipeline",
    type="primary",
    disabled=st.session_state["is_running"] or not topic.strip(),
)

st.divider()

# --- Pipeline execution --------------------------------------------------------
def run_pipeline_ui(topic: str):
    """
    Calls the real run_research_pipeline() from src/pipelines/pipeline.py directly.
    This is intentionally a thin wrapper — no reimplemented agent logic here — so the
    UI can never drift out of sync with what main.py actually runs.
    """
    st.session_state["is_running"] = True
    try:
        with st.status("Running the research pipeline…", expanded=True) as status:
            st.write("Searching → scraping → drafting → critiquing. This can take a minute or two.")
            st.write("Watch your terminal for step-by-step progress logs.")
            state = run_research_pipeline(topic)
            status.update(label="Pipeline complete", state="complete")
    except Exception as e:
        # Show the FULL traceback in the UI, not just the exception message,
        # so silent/partial failures are actually visible instead of hidden.
        st.error("Pipeline raised an exception — see full traceback below.")
        st.code(traceback.format_exc())
        st.session_state["is_running"] = False
        return None

    if not isinstance(state, dict) or not state:
        st.warning(
            f"run_research_pipeline() returned {state!r} instead of a populated dict. "
            "The pipeline ran without raising an error, but produced no usable result."
        )
        st.session_state["is_running"] = False
        return None

    # Normalize whatever shape run_research_pipeline() returns into plain strings
    for key in ("draft", "final", "sources", "topic"):
        if key in state:
            state[key] = extract_text(state[key]) if key != "sources" else state[key]

    st.session_state["last_debug_keys"] = list(state.keys())
    st.session_state["is_running"] = False
    return state


if run_clicked:
    result_state = run_pipeline_ui(topic)
    if result_state is not None:
        st.session_state["pipeline_state"] = result_state
        st.session_state["history"].append(
            {
                "topic": topic,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "state": result_state,
            }
        )
        st.rerun()

# --- Results -------------------------------------------------------------------
state = st.session_state["pipeline_state"]
if state:
    st.subheader("Results")
    if state.get("topic"):
        st.caption(f"Topic: {state['topic']}")

    tab_final, tab_draft, tab_sources = st.tabs(["✅ Final report", "📝 Draft", "🔗 Sources"])

    with tab_final:
        if state.get("final"):
            st.markdown(state["final"])
            st.download_button(
                "Download final report (.md)",
                data=state["final"],
                file_name="final_report.md",
                mime="text/markdown",
            )
        else:
            st.info("No final report yet. Run the pipeline above.")

    with tab_draft:
        if state.get("draft"):
            st.markdown(state["draft"])
        else:
            st.info("No draft yet.")

    with tab_sources:
        sources = state.get("sources")
        if sources:
            if isinstance(sources, (list, tuple, set)):
                for url in sources:
                    st.markdown(f"- {url}")
            else:
                st.markdown(sources)
        else:
            st.info("No sources yet.")
else:
    st.info("Enter a topic above and click **Run pipeline** to get started.")