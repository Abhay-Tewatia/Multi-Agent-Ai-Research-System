import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(page_title="AI Research Studio", page_icon="🔎", layout="wide")

# ---------- Custom styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: radial-gradient(circle at top left, #1e1b4b 0%, #0f172a 45%, #020617 100%);
    color: #e2e8f0;
}

.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem 1rem;
    animation: fadeDown 0.8s ease-out;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #818cf8, #38bdf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero p { color: #94a3b8; font-size: 1.05rem; }

.pipeline {
    display: flex; justify-content: center; gap: 0.6rem;
    flex-wrap: wrap; margin: 1.2rem 0 2rem 0;
}
.step {
    padding: 0.5rem 1rem; border-radius: 999px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(129,140,248,0.35);
    font-size: 0.85rem; color: #c7d2fe;
    animation: pulse 2.4s ease-in-out infinite;
}
.step:nth-child(2) { animation-delay: 0.3s; }
.step:nth-child(3) { animation-delay: 0.6s; }
.step:nth-child(4) { animation-delay: 0.9s; }

.card {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(148,163,184,0.15);
    border-radius: 18px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
    animation: fadeUp 0.6s ease-out;
}

.stTextInput input {
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
    padding: 0.9rem !important;
    font-size: 1rem !important;
}
.stTextInput input:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.25) !important;
}

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #0ea5e9) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 0.7rem 1.6rem !important;
    font-weight: 600 !important; transition: transform 0.2s, box-shadow 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(99,102,241,0.45) !important;
}

.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
.stTabs [data-baseweb="tab"] {
    background: rgba(30,41,59,0.6); border-radius: 10px;
    padding: 0.5rem 1rem; color: #94a3b8;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #6366f1, #0ea5e9) !important;
    color: white !important;
}

@keyframes fadeDown { from {opacity:0; transform:translateY(-12px);} to {opacity:1; transform:none;} }
@keyframes fadeUp   { from {opacity:0; transform:translateY(16px);}  to {opacity:1; transform:none;} }
@keyframes pulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(129,140,248,0.4); }
    50%     { box-shadow: 0 0 0 8px rgba(129,140,248,0); }
}
</style>
""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown("""
<div class="hero">
    <h1>AI Research Studio</h1>
    <p>Multi-agent research, written and reviewed automatically</p>
</div>
<div class="pipeline">
    <div class="step">🔍 Search Agent</div>
    <div class="step">📖 Reader Agent</div>
    <div class="step">✍️ Writer Chain</div>
    <div class="step">🧐 Critic Chain</div>
</div>
""", unsafe_allow_html=True)

# ---------- Input ----------
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of AI on healthcare",
        label_visibility="collapsed",
    )
with col2:
    run = st.button("Generate Report", type="primary", use_container_width=True)

# ---------- Run ----------
if run:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        progress = st.progress(0, text="Starting agents...")
        try:
            with st.spinner("Agents are researching, writing and reviewing..."):
                state = run_research_pipeline(topic)
            progress.progress(100, text="Done!")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

        st.balloons()
        st.success(f"Report ready for: {topic}")

        tab1, tab2, tab3, tab4 = st.tabs(
            ["📄 Report", "🔍 Search", "🌐 Scraped", "🧐 Critic"]
        )

        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(state["report"])
            st.markdown('</div>', unsafe_allow_html=True)
            st.download_button(
                "⬇️ Download report (.md)",
                data=state["report"],
                file_name="report.md",
                mime="text/markdown",
            )

        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(state["search_results"])
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(state["scraped_content"])
            st.markdown('</div>', unsafe_allow_html=True)

        with tab4:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(state["feedback"])
            st.markdown('</div>', unsafe_allow_html=True)