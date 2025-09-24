#!/usr/bin/env bash
set -euo pipefail

# ---- Config (env overrides supported) ----
API_BASE="${ADK_API_BASE:-http://localhost:8000}"
APP_NAME="${ADK_APP_SIMPLE:-simple}"
USER_ID="${ADK_USER_ID:-test-user}"
SESSION_ID="test-$(date +%s)"
QUESTION="${1:-What is retrieval augmented generation? Tell me with references}"

echo "== Create session =="
curl -s -X POST "$API_BASE/apps/$APP_NAME/users/$USER_ID/sessions/$SESSION_ID" \
  -H "Content-Type: application/json" -d '{}' | jq .

echo
echo "== Ask =="
RESP=$(
curl -s -X POST "$API_BASE/run" -H "Content-Type: application/json" -d @- <<JSON
{
  "app_name": "$APP_NAME",
  "user_id": "$USER_ID",
  "session_id": "$SESSION_ID",
  "new_message": {"role":"user","parts":[{"text":"$QUESTION"}]}
}
JSON
)

echo
echo "== Full events (debug) =="
echo "$RESP" | jq .

echo
echo "== Final assistant text =="
echo "$RESP" | jq -r '
  (.. | objects | select(has("parts")) | .parts[]? | select(has("text")) | .text) // empty
' | awk 'NF{p=$0} END{print p}'

echo
echo "== Search text (queries used by tools) =="
echo "$RESP" | jq -r '
  [
    (.. | objects | .functionCall? | .args?.query?),
    (.. | objects | .function_call? | .arguments?.query?),
    (.. | objects | .tool_request? | .arguments?.query?)
  ]
  | flatten | map(select(. != null and . != "")) | unique | .[]?
' || true

echo
echo "== Done =="

