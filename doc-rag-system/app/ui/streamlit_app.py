import streamlit as st
import requests
import time

API_URL = "http://rag-app:8000/api/v1/query/test-rag"
INGEST_URL = "http://rag-app:8000/api/v1/query/ingest"

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RAG Interface",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:       #0d0f14;
    --surface:  #13161e;
    --border:   #1f2433;
    --accent:   #5b7fff;
    --accent2:  #a78bfa;
    --text:     #e4e8f5;
    --muted:    #5a6282;
    --green:    #34d399;
    --red:      #f87171;
    --amber:    #fbbf24;
}

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

.stApp {
    background: var(--bg);
}

/* Subtle grid texture */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(91,127,255,.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(91,127,255,.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'DM Serif Display', serif;
    color: var(--text);
}

/* Sidebar section labels */
.sidebar-section {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.4rem 0 .4rem;
}

/* ── Page title ── */
.page-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    line-height: 1.1;
    background: linear-gradient(135deg, var(--text) 30%, var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
}

.page-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: .75rem;
    color: var(--muted);
    letter-spacing: .08em;
    margin-top: .2rem;
    margin-bottom: 2rem;
}

/* ── Query textarea ── */
.stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .95rem !important;
    transition: border-color .2s;
    resize: vertical;
}

.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(91,127,255,.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: .8rem !important;
    letter-spacing: .05em !important;
    padding: .55rem 1.4rem !important;
    transition: opacity .2s, transform .15s !important;
}

.stButton > button:hover {
    opacity: .88 !important;
    transform: translateY(-1px) !important;
}

/* Secondary (ingest) button */
.stButton.secondary > button {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}

/* ── Answer card ── */
.answer-card {
    background: linear-gradient(135deg, rgba(91,127,255,.08), rgba(167,139,250,.06));
    border: 1px solid rgba(91,127,255,.25);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0 1.6rem;
    position: relative;
    overflow: hidden;
}

.answer-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
    border-radius: 3px 0 0 3px;
}

.answer-card p {
    margin: 0;
    line-height: 1.75;
    font-size: 1rem;
}

/* ── Source expanders ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    margin-bottom: .6rem;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(91,127,255,.4) !important;
}

[data-testid="stExpander"] summary {
    font-family: 'DM Mono', monospace !important;
    font-size: .82rem !important;
    color: var(--text) !important;
}

/* ── Score badge ── */
.score-badge {
    display: inline-block;
    background: rgba(91,127,255,.15);
    color: var(--accent);
    font-family: 'DM Mono', monospace;
    font-size: .7rem;
    padding: .15rem .55rem;
    border-radius: 999px;
    border: 1px solid rgba(91,127,255,.3);
    margin-left: .5rem;
    vertical-align: middle;
}

/* Score colour tiers */
.score-high  { background: rgba(52,211,153,.12); color: var(--green);  border-color: rgba(52,211,153,.3); }
.score-mid   { background: rgba(251,191,36,.10);  color: var(--amber); border-color: rgba(251,191,36,.3); }
.score-low   { background: rgba(248,113,113,.10); color: var(--red);   border-color: rgba(248,113,113,.3); }

/* ── Status / info boxes ── */
.stAlert {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border) !important;
    margin: 2rem 0 1rem !important;
}

/* ── Metrics row ── */
.metric-pill {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: .3rem .9rem;
    font-family: 'DM Mono', monospace;
    font-size: .75rem;
    color: var(--muted);
    margin-right: .5rem;
}

.metric-pill span.val {
    color: var(--text);
    font-weight: 500;
}

/* Toggle / slider labels */
.stToggle label, .stSlider label {
    font-family: 'DM Mono', monospace !important;
    font-size: .8rem !important;
    color: var(--muted) !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--accent) !important;
}

/* Source text inside expander */
.source-text {
    font-size: .88rem;
    line-height: 1.7;
    color: #c4c9dc;
    padding: .2rem 0;
}

