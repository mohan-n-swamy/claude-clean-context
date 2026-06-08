#!/usr/bin/env python3
"""Report eager skill-description token cost and optionally archive a global skill."""

import argparse
import math
import re
import shutil
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*", re.DOTALL)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Estimate standing token cost for Claude skills. "
            "Archiving a GLOBAL skill removes it from ALL projects; if it belongs "
            "to one project, move it into that project's local .claude/skills/."
        )
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        help="Override scan location. Default scans ~/.claude/skills/ and <cwd>/.claude/skills/ if present.",
    )
    parser.add_argument(
        "--archive",
        help="Move a global skill to ~/.claude/skills-archive/NAME. Reversible; never deletes.",
    )
    return parser.parse_args()


def frontmatter_value(body, key):
    pattern = re.compile(rf"^{re.escape(key)}:\s*(?P<value>.*)$", re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return ""
    value = match.group("value").strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def read_skill(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    name = skill_dir.name
    description = ""

    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return name, description

    match = FRONTMATTER_RE.match(text)
    if not match:
        return name, description

    body = match.group("body")
    name = frontmatter_value(body, "name") or name
    description = frontmatter_value(body, "description")
    return name, description


def token_estimate(name, description):
    return math.ceil(len(name + description) / 4)


def scan_dirs(override):
    cwd = Path.cwd()
    if override:
        path = override.expanduser()
        return [(path, "custom")] if path.exists() else []

    candidates = [
        (Path("~/.claude/skills").expanduser(), "global"),
        (cwd / ".claude" / "skills", "project"),
    ]
    return [(path, scope) for path, scope in candidates if path.exists()]


def collect_skills(scan_locations):
    rows = []
    for skills_dir, scope in scan_locations:
        for child in sorted(skills_dir.iterdir()):
            if not child.is_dir():
                continue
            name, description = read_skill(child)
            rows.append(
                {
                    "name": name,
                    "dir_name": child.name,
                    "path": child,
                    "scope": scope,
                    "tokens": token_estimate(name, description),
                }
            )
    return rows


def print_table(rows):
    rows = sorted(rows, key=lambda row: (-row["tokens"], row["name"]))
    if not rows:
        print("No skills found.")
        print("Total estimated standing skill-token cost: 0 (this loads every session)")
        return

    skill_width = max(len("skill"), *(len(row["name"]) for row in rows))
    scope_width = max(len("scope"), *(len(row["scope"]) for row in rows))

    print(f"{'skill'.ljust(skill_width)}  {'scope'.ljust(scope_width)}  ~tokens")
    print(f"{'-' * skill_width}  {'-' * scope_width}  -------")
    for row in rows:
        print(f"{row['name'].ljust(skill_width)}  {row['scope'].ljust(scope_width)}  {row['tokens']}")

    total = sum(row["tokens"] for row in rows)
    print(f"\nTotal estimated standing skill-token cost: {total} (this loads every session)")


def archive_skill(name):
    global_dir = Path("~/.claude/skills").expanduser()
    archive_dir = Path("~/.claude/skills-archive").expanduser()
    source = global_dir / name

    if not source.exists():
        matches = []
        if global_dir.exists():
            for path in global_dir.iterdir():
                if not path.is_dir():
                    continue
                frontmatter_name, _description = read_skill(path)
                if path.name == name or frontmatter_name == name:
                    matches.append(path)
        if len(matches) == 1:
            source = matches[0]

    if not source.exists() or not source.is_dir():
        print(f"error: global skill not found: {global_dir / name}", file=sys.stderr)
        return 2

    target = archive_dir / source.name
    if target.exists():
        print(f"error: archive target already exists: {target}", file=sys.stderr)
        return 2

    archive_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))
    print(f"Archived global skill:")
    print(f"  before: {source}")
    print(f"  after:  {target}")
    print("Reversible: move it back into ~/.claude/skills/ to restore it.")
    print("Caution: archiving a global skill removes it from all projects.")
    return 0


def main():
    args = parse_args()

    if args.archive:
        return archive_skill(args.archive)

    scan_locations = scan_dirs(args.skills_dir)
    rows = collect_skills(scan_locations)
    print_table(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
