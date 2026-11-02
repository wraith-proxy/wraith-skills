---
name: knowledge-base
description: "Use when something non-obvious is learned or decided: a quirk, a gotcha, a convention, a term or an architectural decision. Records it in the project's knowledge files, glossary or ADRs so it survives the session and is not relitigated."
license: MIT
metadata:
  source: MP@d1478fc:skills/engineering/domain-modeling/SKILL.md
---

# Knowledge Base

Actively build and sharpen the project's domain model and knowledge as you work: challenging terms, inventing edge-case scenarios, and writing glossary entries, decisions and gotchas down the moment they crystallise.

A glossary defines terms. When terms need relations and axioms, use wraith:ontology-modeling.

## Files

Taken from the `## wraith` block of the project's `AGENTS.md`, defaults in brackets:

- `knowledge_dir` [.claude/knowledge], holding `stack.md`, `decisions.md`, `gotchas.md`, `conventions.md`
- `glossary` [GLOSSARY.md]
- `adr_dir` [docs/adr]

If a key is missing, ask once and suggest `wraith:setup`.

## Rules

- Lead with the fact or rule, then one sentence on why it matters.
- Keep each entry under a paragraph.
- Update an existing entry instead of adding a near-duplicate.
- Decisions read decision, why, consequence. Gotchas read symptom, cause, fix.
- Never record file paths, code structure or git history; read those from the code.
- If a file does not exist, create it on first write; otherwise proceed silently.
- When a new decision conflicts with an ADR, write `_Contradicts ADR-NNNN (<title>), but worth reopening because <reason>._` and ask the user.

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives, each with its own glossary and ADR directory.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in the glossary, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update the glossary inline

When a term is resolved, update the glossary right there. Don't batch these up: capture them as they happen. Use the format in [glossary-format.md](references/glossary-format.md).

The glossary must be totally devoid of implementation details. Do not treat it as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [adr-format.md](references/adr-format.md).