/* Query history item */
.history-item {
    padding: .5rem .7rem;
    border-radius: 8px;
    border: 1px solid var(--border);
    margin-bottom: .4rem;
    font-size: .82rem;
    color: var(--muted);
    cursor: pointer;
    transition: border-color .2s, color .2s;
    font-family: 'DM Mono', monospace;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.history-item:hover {
    border-color: var(--accent);
    color: var(--text);
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []   # list of {"query": str, "answer": str, "sources": list}
if "prefill_query" not in st.session_state:
    st.session_state.prefill_query = ""

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## RAG Settings")

    st.markdown('<p class="sidebar-section">Display</p>', unsafe_allow_html=True)
    show_scores = st.toggle("Show similarity scores", value=True)
    max_sources = st.slider("Max sources", 1, 20, 5)

    st.markdown('<p class="sidebar-section">History</p>', unsafe_allow_html=True)
    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history[-10:])):
            label = entry["query"][:60] + ("…" if len(entry["query"]) > 60 else "")
            if st.button(label, key=f"hist_{i}", use_container_width=True):
                st.session_state.prefill_query = entry["query"]
                st.rerun()
    else:
        st.caption("No queries yet.")

    if st.session_state.history:
        if st.button("🗑 Clear history", use_container_width=True):
            st.session_state.history = []
            st.rerun()

    st.markdown('<p class="sidebar-section">Data</p>', unsafe_allow_html=True)
    ingest = st.button("📥 Ingest Documents", use_container_width=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="page-title">RAG Interface</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">retrieval-augmented generation · semantic search</p>', unsafe_allow_html=True)

# ── Ingest handler ─────────────────────────────────────────────────────────────
if ingest:
    with st.spinner("Ingesting documents…"):
        try:
            res = requests.get(INGEST_URL, timeout=300)
            if res.status_code == 200:
                st.success("✅ " + res.json().get("response", "Ingestion complete."))
            else:
                st.error(f"Ingest failed — HTTP {res.status_code}")
        except Exception as e:
            st.error(f"Connection error: {e}")

# ── Query input ────────────────────────────────────────────────────────────────
query = st.text_area(
    "Query",
    value=st.session_state.prefill_query,
    height=110,
    placeholder="What would you like to know? …",
    label_visibility="collapsed",
)
st.session_state.prefill_query = ""  # reset after use

c1, c2 = st.columns([1, 7])
with c1:
    submit = st.button("Search →", use_container_width=True)

# ── Query handler ──────────────────────────────────────────────────────────────
if submit and query.strip():
    t0 = time.time()
    with st.spinner("Searching…"):
        try:
            res = requests.post(API_URL, json={"query": query.strip()}, timeout=300)
            elapsed = time.time() - t0

            if res.status_code == 200:
                data = res.json()
                answer  = data.get("answer", "No answer returned.")
                sources = data.get("sources", [])[:max_sources]

                # persist to history
                st.session_state.history.append({
                    "query": query.strip(),
                    "answer": answer,
                    "sources": sources,
                })

                # ── Metrics row ──
                st.markdown(
                    f'<div style="margin:1rem 0 .6rem">'
                    f'<span class="metric-pill">⏱ <span class="val">{elapsed:.2f}s</span></span>'
                    f'<span class="metric-pill">📚 <span class="val">{len(sources)}</span> source{"s" if len(sources) != 1 else ""}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                # ── Answer ──
                st.markdown("#### Response")
                st.markdown(
                    f'<div class="answer-card"><p>{answer}</p></div>',
                    unsafe_allow_html=True,
                )

                # ── Sources ──
                if sources:
                    st.markdown("#### Sources")
                    for i, s in enumerate(sources):
                        score = s.get("score", None)

                        # badge colour tier
                        if score is not None:
                            if score >= 0.75:
                                tier = "score-high"
                            elif score >= 0.5:
                                tier = "score-mid"
                            else:
                                tier = "score-low"
                            badge = f'<span class="score-badge {tier}">{score:.4f}</span>' if show_scores else ""
                        else:
                            badge = ""

                        label = f"Source {i + 1}{('  ·  ' + str(round(score, 4))) if (show_scores and score is not None) else ''}"

                        with st.expander(label):
                            st.markdown(
                                f'<div class="source-text">{s.get("text", "")}</div>',
                                unsafe_allow_html=True,
                            )
                else:
                    st.info("No source documents returned.")

            else:
                st.error(f"Request failed — HTTP {res.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the RAG backend. Is `rag-app` running?")
        except requests.exceptions.Timeout:
            st.error("Request timed out (300 s). The backend may be overloaded.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

elif submit and not query.strip():
    st.warning("Please enter a query before submitting.")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="font-family:\'DM Mono\',monospace;font-size:.7rem;color:#3a3f55;text-align:center">'
    'RAG Interface · Retrieval-Augmented Generation</p>',
    unsafe_allow_html=True,
)