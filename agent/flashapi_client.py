import os
from typing import Optional

import requests

from .config import load_dotenv, getenv


load_dotenv()


class GeminiFlashClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or getenv("GEMINI_API_KEY")
        self.endpoint = getenv("GEMINI_FLASHAPI_ENDPOINT", "https://flashapi.googleapis.com/v1beta/generateText")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def explain_issue(self, prompt: str, source: str) -> Optional[str]:
        if not self.is_configured():
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gemini-flash",
            "prompt": {
                "text": prompt,
                "context": source,
            },
            "maxOutputTokens": 256,
        }
        try:
            response = requests.post(self.endpoint, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("outputText") or data.get("result", {}).get("outputText")
        except Exception:
            return None
