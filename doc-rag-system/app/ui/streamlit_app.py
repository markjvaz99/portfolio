import streamlit as st
import requests
import time
import json

API_URL = "http://rag-app:8000/api/v1/query/test-rag-stream"

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RAG Chat",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS (ChatGPT-inspired dark theme) ────────────────────────────────
st.markdown("""
<style>

/* Font only — SAFE */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&display=swap');

html, body {
    font-family: 'Sora', sans-serif;
    background-color: #0d0d0d;
    color: #ececec;
}
            
.chat-title {
    padding: 0rem 0 0rem;
    font-size: 3.2rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    position: relative;

    /* Gradient text */
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #22d3ee, #60a5fa);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    /* Glow */
    text-shadow: 0 0 8px rgba(96,165,250,0.25),
                 0 0 16px rgba(167,139,250,0.15);

    /* Animation */
    animation: gradientShift 6s ease infinite;
}

/* Gradient animation */
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Subtle scanning line effect */
.chat-title::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: -1px;
    width: 100%;
    height: 1px;

    background: linear-gradient(
        90deg,
        transparent,
        rgba(96,165,250,0.8),
        transparent
    );

    animation: scanLine 3s linear infinite;
}

@keyframes scanLine {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}


/* DO NOT touch Streamlit internal class system */

/* Sidebar styling (safe only) */
[data-testid="stSidebar"] {
    background-color: #171717;
    border-right: 1px solid #2a2a2a;
}

/* Chat message styling (safe) */
[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 0.9rem 1.2rem;
    margin: 0.4rem 0;
}

/* Input styling */
[data-testid="stChatInput"] {
    border-radius: 14px;
}
            
/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 0.9rem 1.2rem !important;
    margin: 0.35rem 0 !important;
    line-height: 1.65;
    font-size: 0.95rem;
    border: none !important;
    box-shadow: none !important;
}
            
            /* User bubble */
[data-testid="stChatMessage"][data-testid*="user"],
.stChatMessage:has([data-testid="chatAvatarIcon-user"]) {
    background-color: #1a1a2e !important;
}
 
/* Assistant bubble */
[data-testid="stChatMessage"][data-testid*="assistant"],
.stChatMessage:has([data-testid="chatAvatarIcon-assistant"]) {
    background-color: #141414 !important;
}
 
/* ── Source expander ── */
.stExpander {
    background: #1a1a1a !important;
    border: 1px solid #2c2c2c !important;
    border-radius: 10px !important;
    margin-top: 0.6rem;
}
.stExpander summary {
    font-size: 0.8rem !important;
    color: #888 !important;
    font-weight: 500;
    letter-spacing: 0.03em;
}
.stExpander summary:hover {
    color: #bbb !important;
}
.source-card {
    background: #111;
    border: 1px solid #252525;
    border-radius: 8px;
    padding: 0.65rem 0.9rem;
    margin: 0.4rem 0;
    font-size: 0.82rem;
    color: #ccc;
    line-height: 1.5;
}
.source-score {
    font-size: 0.72rem;
    color: #555;
    margin-top: 0.3rem;
    font-variant-numeric: tabular-nums;
}
 
/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: #1a1a1a !important;
    border: 1px solid #2e2e2e !important;
    border-radius: 14px !important;
    padding: 0.4rem 0.8rem !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #ececec !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.94rem !important;
}
[data-testid="stChatInput"] button {
    background: #2563eb !important;
    border-radius: 8px !important;
}
 
/* ── Thinking dots animation ── */
@keyframes blink {
    0%, 80%, 100% { opacity: 0.15; }
    40%           { opacity: 1; }
}
.thinking-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #555;
    margin: 0 2px;
    animation: blink 1.2s infinite;
}
.thinking-dot:nth-child(2) { animation-delay: 0.2s; }
.thinking-dot:nth-child(3) { animation-delay: 0.4s; }
.thinking-label {
    font-size: 0.82rem;
    color: #666;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0.4rem 0;
}

</style>
""", unsafe_allow_html=True)



# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Actions")
    st.divider()

    if st.button("📥 Ingest Documents", use_container_width=True):
        with st.spinner("Ingesting documents..."):
            try:
                res = requests.get(
                    "http://rag-app:8000/api/v1/query/ingest",
                    timeout=300,
                )
                if res.status_code == 200:
                    st.success(res.json().get("response", "Done"))
                else:
                    st.error(f"Failed ({res.status_code})")
            except Exception as e:
                st.error(str(e))

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        "<div style='position:absolute;bottom:1rem;font-size:0.75rem;color:#444;'>RAG Chat v2</div>",
        unsafe_allow_html=True,
    )


# ─── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []  # each item: {role, content, sources}


# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown('<div class="chat-title">🧠 RAG Chat Assistant</div>', unsafe_allow_html=True)


# ─── Render history ──────────────────────────────────────────────────────────
def render_sources(sources: list):
    """Render sources with progressive disclosure (collapsed + per-source expand)."""
    if not sources:
        return

    with st.expander(
        f"📚 {len(sources)} source{'s' if len(sources) > 1 else ''} retrieved",
        expanded=False
    ):
        for i, src in enumerate(sources, 1):
            text = src.get("text", "—")
            score = src.get("score", None)

            # ── Truncate preview ──
            preview = text[:180] + ("..." if len(text) > 180 else "")
            score_str = f"Score: {score:.4f}" if score is not None else ""

            # ── Individual collapsible source ──
            with st.expander(f"🔎 Source {i}", expanded=False):
                st.markdown(
                    f'<div class="source-card">{text}'
                    f'{"<div class=source-score>" + score_str + "</div>" if score_str else ""}'
                    f"</div>",
                    unsafe_allow_html=True,
                )

            # ── Preview shown outside (lightweight) ──
            st.markdown(
                f'<div class="source-card" style="opacity:0.7;">'
                f'<strong style="color:#888;font-size:0.75rem;">SOURCE {i} (preview)</strong><br>{preview}'
                f"</div>",
                unsafe_allow_html=True,
            )



for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            render_sources(msg["sources"])


# ─── Chat input ──────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask something...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input, "sources": []})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant turn
    with st.chat_message("assistant"):
        placeholder = st.empty()

        full_text = ""
        sources = []
        raw_chunks = []
        first_chunk = False
        start = time.time()

        # ── Thinking animation while waiting ──
        dot_html = (
            '<div class="thinking-label">'
            '<span class="thinking-dot"></span>'
            '<span class="thinking-dot"></span>'
            '<span class="thinking-dot"></span>'
            "</div>"
        )
        placeholder.markdown(dot_html, unsafe_allow_html=True)

        try:
            with requests.post(
                API_URL,
                json={"query": user_input},
                stream=True,
                timeout=120,
            ) as r:
                for chunk in r.iter_content(chunk_size=64, decode_unicode=True):
                    if chunk:
                        if not first_chunk:
                            first_chunk = True
                            placeholder.empty()
                        raw_chunks.append(chunk)
                        # Try to parse as JSON; if not complete yet, stream raw text
                        combined = "".join(raw_chunks)
                        try:
                            data = json.loads(combined)
                            # Valid JSON — extract structured fields
                            full_text = data.get("answer", combined)
                            sources = data.get("sources", [])
                            placeholder.markdown(full_text)
                        except json.JSONDecodeError:
                            # Still streaming — show raw accumulated text
                            placeholder.markdown(combined)

            # Final parse after stream closes
            combined = "".join(raw_chunks)
            try:
                data = json.loads(combined)
                full_text = data.get("answer", combined)
                sources = data.get("sources", [])
            except json.JSONDecodeError:
                full_text = combined
                sources = []

            placeholder.markdown(full_text)

        except Exception as e:
            full_text = f"⚠️ Error: {str(e)}"
            placeholder.markdown(full_text)

        # Render sources inline
        render_sources(sources)

    # Persist to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_text,
        "sources": sources,
    })