#!/usr/bin/env bash
set -euo pipefail
export PYTHONUNBUFFERED=1
streamlit run apps/apps.py --server.runOnSave=true