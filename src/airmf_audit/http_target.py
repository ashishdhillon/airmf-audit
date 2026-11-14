from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Callable, Optional


def create_http_target(
    endpoint: str,
    model: str = "default",
    api_key: Optional[str] = None,
    timeout: float = 30.0,
) -> Callable[[str], str]:
    """Creates a callable completion function connecting to an OpenAI-compatible HTTP LLM endpoint.
    
    Supports Ollama, vLLM, LocalAI, LM Studio, OpenAI, and any compatible /v1/chat/completions server.
    """
    def target_fn(prompt: str) -> str:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
        }
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "airmf-audit/0.2.0",
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                resp_bytes = response.read()
                resp_json = json.loads(resp_bytes.decode("utf-8", errors="replace"))

                # Standard OpenAI format: choices[0].message.content
                if "choices" in resp_json and len(resp_json["choices"]) > 0:
                    choice = resp_json["choices"][0]
                    if "message" in choice and "content" in choice["message"]:
                        return choice["message"]["content"] or ""
                    if "text" in choice:
                        return choice["text"] or ""

                # Ollama /generate format fallback: {"response": "..."}
                if "response" in resp_json:
                    return resp_json["response"] or ""

                return str(resp_json)

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            return f"[HTTP_ERROR_{e.code}] {err_body}"
        except urllib.error.URLError as e:
            return f"[CONNECTION_ERROR] {e.reason}"
        except Exception as e:
            return f"[ERROR] {e}"

    return target_fn
