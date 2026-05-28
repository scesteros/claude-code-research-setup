#!/usr/bin/env python3
"""Static checker for broken cross-reference and file links in a LaTeX project.

Catches, before compilation, the failure modes that otherwise surface only as
"Reference ... undefined" / "File not found" warnings buried in the .log:

  - \\ref/\\eqref/\\cref/... that point to a \\label that is defined nowhere
  - duplicate \\label definitions (LaTeX "multiply defined")
  - \\input/\\include whose target file does not exist
  - \\includegraphics whose image file is not found on the graphics path

It is robust to two patterns this repo relies on, which defeat a naive
single-file grep:

  1. Labels that live inside \\input-ed files (e.g. the Step*.tex tables emit
     their own \\label, referenced from the main report). The checker follows
     \\input/\\include recursively, resolving path macros such as \\rkdinput.

  2. \\IfFileExists{cond}{true}{false} guards. Only the branch matching the
     on-disk state of <cond> is kept, so a placeholder \\label in the dead
     branch is not miscounted as a duplicate.

Usage:
    python check_latex_links.py path/to/main.tex [more.tex ...]

Exit code 0 if clean, 1 if any problem is found.
"""
from __future__ import annotations

import os
import re
import sys

LABEL_RE = re.compile(r"\\label\{([^}]*)\}")
REF_RE = re.compile(r"\\(?:eq|page|auto|name|c|C|v|vpage)?ref\*?\{([^}]*)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]*)\}")
GRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}")
GRAPHICSPATH_RE = re.compile(r"\\graphicspath\{(.+?)\}\s*$", re.DOTALL)
NEWCMD_RE = re.compile(
    r"\\(?:new|renew)command\*?\s*\{?\\([A-Za-z]+)\}?\s*(?:\[\d+\])?\s*\{"
)
DEF_RE = re.compile(r"\\def\s*\\([A-Za-z]+)\s*\{")
IMG_EXTS = (".png", ".pdf", ".jpg", ".jpeg", ".eps")


