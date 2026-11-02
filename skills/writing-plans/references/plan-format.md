# Plan format

Plans are written for agents that execute without making design decisions.

## Sections, in order
1. Title `# <Topic>: Implementation Plan`, then the agentic-worker header line.
2. The brief line: "This file is your brief. Work one card at a time, stop at each gate, and report."
3. Goal, Architecture (2 to 3 sentences), Tech stack, and Spec (a path, or "sections 1 to N of this file").
4. Ground truth: pinned versions, sources with tag and commit, facts checked and the date checked. Mark facts to re-verify.
5. Global constraints: numbered one-liners with exact values. Every card inherits them.
6. Review focus: up to five inputs or failure modes no card's tests cover, each with the test that pins it and its owning card.
7. Execution model: branches and worktrees, orchestrator duties, model and effort per card, concurrency limit, card contract, phase gate, host or device checks.
8. Phases: `## Phase N: <name> (<ticket>)`, the order cards may run in, the cards, then a gate line.
9. Cost and limits.
10. Not doing (ask if wanted).
11. Risks, each with a mitigation.
12. Decisions for the owner, numbered, each with its default.

## Card format
### Card <ID>: <name> (<model>, effort <level>)
**Owns:** the files and globs the card may create or modify. Everything else is forbidden.
**Sources:** upstream or project files with exact paths, plus tag and commit for upstream.
**Interfaces:** Consumes and Produces, with exact names and signatures, when code is involved.
**Decisions:** values, rules and text the card must use verbatim.
**Tests:** test names and what each asserts.
**Acceptance:** a checkbox list of commands, each with the output that means pass.
**Commit:** the exact message.

## Rules
- A card is the smallest unit with its own test cycle that a reviewer could reject while approving its neighbour.
- Every fact a prose-writing agent needs is inline in its card.
- Model per card: opus only for orchestration and hard synthesis, sonnet for implementation and review, haiku for mechanical edits with write-then-read-back.
- Gates say what to present, then stop. Push only after the owner's go.
- No em dashes.
