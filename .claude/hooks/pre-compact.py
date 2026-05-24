#!/usr/bin/env python3
"""
Pre-Compact State Capture Hook

Captures active plan path, current task, and recent decisions before compaction.
Hook Event: PreCompact
"""

from __future__ import annotations

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime
import hashlib

CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
NC = "\033[0m"


def get_session_dir() -> Path:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return Path.home() / ".claude" / "sessions" / "default"
    project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:8]
    session_dir = Path.home() / ".claude" / "sessions" / project_hash
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def find_active_plan(project_dir: str) -> dict | None:
    plans_dir = Path(project_dir) / "quality_reports" / "plans"
    if not plans_dir.exists():
        return None
    plan_files = sorted(plans_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    for plan_file in plan_files[:3]:
        content = plan_file.read_text()
        if "COMPLETED" in content.upper():
            continue
        status = "in_progress"
        if "APPROVED" in content.upper():
            status = "approved"
        elif "DRAFT" in content.upper():
            status = "draft"
        current_task = None
        for line in content.split("\n"):
            if "- [ ]" in line:
                current_task = line.replace("- [ ]", "").strip()
                break
        return {"plan_path": str(plan_file), "plan_name": plan_file.name, "status": status, "current_task": current_task}
    return None


def extract_recent_decisions(project_dir: str, limit: int = 3) -> list[str]:
    logs_dir = Path(project_dir) / "quality_reports" / "session_logs"
    if not logs_dir.exists():
        return []
    log_files = sorted(logs_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not log_files:
        return []
    content = log_files[0].read_text()
    decisions = []
    patterns = [r"Decision:\s*(.+)", r"Decided:\s*(.+)", r"Chose:\s*(.+)", r"→\s*(.+)"]
    for line in content.split("\n")[-50:]:
        for pattern in patterns:
            match = re.search(pattern, line.strip())
            if match and len(match.group(1)) > 10:
                decisions.append(match.group(1)[:100])
                if len(decisions) >= limit:
                    return decisions
    return decisions


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        hook_input = {}

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return 0

    plan_info = find_active_plan(project_dir)
    decisions = extract_recent_decisions(project_dir)

    state = {
        "trigger": hook_input.get("trigger", "auto"),
        "timestamp": datetime.now().isoformat(),
        "plan_path": plan_info["plan_path"] if plan_info else None,
        "plan_status": plan_info["status"] if plan_info else None,
        "current_task": plan_info.get("current_task") if plan_info else None,
        "decisions": decisions
    }

    state_file = get_session_dir() / "pre-compact-state.json"
    try:
        state_file.write_text(json.dumps(state, indent=2))
    except IOError:
        pass

    # Append note to session log
    logs_dir = Path(project_dir) / "quality_reports" / "session_logs"
    if logs_dir.exists():
        log_files = sorted(logs_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
        if log_files:
            try:
                with open(log_files[0], "a") as f:
                    f.write(f"\n\n---\n**Context compaction at {datetime.now().strftime('%H:%M')}**\n")
            except IOError:
                pass

    lines = [f"\n{YELLOW}Context compaction starting{NC}", ""]
    if plan_info:
        lines.append(f"{GREEN}State saved:{NC} {plan_info['plan_name']} ({plan_info['status']})")
        if plan_info.get("current_task"):
            lines.append(f"  Next task: {plan_info['current_task']}")
    lines.append(f"\n{CYAN}State will be restored after compaction.{NC}\n")
    print("\n".join(lines), file=sys.stderr)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
