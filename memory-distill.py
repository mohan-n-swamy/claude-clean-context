#!/usr/bin/env python3
"""Distill Claude Code memory indexes into durable guard rails.

`MEMORY.md` should be an always-loaded guard-rail surface, not a status
board. A pointer earns standing context only when it must be active before
action, is not derivable elsewhere, and prevents a concrete recurring error.

The default for project/reference pointers is inverted: demote unless the
target contains an explicit allowlist stem. Demotion never deletes target
files; it only moves pointer lines from `MEMORY.md` to lazy `ARCHIVE.md`.
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


POINTER_RE = re.compile(r"^\s*-\s*\[(?P<title>[^\]]*)\]\((?P<target>[^)]*)\)(?P<rest>.*)$")
SESSION_20_RE = re.compile(r"session_20")
SESSION_RESUME_TITLE_RE = re.compile(r"session resume", re.IGNORECASE)
SESSION_YEAR_TITLE_RE = re.compile(r"\bSession 20\d\d\b")
CLOSED_RE = re.compile(r"\bCLOSED\b|\(resolved\)|\(done\)", re.IGNORECASE)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Dry-run or apply deterministic MEMORY.md distillation. "
            "Use --mem-dir for one memory dir or --all for ~/.claude/projects/*/memory/."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mem-dir", type=Path, help="Memory directory containing MEMORY.md")
    group.add_argument(
        "--all",
        action="store_true",
        help="Process every ~/.claude/projects/*/memory/ directory with a MEMORY.md",
    )
    parser.add_argument("--apply", action="store_true", help="Write MEMORY.md and ARCHIVE.md changes")
    parser.add_argument("--budget", type=int, default=60, help="Soft target pointer count")
    return parser.parse_args()


def memory_dirs(args):
    if args.mem_dir:
        mem_dir = args.mem_dir.expanduser()
        if not (mem_dir / "MEMORY.md").exists():
            raise FileNotFoundError(f"missing MEMORY.md in {mem_dir}")
        return [mem_dir]

    root = Path("~/.claude/projects").expanduser()
    return sorted(path.parent for path in root.glob("*/memory/MEMORY.md"))


def load_allowlist(mem_dir):
    allowlist_path = mem_dir / ".allowlist"
    stems = []
    if not allowlist_path.exists():
        return stems

    for raw_line in allowlist_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        stems.append(line.split()[0])
    return stems


def classify(title, target, rest, allowlist):
    target_text = target.lower()
    title_rest = f"{title} {rest}"

    if "resume-state" in target_text:
        return "keep"
    if "feedback_" in target_text:
        return "keep"
    if (
        "project_session_resume" in target_text
        or SESSION_20_RE.search(target)
        or SESSION_RESUME_TITLE_RE.search(title)
        or SESSION_YEAR_TITLE_RE.search(title)
    ):
        return "session-resume snapshot (canonical = resume-state/STATUS.md)"
    if CLOSED_RE.search(title_rest):
        return "closed/resolved/done"
    if "project_" in target_text or "reference_" in target_text:
        if any(stem in target for stem in allowlist):
            return "keep"
        return "project/reference status → retrieval layer (not allowlisted)"
    return "keep"


def truncate(line, width=90):
    line = line.strip()
    if len(line) <= width:
        return line
    return line[: width - 3] + "..."


def collapse_blank_lines(lines):
    output = []
    blank_count = 0
    for line in lines:
        if line.strip():
            blank_count = 0
            output.append(line)
        else:
            blank_count += 1
            if blank_count < 2:
                output.append(line)
    return output


def process_dir(mem_dir, apply, budget):
    memory_path = mem_dir / "MEMORY.md"
    allowlist = load_allowlist(mem_dir)
    lines = memory_path.read_text(encoding="utf-8").splitlines(keepends=True)

    kept_lines = []
    demoted = []
    pointer_count = 0

    for line in lines:
        match = POINTER_RE.match(line.rstrip("\n"))
        if not match:
            kept_lines.append(line)
            continue

        pointer_count += 1
        title = match.group("title")
        target = match.group("target")
        rest = match.group("rest")
        decision = classify(title, target, rest, allowlist)

        if decision == "keep":
            kept_lines.append(line)
        else:
            demoted.append((line, decision))

    after_count = pointer_count - len(demoted)
    print(f"{mem_dir}: {pointer_count} -> {after_count} pointers")

    if demoted:
        for line, reason in demoted:
            print(f"  DEMOTE: {truncate(line)}")
            print(f"          reason: {reason}")
    else:
        print("  Already lean")

    if after_count > budget:
        print(f"  WARNING: {after_count} pointers remain over soft budget {budget}")

    if apply and demoted:
        archive_path = mem_dir / "ARCHIVE.md"
        date = datetime.now(timezone.utc).date().isoformat()
        with archive_path.open("a", encoding="utf-8") as archive:
            archive.write(f"\n## Demoted {date}\n\n")
            for line, reason in demoted:
                archive.write(line if line.endswith("\n") else line + "\n")
                archive.write(f"  - reason: {reason}\n")

        rewritten = collapse_blank_lines(kept_lines)
        memory_path.write_text("".join(rewritten), encoding="utf-8")

    return len(demoted)


def main():
    args = parse_args()
    try:
        dirs = memory_dirs(args)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not dirs:
        print("No memory directories found.")
        return 0

    total_demoted = 0
    for mem_dir in dirs:
        total_demoted += process_dir(mem_dir, args.apply, args.budget)

    mode = "applied" if args.apply else "dry-run"
    print(f"Summary: {mode}; demoted {total_demoted} pointer(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
