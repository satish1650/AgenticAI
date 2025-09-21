# ADK + Streamlit (Precursor): Simple Q&A with Tavily MCP

This tiny project shows **exactly** how to wire a **Streamlit** front end to the **ADK API Server**.
It uses a **single agent** (`agents/simple/agent.py`) that calls **Tavily MCP** when it needs to search.

## 0) Prereqs
- Python 3.10+
- ADK installed in your environment (provides `adk api_server`)
- `GOOGLE_API_KEY` (for the model used by ADK)
- `TAVILY_API_KEY` (for the Tavily MCP search server)

## 1) Install front-end deps
```bash
pip install -r requirements.txt
```

## 2) Configure environment
```bash
cp .env.example .env
# edit .env and set TAVILY_API_KEY, GOOGLE_API_KEY
```

## 3) Start the ADK API server
From the project root (where `agents/` lives):
```bash
bash scripts/run_api_server.sh
# Server runs at http://localhost:8000   (Swagger: /docs)
```

## 4) Start the Streamlit app
In a new terminal:
```bash
bash scripts/run_streamlit.sh
```

## 5) Use it
- In the sidebar, click **Create / Reset Session**.
- Ask a question. The agent will call Tavily MCP if needed and return an answer.
- That’s it—the smallest useful pattern: **create a session → send a message → render text**.

---

## How it works (in one diagram)
```mermaid
flowchart LR
  UI[Streamlit ask_app.py] -- HTTP --> API[ADK API Server]
  API --> AGENT[Simple Q&A Agent]
  AGENT -. when needed .-> MCP[Tavily MCP (npx)]
  MCP --> AGENT --> API --> UI
```
