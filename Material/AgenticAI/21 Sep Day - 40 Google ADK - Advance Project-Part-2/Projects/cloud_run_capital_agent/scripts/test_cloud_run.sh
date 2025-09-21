#!/usr/bin/env bash
set -euo pipefail

: "${APP_URL:?Set APP_URL to your Cloud Run service URL}"
AUTH=()
if [[ -n "${TOKEN:-}" ]]; then AUTH=(-H "Authorization: Bearer $TOKEN"); fi

APP_NAME="${APP_NAME:-capital_agent}"
USER_ID="${USER_ID:-user_123}"
SESSION_ID="${SESSION_ID:-session_abc}"

echo "== List apps =="
curl -sS "${AUTH[@]}" -X GET "$APP_URL/list-apps" | jq . || true

echo
echo "== Create/Update session =="
curl -sS "${AUTH[@]}" -X POST "$APP_URL/apps/$APP_NAME/users/$USER_ID/sessions/$SESSION_ID"   -H "Content-Type: application/json"   -d '{}' | jq . || true

echo
echo "== Run once (non-streaming) =="
curl -sS "${AUTH[@]}" -X POST "$APP_URL/run"   -H "Content-Type: application/json"   -d '{
    "app_name": "'"$APP_NAME"'",
    "user_id": "'"$USER_ID"'",
    "session_id": "'"$SESSION_ID"'",
    "new_message": {
      "role": "user",
      "parts": [{"text": "What is the capital of Canada?"}]
    }
  }' | jq . || true

echo
echo "== (Optional) Streaming via SSE =="
echo "Use /run_sse and pipe 'data:' lines to jq -s"
echo "curl -s -N ${AUTH:+-H "Authorization: Bearer $TOKEN"} -X POST "$APP_URL/run_sse" -H "Content-Type: application/json" -d '{...}' | sed -n 's/^data: //p' | jq -s ."
