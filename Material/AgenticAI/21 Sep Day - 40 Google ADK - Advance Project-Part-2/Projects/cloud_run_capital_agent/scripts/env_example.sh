#!/usr/bin/env bash
# Copy to env.sh and 'source env.sh' before deploying.

# --- Choose ONE auth mode ---

# Vertex AI (recommended on GCP)
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_GENAI_USE_VERTEXAI=True

# OR AI Studio API key
# export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
# export GOOGLE_CLOUD_LOCATION="us-central1"
# export GOOGLE_GENAI_USE_VERTEXAI=False
# export GOOGLE_API_KEY="your-ai-studio-api-key"

# Optional names/path
export SERVICE_NAME="capital-agent-service"
export APP_NAME="capital_agent"
export AGENT_PATH="./capital_agent"
