from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5")
API_URL = "https://api.openai.com/v1/responses"


class LLMNotConfigured(RuntimeError):
    pass


def api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise LLMNotConfigured(
            "缺少 OPENAI_API_KEY，请先设置环境变量：export OPENAI_API_KEY=sk-..."
        )
    return key


def llm_enabled() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY", "").strip())


def complete_json(
    system_prompt: str,
    user_prompt: str,
    *,
    model: str | None = None,
    temperature: float = 0.2,
) -> dict[str, Any]:
    """调用 OpenAI Responses API，并要求模型返回 JSON 对象。"""
    payload = {
        "model": model or DEFAULT_MODEL,
        "instructions": system_prompt,
        "input": user_prompt,
        "temperature": temperature,
        "text": {"format": {"type": "json_object"}},
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LLM API 请求失败: {exc.code} {detail}") from exc

    output_text = data.get("output_text", "")
    if not output_text:
        output_text = _extract_output_text(data)
    return _parse_json_object(output_text)


def _extract_output_text(data: dict[str, Any]) -> str:
    parts: list[str] = []
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                parts.append(content.get("text", ""))
    return "\n".join(parts)


def _parse_json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"LLM 返回的不是合法 JSON: {text[:200]}") from exc
    if not isinstance(result, dict):
        raise RuntimeError("LLM 返回的 JSON 必须是 object")
    return result