def read(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def strip_comments(text: str) -> str:
    """Truncate each line at the first unescaped %, preserving line count."""
    out = []
    for line in text.split("\n"):
        res = []
        backslashes = 0
        for ch in line:
            if ch == "%" and backslashes % 2 == 0:
                break
            res.append(ch)
            backslashes = backslashes + 1 if ch == "\\" else 0
        out.append("".join(res))
    return "\n".join(out)


def brace_group(text: str, i: int):
    """text[i] is '{'. Return (inner_start, close_index) or None."""
    depth = 0
    j = i
    n = len(text)
    while j < n:
        c = text[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return (i + 1, j)
        j += 1
    return None


def next_group(text: str, pos: int):
    """Find the next brace group at/after pos. Return (inner_start, inner_end, outer_end)."""
    k = pos
    n = len(text)
    while k < n and text[k] in " \t\r\n":
        k += 1
    if k >= n or text[k] != "{":
        return None
    g = brace_group(text, k)
    if not g:
        return None
    inner_start, close = g
    return (inner_start, close, close + 1)


def find_macros(text: str) -> dict:
    macros = {}
    for rx, has_body_brace in ((NEWCMD_RE, True), (DEF_RE, True)):
        for m in rx.finditer(text):
            name = m.group(1)
            g = brace_group(text, m.end() - 1)
            if not g:
                continue
            body = text[g[0]:g[1]]
            if "#" in body:  # macro takes arguments; skip
                continue
            macros[name] = body
    return macros


def resolve_macros(s: str, macros: dict) -> str:
    if not macros:
        return s
    for _ in range(10):
        changed = False

        def repl(m):
            nonlocal changed
            name = m.group(1)
            if name in macros:
                changed = True
                return macros[name]
            return m.group(0)

        s = re.sub(r"\\([A-Za-z]+)", repl, s)
        if not changed:
            break
    return s


def blank_span(chars: list, a: int, b: int) -> None:
    for k in range(a, b):
        if chars[k] != "\n":
            chars[k] = " "


def resolve_iffileexists(text: str, base_dir: str, macros: dict) -> str:
    """Keep only the live branch of each \\IfFileExists, blanking the rest
    (space-fill, newlines preserved so line numbers stay accurate)."""
    chars = list(text)
    guard = 0
    while True:
        guard += 1
        if guard > 10000:
            break
        s = "".join(chars)
        idx = s.find("\\IfFileExists")
        if idx < 0:
            break
        pos = idx + len("\\IfFileExists")
        g1 = next_group(s, pos)
        if not g1:
            blank_span(chars, idx, pos)
            continue
        g2 = next_group(s, g1[2])
        if not g2:
            blank_span(chars, idx, g1[2])
            continue
        g3 = next_group(s, g2[2])
        if not g3:
            blank_span(chars, idx, g2[2])
            continue
        cond = resolve_macros(s[g1[0]:g1[1]].strip(), macros)
        cond_full = (
            cond if os.path.isabs(cond) else os.path.normpath(os.path.join(base_dir, cond))
        )
        if os.path.exists(cond_full):  # keep TRUE branch inner
            blank_span(chars, idx, g2[0])
            blank_span(chars, g2[1], g3[2])
        else:  # keep FALSE branch inner
            blank_span(chars, idx, g3[0])
            blank_span(chars, g3[1], g3[2])
    return "".join(chars)


def collect_graphicspath(text: str, main_dir: str, macros: dict) -> list:
    dirs = []
    for m in GRAPHICSPATH_RE.finditer(text):
        for d in re.findall(r"\{([^{}]*)\}", m.group(1)):
            d = resolve_macros(d, macros)
            dirs.append(os.path.normpath(os.path.join(main_dir, d)))
    return dirs


class Results:
    def __init__(self, main_dir):
        self.main_dir = main_dir
        self.labels = {}           # name -> [(file, line), ...]
        self.refs = []             # (name, file, line)
        self.graphics = []         # (rawpath, file, line)
        self.missing_inputs = []   # (rawpath, resolved, file, line)
        self.graphicspath = []     # absolute search dirs


def resolve_input_target(raw: str, base_dir: str, macros: dict) -> str:
    p = resolve_macros(raw.strip(), macros)
    if not os.path.splitext(p)[1]:
        p += ".tex"
    return p if os.path.isabs(p) else os.path.normpath(os.path.join(base_dir, p))


def graphics_found(raw: str, res: Results, macros: dict) -> bool:
    p = resolve_macros(raw.strip(), macros)
    bases = [res.main_dir] + res.graphicspath
    cands = []
    for b in bases:
        full = p if os.path.isabs(p) else os.path.normpath(os.path.join(b, p))
        if os.path.splitext(full)[1]:
            cands.append(full)
        else:
            cands += [full + e for e in IMG_EXTS]
    return any(os.path.exists(c) for c in cands)


def process_file(path: str, macros: dict, visited: set, res: Results) -> None:
    path = os.path.normpath(path)
    if path in visited:
        return
    visited.add(path)
    if not os.path.exists(path):
        return
    base_dir = os.path.dirname(path)
    text = strip_comments(read(path))
    macros.update(find_macros(text))
    res.graphicspath += collect_graphicspath(text, res.main_dir, macros)
    text = resolve_iffileexists(text, base_dir, macros)

    for lineno, line in enumerate(text.split("\n"), 1):
        for m in LABEL_RE.finditer(line):
            res.labels.setdefault(m.group(1), []).append((path, lineno))
        for m in REF_RE.finditer(line):
            for name in m.group(1).split(","):
                name = name.strip()
                if name:
                    res.refs.append((name, path, lineno))
        for m in GRAPHICS_RE.finditer(line):
            res.graphics.append((m.group(1), path, lineno))
        for m in INPUT_RE.finditer(line):
            target = resolve_input_target(m.group(1), base_dir, macros)
            if os.path.exists(target):
                if target.endswith(".tex"):
                    process_file(target, macros, visited, res)
            else:
                res.missing_inputs.append((m.group(1), target, path, lineno))


def rel(p: str, root: str) -> str:
    try:
        return os.path.relpath(p, root)
    except ValueError:
        return p


def main(argv) -> int:
    if not argv:
        print("usage: python check_latex_links.py main.tex [more.tex ...]")
        return 2
    problems = 0
    for main_file in argv:
        main_file = os.path.normpath(main_file)
        if not os.path.exists(main_file):
            print(f"[ERROR] file not found: {main_file}")
            problems += 1
            continue
        root = os.path.dirname(os.path.abspath(main_file)) or "."
        res = Results(root)
        process_file(main_file, {}, set(), res)

        print(f"\n=== {main_file} ===")
        print(
            f"labels: {sum(len(v) for v in res.labels.values())} "
            f"({len(res.labels)} unique) | refs: {len(res.refs)} | "
            f"graphics: {len(res.graphics)} | inputs missing: {len(res.missing_inputs)}"
        )

        broken = sorted(
            {(n, f, l) for (n, f, l) in res.refs if n not in res.labels}
        )
        dups = {n: v for n, v in res.labels.items() if len(v) > 1}
        missing_gfx = [
            (raw, f, l)
            for (raw, f, l) in res.graphics
            if not graphics_found(raw, res, {})
        ]

        if broken:
            print(f"\n[BROKEN REFS] {len(broken)} reference(s) with no matching \\label:")
            for n, f, l in broken:
                print(f"  - \\ref{{{n}}}  at {rel(f, root)}:{l}")
        if dups:
            print(f"\n[DUPLICATE LABELS] {len(dups)} label(s) defined more than once:")
            for n, locs in sorted(dups.items()):
                where = ", ".join(f"{rel(f, root)}:{l}" for f, l in locs)
                print(f"  - \\label{{{n}}}  at {where}")
        if res.missing_inputs:
            print(f"\n[MISSING INPUT FILES] {len(res.missing_inputs)}:")
            for raw, target, f, l in res.missing_inputs:
                print(f"  - \\input{{{raw}}} -> {rel(target, root)}  (from {rel(f, root)}:{l})")
        if missing_gfx:
            print(f"\n[MISSING GRAPHICS] {len(missing_gfx)}:")
            for raw, f, l in missing_gfx:
                print(f"  - \\includegraphics{{{raw}}}  at {rel(f, root)}:{l}")

        n_prob = len(broken) + len(dups) + len(res.missing_inputs) + len(missing_gfx)
        if n_prob == 0:
            print("\nOK - no broken links found.")
        else:
            print(f"\nPROBLEMS: {n_prob} issue(s) found.")
            problems += n_prob

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
