#!/usr/bin/env python3
"""
Post-Compact Context Restoration Hook

Reads saved state and prints recovery context after compaction.
Hook Event: SessionStart (matcher: "compact|resume")
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
NC = "\033[0m"


def get_session_dir() -> Path:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return Path.home() / ".claude" / "sessions" / "default"
    import hashlib
    project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:8]
    session_dir = Path.home() / ".claude" / "sessions" / project_hash
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def read_pre_compact_state() -> dict | None:
    state_file = get_session_dir() / "pre-compact-state.json"
    if not state_file.exists():
        return None
    try:
        state = json.loads(state_file.read_text())
        state_file.unlink()
        return state
    except (json.JSONDecodeError, IOError):
        return None


def find_active_plan(project_dir: str) -> dict | None:
    plans_dir = Path(project_dir) / "quality_reports" / "plans"
    if not plans_dir.exists():
        return None
    plan_files = sorted(plans_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not plan_files:
        return None
    latest_plan = plan_files[0]
    content = latest_plan.read_text()
    status = "unknown"
    if "COMPLETED" in content.upper():
        status = "completed"
    elif "APPROVED" in content.upper():
        status = "in_progress"
    elif "DRAFT" in content.upper():
        status = "draft"
    current_task = None
    for line in content.split("\n"):
        if "- [ ]" in line:
            current_task = line.replace("- [ ]", "").strip()
            break
    return {"plan_path": str(latest_plan), "plan_name": latest_plan.name, "status": status, "current_task": current_task}


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        hook_input = {}

    session_source = hook_input.get("source", "")
    if session_source not in ("compact", "resume"):
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return 0

    pre_compact_state = read_pre_compact_state()
    plan_info = find_active_plan(project_dir)

    logs_dir = Path(project_dir) / "quality_reports" / "session_logs"
    session_log = None
    if logs_dir.exists():
        log_files = sorted(logs_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
        if log_files:
            session_log = {"log_name": log_files[0].name}

    if not (pre_compact_state or plan_info or session_log):
        return 0

    lines = [f"\n{CYAN}[Context Restored After Compaction]{NC}", ""]
    if pre_compact_state:
        lines.append(f"{GREEN}Pre-Compaction State:{NC}")
        if pre_compact_state.get("plan_path"):
            lines.append(f"  Plan: {pre_compact_state['plan_path']}")
        if pre_compact_state.get("current_task"):
            lines.append(f"  Task: {pre_compact_state['current_task']}")
        if pre_compact_state.get("decisions"):
            lines.append("  Recent decisions:")
            for d in pre_compact_state["decisions"][-3:]:
                lines.append(f"    - {d}")
        lines.append("")
    if plan_info:
        lines.append(f"{GREEN}Active Plan:{NC} {plan_info['plan_name']} ({plan_info['status']})")
        if plan_info.get("current_task"):
            lines.append(f"  Next task: {plan_info['current_task']}")
        lines.append("")
    if session_log:
        lines.append(f"{GREEN}Session Log:{NC} {session_log['log_name']}")
        lines.append("")
    lines.extend([
        f"{YELLOW}Recovery Actions:{NC}",
        "  1. Read the active plan to understand current objectives",
        "  2. Check git status/diff for uncommitted changes",
        "  3. Continue from where you left off", ""
    ])
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
