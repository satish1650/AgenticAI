"""
ADK API + Streamlit — Simple Q&A (with search text)

Goals:
- Be easy to read: few helpers, lots of inline comments, no cleverness.
- Show the 3 core calls:
    1) POST /apps/{app}/users/{user}/sessions/{session}  (create session)
    2) POST /run                                          (send a user message)
    3) GET  /list-apps, GET /apps/{app}/users/{user}/sessions  (discovery)
- Parse /run response safely whether it's a dict-with-"events" or a list of events.

Tip for instructors:
Walk from top to bottom. Each function does exactly one thing and is < 10 lines.
"""

from __future__ import annotations
import os, uuid, json, requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Config defaults (also editable in the sidebar) ────────────────────────────
API_DEFAULT = os.getenv("ADK_API_BASE", "http://localhost:8000")
APP_DEFAULT = os.getenv("ADK_APP_SIMPLE", "simple")
USER_DEFAULT = os.getenv("ADK_USER_ID", f"user-{uuid.uuid4()}")

# ── Streamlit page ────────────────────────────────────────────────────────────
st.set_page_config(page_title="ADK + Streamlit: Simple Q&A", layout="centered")
st.title("Q&A (shows search text)")
st.caption("Front end: Streamlit • Backend: ADK API • Tooling: Tavily MCP")

# ── Simple page state (kept explicit) ─────────────────────────────────────────
if "api_base" not in st.session_state:  st.session_state.api_base = API_DEFAULT
if "app_name" not in st.session_state:  st.session_state.app_name = APP_DEFAULT
if "user_id"  not in st.session_state:  st.session_state.user_id  = USER_DEFAULT
if "session_id" not in st.session_state: st.session_state.session_id = None
if "events" not in st.session_state:    st.session_state.events = []  # always a list

# ── One-liner HTTP helpers (timeout + error bubbling via raise_for_status) ────
def GET(url: str):
    r = requests.get(url, timeout=60); r.raise_for_status(); return r.json()

def POST(url: str, payload: dict):
    r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=120)
    r.raise_for_status(); 
    try:    return r.json()
    except requests.JSONDecodeError: return {"raw": r.text}

# ── Tiny API wrappers (just glue URLs) ────────────────────────────────────────
def create_session() -> str:
    sid = f"session-{uuid.uuid4()}"
    url = f"{st.session_state.api_base}/apps/{st.session_state.app_name}/users/{st.session_state.user_id}/sessions/{sid}"
    r = requests.post(url, json={}, headers={"Content-Type": "application/json"}, timeout=60)
    r.raise_for_status()
    st.session_state.session_id = sid
    return sid

def run_turn(question: str):
    payload = {
        "app_name":   st.session_state.app_name,
        "user_id":    st.session_state.user_id,
        "session_id": st.session_state.session_id,
        "new_message": {"role": "user", "parts": [{"text": question}]},
    }
    return POST(f"{st.session_state.api_base}/run", payload)

def list_apps():
    return GET(f"{st.session_state.api_base}/list-apps")

def list_sessions():
    return GET(f"{st.session_state.api_base}/apps/{st.session_state.app_name}/users/{st.session_state.user_id}/sessions")

# ── Response parsing kept obvious ─────────────────────────────────────────────
def normalize_events(resp) -> list[dict]:
    """Return a list of event dicts from either {"events":[...]} or [...] or {"raw":...}."""
    if isinstance(resp, list):  return resp
    if isinstance(resp, dict) and isinstance(resp.get("events"), list): return resp["events"]
    return []

def last_text(events: list[dict]) -> str:
    """Return the last non-empty text part we see."""
    text = ""
    for ev in events:
        parts = (ev.get("content") or {}).get("parts", [])
        for p in parts:
            if isinstance(p, dict) and isinstance(p.get("text"), str) and p["text"].strip():
                text = p["text"].strip()
    return text

def find_queries(events: list[dict]) -> list[str]:
    """Collect tool/function-call query strings from common shapes."""
    out, seen = [], set()

    def walk(x):
        if isinstance(x, dict):
            # functionCall.args.query
            if isinstance(x.get("functionCall"), dict):
                q = (x["functionCall"].get("args") or {}).get("query")
                if isinstance(q, str) and q.strip() and q not in seen: seen.add(q); out.append(q)
            # function_call.arguments.query
            if isinstance(x.get("function_call"), dict):
                q = (x["function_call"].get("arguments") or {}).get("query")
                if isinstance(q, str) and q.strip() and q not in seen: seen.add(q); out.append(q)
            # tool_request.arguments.query
            if isinstance(x.get("tool_request"), dict):
                q = (x["tool_request"].get("arguments") or {}).get("query")
                if isinstance(q, str) and q.strip() and q not in seen: seen.add(q); out.append(q)
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)

    walk(events)
    return out

# ── Sidebar: basic config + two GET buttons ───────────────────────────────────
with st.sidebar:
    st.subheader("Server & Session")
    st.text_input("ADK API Base", value=st.session_state.api_base, key="api_base")
    st.text_input("App Name",      value=st.session_state.app_name, key="app_name")
    st.text_input("User ID",       value=st.session_state.user_id,  key="user_id")

    if st.button("Create / Reset Session", use_container_width=True):
        try:
            sid = create_session()
            st.success(f"Session created: {sid}")
        except requests.HTTPError as e:
            st.error(f"Create session failed: {e}")

    if st.session_state.session_id:
        st.info(f"Active session: {st.session_state.session_id}")
    else:
        st.warning("Create a session to begin.")

    st.markdown("---")
    st.subheader("Quick GETs")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("List Apps", use_container_width=True):
            try: st.json(list_apps())
            except requests.HTTPError as e: st.error(f"/list-apps failed: {e}")
    with c2:
        if st.button("List Sessions", use_container_width=True):
            try: st.json(list_sessions())
            except requests.HTTPError as e: st.error(f"list sessions failed: {e}")

# ── Main: ask → answer → show search text (optional raw) ──────────────────────
st.divider()
st.subheader("Ask a question")
q = st.text_input("Your question", "What is retrieval augmented generation?")
colA, colB = st.columns([1,1])
with colA:
    ask = st.button("Ask", use_container_width=True)
with colB:
    show_raw = st.checkbox("Show raw events", value=False)

if st.session_state.session_id and ask:
    try:
        resp   = run_turn(q)
        events = normalize_events(resp)
        st.session_state.events = events

        st.success("Answer:")
        st.write(last_text(events) or "_(No final text found)_")

        st.subheader("Search text (from tool calls)")
        queries = find_queries(events)
        if queries:
            for qq in queries: st.code(qq, language="text")
        else:
            st.info("No search query detected in this turn.")
    except requests.HTTPError as e:
        st.error(f"/run failed: {e}")

if show_raw and st.session_state.events:
    st.subheader("Raw events")
    st.code(json.dumps(st.session_state.events, indent=2), language="json")
