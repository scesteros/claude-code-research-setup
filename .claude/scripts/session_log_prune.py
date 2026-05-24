"""Prune session logs by tiered cutoffs based on file size.

Tiers (most aggressive first):

==================  =========================
File size           Cutoff (entries older are
                    archived to *_archive.md)
==================  =========================
> 10,000 lines      7 days  (emergency)
>  6,000 lines      14 days (busy)
>  3,000 lines      30 days (hard)
>  1,500 lines      60 days (soft)
<= 1,500 lines      no-op
==================  =========================

Default target: ``quality_reports/session_logs/*.md``.

Pattern adapted from chrisblattman/claudeblattman skills/done.md (v2.4):
moves the prune decision out of model-judgment ("should I prune now?") into a
deterministic helper that runs unconditionally.

Usage:
    python .claude/scripts/session_log_prune.py
    python .claude/scripts/session_log_prune.py --dir quality_reports/session_logs
    python .claude/scripts/session_log_prune.py --dry-run
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ENTRY_HEADER_RE = re.compile(
    r"^##\s*\[?(\d{4}-\d{2}-\d{2})",  # ## [YYYY-MM-DD ...] or ## YYYY-MM-DD ...
)


def pick_cutoff_days(num_lines: int) -> int | None:
    """Return cutoff in days based on file size, or ``None`` if no-op."""
    if num_lines > 10_000:
        return 7
    if num_lines > 6_000:
        return 14
    if num_lines > 3_000:
        return 30
    if num_lines > 1_500:
        return 60
    return None


def split_entries(text: str) -> list[tuple[str | None, str]]:
    """Split a session-log into ``(date_iso_or_None, body)`` chunks.

    Anything before the first dated header is returned with ``date=None`` and
    is always kept.
    """
    chunks: list[tuple[str | None, str]] = []
    current_date: str | None = None
    current_lines: list[str] = []
    for line in text.splitlines(keepends=True):
        m = ENTRY_HEADER_RE.match(line)
        if m:
            if current_lines:
                chunks.append((current_date, "".join(current_lines)))
            current_date = m.group(1)
            current_lines = [line]
        else:
            current_lines.append(line)
    if current_lines:
        chunks.append((current_date, "".join(current_lines)))
    return chunks


def prune_one_file(path: Path, dry_run: bool = False) -> dict:
    text = path.read_text(encoding="utf-8")
    num_lines = text.count("\n") + 1
    cutoff_days = pick_cutoff_days(num_lines)
    result = {"file": str(path), "lines": num_lines, "cutoff_days": cutoff_days}
    if cutoff_days is None:
        result["status"] = "no-op"
        return result

    cutoff_date = (datetime.utcnow() - timedelta(days=cutoff_days)).date()
    chunks = split_entries(text)
    keep: list[str] = []
    archive: list[str] = []
    for date_iso, body in chunks:
        if date_iso is None:
            keep.append(body)
            continue
        try:
            entry_date = datetime.strptime(date_iso, "%Y-%m-%d").date()
        except ValueError:
            keep.append(body)
            continue
        if entry_date < cutoff_date:
            archive.append(body)
        else:
            keep.append(body)

    result["archived_entries"] = sum(1 for d, _ in chunks if d and _ in archive)
    result["kept_entries"] = sum(1 for d, _ in chunks if d and _ in keep)

    if not archive:
        result["status"] = "no-op (nothing older than cutoff)"
        return result

    archive_path = path.with_name(path.stem + "_archive.md")
    if dry_run:
        result["status"] = f"DRY-RUN would archive {len(archive)} entries -> {archive_path.name}"
        return result

    # Append to archive (preserve existing archive)
    archive_existing = ""
    if archive_path.exists():
        archive_existing = archive_path.read_text(encoding="utf-8")
    archive_path.write_text(archive_existing + "".join(archive), encoding="utf-8")
    path.write_text("".join(keep), encoding="utf-8")
    result["status"] = f"archived {len(archive)} entries -> {archive_path.name}"
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--dir",
        default="quality_reports/session_logs",
        help="Directory containing session logs (default: quality_reports/session_logs)",
    )
    ap.add_argument(
        "--pattern",
        default="*.md",
        help="Glob pattern for session log files (default: *.md)",
    )
    ap.add_argument("--dry-run", action="store_true", help="Report decisions without writing")
    args = ap.parse_args()

    target_dir = Path(args.dir)
    if not target_dir.is_dir():
        print(f"[prune] target dir not found: {target_dir}", file=sys.stderr)
        return 1

    files = [p for p in target_dir.glob(args.pattern) if not p.name.endswith("_archive.md")]
    if not files:
        print(f"[prune] no files matching {args.pattern} in {target_dir}")
        return 0

    for path in files:
        info = prune_one_file(path, dry_run=args.dry_run)
        line = (
            f"[prune] {info['file']} ({info['lines']} lines, cutoff="
            f"{info['cutoff_days']}d): {info['status']}"
        )
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
