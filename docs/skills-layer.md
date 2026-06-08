# Skills Layer

Skills have a standing cost because each skill's name and description loads every session. The body can lazy-load later, but the eager catalog still consumes context.

The same standing-context rule applies:

> Keep a skill eager only if this project plausibly invokes it before you know you need it.

## Baseline First

Use `/context` in Claude Code to see your current context baseline. Then run:

```bash
python3 skills-report.py
```

The report scans:

- `~/.claude/skills/` for global skills
- `<cwd>/.claude/skills/` for project-local skills

It prints each skill, its scope, and a rough standing token estimate based on the skill name and description.

## Global Vs Project-Local

Global skills load in every project. Keep a skill global only when it is broadly useful across projects.

Project-local skills belong under:

```text
<project>/.claude/skills/
```

Use project-local scope when a skill is relevant to one repo or one class of work.

## Archive, Do Not Delete

To archive a global skill:

```bash
python3 skills-report.py --archive <skill-name>
```

This moves:

```text
~/.claude/skills/<skill-name>
```

to:

```text
~/.claude/skills-archive/<skill-name>
```

The move is reversible.

## Cross-Project Caution

Archiving a global skill removes it from all projects. If the skill simply belongs to a different project, move it into that project's local `.claude/skills/` directory instead of archiving it.

The goal is not to minimize skills blindly. The goal is to keep the eager catalog aligned with real use.
