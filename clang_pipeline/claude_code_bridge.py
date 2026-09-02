from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


def claude_code_command() -> str | None:
    configured = os.environ.get("CLAUDE_CODE_BIN", "").strip()
    if configured:
        return configured
    return shutil.which("claude")


def claude_code_available() -> bool:
    return claude_code_command() is not None


def run_claude_code(
    question: str,
    *,
    system_prompt: str | None = None,
    model: str | None = None,
    cwd: Path | str | None = None,
    timeout: int = 600,
    json_schema: dict[str, Any] | None = None,
    add_dirs: list[Path | str] | None = None,
) -> dict[str, Any]:
    command = claude_code_command()
    if command is None:
        raise RuntimeError("未找到 Claude Code，请先安装 claude 或设置 CLAUDE_CODE_BIN")
    arguments = [command, "-p", question]
    if system_prompt:
        arguments += ["--append-system-prompt", system_prompt]
    if model:
        arguments += ["--model", model]
    for directory in add_dirs or []:
        arguments += ["--add-dir", str(directory)]
    arguments += ["--output-format", "json"]
    if json_schema:
        arguments += ["--json-schema", json.dumps(json_schema, ensure_ascii=False)]

    completed = subprocess.run(
        arguments,
        cwd=str(cwd or Path.cwd()),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Claude Code 执行失败: {completed.stderr.strip() or completed.stdout.strip()}"
        )
    payload = _parse_json_output(completed.stdout)
    if isinstance(payload, dict):
        return payload
    return {"result": completed.stdout.strip(), "raw": True}


def _parse_json_output(text: str) -> Any:
    cleaned = text.strip()
    if not cleaned:
        return {}
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(cleaned[start : end + 1])
            except json.JSONDecodeError:
                pass
    return cleaned
