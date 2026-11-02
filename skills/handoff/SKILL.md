---
name: handoff
description: "Use when ending a session, when context is getting heavy, or when the user asks for a summary or handover. Narrates the decisions in order, marks anything that drifted from the user's latest intent, and writes a handover doc a fresh session can start from."
license: MIT
metadata:
  source: MP@d1478fc:skills/productivity/handoff/SKILL.md
---

## Narrate first

In plain words, without jargon, narrate each step of the session briefly in the order it actually happened. Bold anything in the current branch that drifted from the user's most recent stated intent.

## The handover document

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Write it to `<artifacts_dir>/<YYYY-MM-DD>-<topic>/handoff.md` with exactly these sections:

- `Read this first in a fresh session`
- `Rules from the owner (do not break)`: each rule with the incident or reason behind it.
- `Where we are`: repo path relative to the project, branch, HEAD sha, and the last test count with the command that produced it.
- `Done`: dated lines.
- `Open items`: numbered, each with the next command to run.
- `Where to look`: `path: purpose` lines.

Include a "suggested skills" list in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
