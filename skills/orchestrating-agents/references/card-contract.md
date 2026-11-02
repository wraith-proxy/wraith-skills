## Appendix B: card prompt and report section

The orchestrator sends this prompt, filling the angle brackets:

```text
You are executing Card <ID> of PLAN.md in the worktree <path>.
Read only: PLAN.md section 3 (Global constraints), Card <ID>, the appendices it
cites, and the files it names. Do not read other cards.
Rules:
- Touch only the files the card owns. If you need anything else, stop and report.
- Follow the steps in order. Run every acceptance command and quote its output.
- Make exactly one commit with the card's message. Do not push.
- If a step is ambiguous, or a check fails twice, stop and report the question
  or the failure. Do not choose between designs.
- Deadline: epoch <seconds>.
Finish with the report section below.
```

Every agent body ends with this section, verbatim:

```markdown
## When you finish, report

Report in at most 200 words: the files you changed, the commands you ran with their results quoted, and anything you could not verify.
```

## Appendix D: reviewer checklist

1. Only owned files changed: `git diff --name-only <base>..HEAD`.
2. The reviewer re-runs every acceptance command; each passes, with its output quoted.
3. Lint prints `0 problems`, `build_copilot.py --check` is clean, and the privacy scan prints `0 findings`.
4. Frontmatter matches Appendix E or F exactly, except `metadata.source`.
5. Vendored files differ from `.upstream/<KEY>/<path>` only by the card's listed edits, Appendix C and G8.
6. Every rule the card marks verbatim appears verbatim.
7. No em dashes, private data, upstream tokens, or companion text copied in (G21).
8. No `TBD`, `TODO` or `Stub:` left in owned files (Card 1G excepted).
9. Exactly one commit, with the card's exact message, matching G4.
10. Every number in the implementer's report matches the artifact.

Verdict: APPROVE, or CHANGES with a numbered list of blockers.
