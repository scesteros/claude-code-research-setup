#!/usr/bin/env python3
"""
Context Usage Monitor Hook

Monitors context usage and provides progressive warnings.
Hook Event: PostToolUse (on common tools)
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RED = "\033[0;31m"
MAGENTA = "\033[0;35m"
NC = "\033[0m"

LEARN_THRESHOLDS = [40, 55, 65]
THRESHOLD_WARN = 80
THRESHOLD_CRITICAL = 90
THROTTLE_INTERVAL = 60


def get_session_dir() -> Path:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return Path.home() / ".claude" / "sessions" / "default"
    import hashlib
    project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:8]
    session_dir = Path.home() / ".claude" / "sessions" / project_hash
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def read_cache() -> dict:
    cache_file = get_session_dir() / "context-monitor-cache.json"
    if not cache_file.exists():
        return {}
    try:
        return json.loads(cache_file.read_text())
    except (json.JSONDecodeError, IOError):
        return {}


def save_cache(data: dict) -> None:
    cache_file = get_session_dir() / "context-monitor-cache.json"
    try:
        cache_file.write_text(json.dumps(data, indent=2))
    except IOError:
        pass


def estimate_context_percentage() -> float:
    cache = read_cache()
    tool_calls = cache.get("tool_calls", 0) + 1
    cache["tool_calls"] = tool_calls
    save_cache(cache)
    MAX_TOOL_CALLS = 150
    return min((tool_calls / MAX_TOOL_CALLS) * 100, 100)


def is_throttled(percentage: float) -> bool:
    cache = read_cache()
    last_check = cache.get("last_check_time", 0)
    now = time.time()
    if percentage < THRESHOLD_WARN and (now - last_check) < THROTTLE_INTERVAL:
        return True
    cache["last_check_time"] = now
    save_cache(cache)
    return False


def get_shown_thresholds() -> dict:
    cache = read_cache()
    return {
        "learn": cache.get("shown_learn", []),
        "warn_80": cache.get("shown_warn_80", False),
        "warn_90": cache.get("shown_warn_90", False)
    }


def mark_threshold_shown(threshold_type: str, value: int | bool = True) -> None:
    cache = read_cache()
    if threshold_type == "learn":
        shown = cache.get("shown_learn", [])
        if value not in shown:
            shown.append(value)
        cache["shown_learn"] = shown
    else:
        cache[f"shown_{threshold_type}"] = value
    save_cache(cache)


def run_context_monitor() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        hook_input = {}

    percentage = estimate_context_percentage()
    if is_throttled(percentage):
        return 0

    shown = get_shown_thresholds()

    for threshold in LEARN_THRESHOLDS:
        if percentage >= threshold and threshold not in shown["learn"]:
            print(f"\n{CYAN}Context at {percentage:.0f}%{NC}\n"
                  f"Non-obvious discovery? Consider using {GREEN}/learn{NC} to capture it.\n")
            mark_threshold_shown("learn", threshold)
            return 0

    if percentage >= THRESHOLD_CRITICAL and not shown["warn_90"]:
        print(f"\n{RED}Context at {percentage:.0f}% — auto-compact approaching{NC}\n"
              f"Complete current task with full quality.\n"
              f"{YELLOW}Actions:{NC} Save decisions to session log, update plan status.\n")
        mark_threshold_shown("warn_90", True)
        return 0

    if percentage >= THRESHOLD_WARN and not shown["warn_80"]:
        print(f"\n{YELLOW}Context at {percentage:.0f}%{NC}\n"
              f"Auto-compact will handle context management automatically.\n")
        mark_threshold_shown("warn_80", True)
        return 0

    return 0


if __name__ == "__main__":
    try:
        sys.exit(run_context_monitor())
    except Exception:
        sys.exit(0)
