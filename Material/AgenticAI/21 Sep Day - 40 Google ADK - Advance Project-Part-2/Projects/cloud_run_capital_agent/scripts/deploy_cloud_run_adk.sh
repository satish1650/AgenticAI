#!/usr/bin/env bash
set -euo pipefail

: "${GOOGLE_CLOUD_PROJECT:?Set GOOGLE_CLOUD_PROJECT}"
: "${GOOGLE_CLOUD_LOCATION:?Set GOOGLE_CLOUD_LOCATION}"
: "${GOOGLE_GENAI_USE_VERTEXAI:?Set GOOGLE_GENAI_USE_VERTEXAI (True/False)}"

SERVICE_NAME="${SERVICE_NAME:-capital-agent-service}"
APP_NAME="${APP_NAME:-capital_agent}"
AGENT_PATH="${AGENT_PATH:-./capital_agent}"

echo "== Deploying ADK agent to Cloud Run =="
echo "Project: $GOOGLE_CLOUD_PROJECT"
echo "Region:  $GOOGLE_CLOUD_LOCATION"
echo "Service: $SERVICE_NAME"
echo "App:     $APP_NAME"
echo "Path:    $AGENT_PATH"
echo

adk deploy cloud_run   --project="$GOOGLE_CLOUD_PROJECT"   --region="$GOOGLE_CLOUD_LOCATION"   --service_name="$SERVICE_NAME"   --app_name="$APP_NAME"   --with_ui   "$AGENT_PATH"

echo
echo "If prompted about unauthenticated access:"
echo "  y  = public URL (easiest for demos)"
echo "  n  = private; use identity tokens for curl tests"
echo
echo "Done. The CLI above printed your service URL."
