"""Atomic write helper for files that may be on synced storage (Dropbox, OneDrive).

Avoids partial-write corruption by writing to a temp file in the same directory
and using ``os.replace`` (atomic on POSIX and on Windows).

Usage:
    from atomic_write import atomic_write
    atomic_write(Path("session-log.md"), "new content")

Pattern adapted from chrisblattman/claudeblattman skills/done.md (v1.11+).
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path


def atomic_write(path: str | os.PathLike, content: str, encoding: str = "utf-8") -> None:
    """Write ``content`` to ``path`` atomically.

    Writes to a temp file in the same directory, fsyncs, then renames. If the
    process is interrupted mid-write, the destination keeps its previous content.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(
        prefix=target.name + ".tmp.",
        dir=str(target.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding=encoding, newline="\n") as fh:
            fh.write(content)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, target)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def atomic_append(path: str | os.PathLike, content: str, encoding: str = "utf-8") -> None:
    """Append ``content`` to ``path`` atomically by reading + rewriting.

    Slower than ``open(..., 'a')`` but safe under concurrent sync. Use only for
    small files (<10 MB) like session logs and CSVs.
    """
    target = Path(path)
    if target.exists():
        existing = target.read_text(encoding=encoding)
    else:
        existing = ""
    atomic_write(target, existing + content, encoding=encoding)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        sys.stderr.write("Usage: atomic_write.py <path> <content>\n")
        sys.exit(2)
    atomic_write(sys.argv[1], sys.argv[2])
