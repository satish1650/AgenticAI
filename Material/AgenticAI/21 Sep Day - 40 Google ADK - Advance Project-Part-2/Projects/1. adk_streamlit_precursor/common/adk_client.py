import os
import time
from typing import Any, Dict, List, Optional, Tuple
import requests

API_BASE = os.getenv("ADK_API_BASE", "http://localhost:8000")

class ADKClient:
    """Minimal HTTP client for the ADK API Server: create session + run turn."""

    def __init__(self, api_base: Optional[str] = None):
        self.api_base = api_base or API_BASE

    def create_session(self, app_name: str, user_id: str, session_id: Optional[str] = None) -> str:
        sid = session_id or f"session-{int(time.time())}"
        url = f"{self.api_base}/apps/{app_name}/users/{user_id}/sessions/{sid}"
        r = requests.post(url, headers={"Content-Type": "application/json"}, json={})
        r.raise_for_status()
        return sid

    def run(self, app_name: str, user_id: str, session_id: str, message: str) -> Dict[str, Any]:
        url = f"{self.api_base}/run"
        payload = {
            "app_name": app_name,
            "user_id": user_id,
            "session_id": session_id,
            "new_message": {"role": "user", "parts": [{"text": message}]},
        }
        r = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return {"raw": r.text}

    @staticmethod
    def parse_events_for_text(resp: Dict[str, Any]) -> str:
        """Extract final assistant text from typical ADK event payload."""
        events = []
        if isinstance(resp, dict) and "events" in resp and isinstance(resp["events"], list):
            events = resp["events"]
        elif isinstance(resp, list):
            events = resp
        else:
            events = [resp]

        final_text = ""
        for ev in events:
            content = ev.get("content", {})
            parts = content.get("parts", []) if isinstance(content, dict) else []
            for p in parts:
                if "text" in p and isinstance(p["text"], str):
                    txt = p["text"].strip()
                    if txt:
                        final_text = txt  # keep last seen assistant text
        return final_text
