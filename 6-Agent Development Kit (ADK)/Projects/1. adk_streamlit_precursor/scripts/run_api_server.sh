#!/usr/bin/env bash
set -euo pipefail
# Launch the ADK API server from the repo root. It will auto-discover agents/simple/agent.py (root_agent).
export PYTHONUNBUFFERED=1
adk api_server -v .
