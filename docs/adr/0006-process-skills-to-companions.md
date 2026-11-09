# ADR 0006: process skills to companions

Status: proposed. Date: 2026-11-09. Ticket: WSK-00108.

## Context

`github/awesome-copilot` rejected wraith in issue #6233, judged at v0.5.7 (`b65516b`). The reviewer wrote:

> Most of this is an opinionated plan/build/review/ship workflow adapted from superpowers, gstack and mattpocock/skills, with a session-start hook that injects the router into every session and a command guard that overlaps Copilot's built-in tool permission controls. The GCP, dbt and ODCS rules have real value, but your with-versus-without benchmark has no results yet and the evals run in Claude Code, so meaningful Copilot uplift isn't demonstrated. It doesn't yet show enough differentiated value for this marketplace; a focused data-engineering plugin with benchmark results would be a stronger submission.

Already fixed:

- Hooks and guard: removed in v0.6.0 (ADR 0005).
- Benchmark results: published in wraith-benchmarks on 2026-11-07, testing wraith v0.6.0 (`575afc1`) in Claude Code 2.1.316.
  - Plan review: 131 vs 100 of 180 planted problems.
  - ODCS: 25 of 25 vs 2 of 25 valid contracts.
  - Destructive commands: run in 9 of 25 runs with wraith, 21 of 25 without.
- wizard: removed in v0.7.0 (WSK-00107, #108) to clear a Claude directory credential hold.

Still open:

1. Thirteen of the 28 skills at v0.6.1, and seven of the 12 agents, are generic process material copied from SP, MP and GS. Several are close to verbatim. One of the thirteen (wizard) is already gone; twelve remain.
2. There is no Copilot uplift measurement. Every eval and benchmark ran in Claude Code.
3. The Claude directory still holds v0.7.0 (`ba3b99b`) for content policy review: "Uses a credential from the user's machine", rule `MCP_FORWARDS_CREDENTIAL_ENV`, anchored on `.claude-plugin/plugin.json`. Removing wizard did not clear it. The manifest has no MCP servers, hooks or `userConfig`, so the scanner is matching text elsewhere in the plugin. Three places match the rule's description:
   - `skills/qa/SKILL.md:49` and `skills/cloud-run/references/rollout.md:32` tell the agent to run `curl` with `Bearer $(gcloud auth print-identity-token)`: a credential read from the user's machine, sent to a server.
   - `docs/adr/0002-companion-dbt.md:32` quotes a dbt MCP server config with a `uvx` command and a `DBT_TOKEN` for a hosted endpoint.

   The other directory findings (unrecognized listing fields, the `icon` field, the root agent-plugins `plugin.json`, images passed unread) say "No action needed" and get none.

wraith already names vendor skills instead of copying them: ADRs 0002 (dbt), 0003 (Google) and 0004 (HashiCorp), and docs/reference.md ("wraith does not copy vendor skills"). This ADR applies that rule to the process skills.

## Options

1. **Trim to data and GCP, name SP and MP as companions (chosen).**
   - Smallest plugin and least maintenance.
   - Answers the "adapted from" objection directly.
   - Users lose the built-in sprint and must install companions for it.
2. **Rewrite each process skill as a data-specific version.**
   - Keeps the sprint.
   - The skeletons stay derivative, so the objection stands, and 12 skills keep drifting from upstream.
3. **Split into two plugins, `wraith` and `wraith-workflow`, in one marketplace.**
   - Keeps users' workflows.
   - The copies remain and double the release and sync work. The submission would list only `wraith`, which is option 1 with extra upkeep.

Option 1 wins because it is the only one that removes the derived process text instead of moving it.

## Decision

wraith ships 15 data and GCP skills and 5 specialist agents. Generic process skills are named, never copied (G21), from two companions:

- obra/superpowers (SP)
- mattpocock/skills (MP)

garrytan/gstack (GS) is not recommended as a companion. It stays a credited source for the kept skills derived from it.

Process companions are named only in `using-wraith`, `setup` and the docs. No domain skill names them, so every kept skill works with no companion installed. Neither host enforces cross-plugin dependencies.

Where a companion instruction conflicts with a wraith data or GCP rule, the wraith rule wins. This is the same as in ADRs 0002 to 0004.

### Claude directory credential hold

wraith text never reads a credential and sends it anywhere. This removes every such pattern instead of asking a reviewer to confirm it, which the hold says clears it.

- The Cloud Run smoke test uses `gcloud run services proxy <service> --tag <tag> --region <region> --port 8080`, then `curl -fsS http://localhost:8080/healthz`. gcloud handles authentication itself; no token passes through the agent's command line.
- ADR 0002's dbt MCP row describes the risk without quoting a config or a token variable.
- No `userConfig` is added: wraith has no server of its own to send a credential to.

This ships first as its own fix PR (Card H, release 0.7.1). It is not held for the trim, because the directory review is waiting now.

### Execution model

Every card runs as one fresh subagent with no design judgement. The orchestrator writes the full card prompt before dispatch:

- the exact files the card may touch, and nothing else;
- for each change, either the exact old and new text, or the exact source section and destination heading for a move;
- the exact commit message;
- the exact verification commands, with their expected output.

The subagent executes the steps, runs the verification commands, commits, and reports the output. If any old text does not match, a command fails, or a step needs a choice the prompt does not make, it stops and reports without committing. The orchestrator then fixes the prompt; the subagent never improvises.

Models:

- **Sonnet, medium effort:** cards that move or merge skill text (Cards 1 to 4), where matching sections across files needs care but no design.
- **Haiku:** deletions, regeneration and doc amendments with supplied text (Cards 0, H, 5, 6, 7 and 9).

A reviewer subagent checks each card's diff against its prompt before the next card starts.

### Skills

| Skill | Derived from | Verdict | Reason |
|---|---|---|---|
| bigquery | new | keep | BigQuery cost, access and erasure rules; gains the BigQuery checklist and triage. |
| dbt-bigquery | new | keep | `ds` snapshots, contract tests and dev targets; gains the data tests, dbt checklist and triage. |
| odcs-contracts | new | keep | ODCS v3.2.0 writing and validation; benchmarked (25 of 25). |
| ontology-modeling | new | keep | Ontology YAML as the source of truth; no upstream equivalent. |
| context-layer | new | keep | Warehouse context for agents and text-to-SQL. |
| cloud-run | new | keep | Cloud Run services and jobs; gains the Cloud Run checklist and triage. |
| terraform-gcp | new | keep | `prevent_destroy`, WIF and additive IAM; gains the Terraform checklist and triage. |
| plan-data-review | GS (structure only) | keep | The checklist is wraith's own; the only skill called in plan review (57 of 60 runs). |
| plan-infra-review | GS (structure only) | keep | GCP blast-radius review; sibling of plan-data-review. |
| careful | GS | keep | GCP and data destructive-command list; benchmarked. |
| security-audit | GS, AA | keep | IAM, secrets, ingress and personal data on GCP; gains the CI checklist. |
| deploy | GS | keep | Cloud Run traffic splits and prod dbt runs, with the rollback written first. |
| qa | GS | keep | Proves dbt, contract and Cloud Run changes against a dev target. |
| setup | MP | keep | Writes the `## wraith` block that 12 kept skills read; five unused keys go. |
| using-wraith | SP, KA, GS | keep, rewritten | Router for 15 skills and 5 agents; the description no longer says "every session". |
| brainstorming | SP, GS | drop | Generic design dialogue; its data questions are already plan-data-review Step 0 and items 1 to 3, 6, 7 and 10. |
| writing-plans | SP | drop | Generic plan format. |
| orchestrating-agents | SP | drop | Generic subagent loop and card contract. |
| tdd | MP | drop | Generic; `references/data-tests.md` moves to dbt-bigquery. |
| systematic-debugging | SP, MP | drop | Generic; `references/data-infra-triage.md` is split into the four domain skills. |
| verification-before-completion | SP | drop | Generic. |
| grilling | MP | drop | Generic. |
| handoff | MP | drop | Generic. |
| knowledge-base | MP | drop | Generic; the `glossary` key stays in setup for ontology-modeling and context-layer. |
| writing-skills | MP, SP | drop | Writing skills is not data work. |
| review | MP, SP | drop | Generic two-axis review; `references/checklists.md` is split into the domain skills (the Python list is generic and goes). |
| ship | SP, MP, GS | drop | Near-verbatim SP finishing-a-development-branch; its qa.md gate is already a deploy precondition. |
| wizard | MP | removed | Removed in v0.7.0 (WSK-00107): its template read saved secrets from `.env` and pushed them to GitHub, which held the Claude directory review. |

### Agents

| Agent | Derived from | Verdict | Reason |
|---|---|---|---|
| data-engineer | AA | keep | dbt on BigQuery, contracts, backfills. |
| platform-engineer | AA | keep | Terraform, Cloud Run, IAM, WIF. |
| sre | AA | keep | GCP observability and incident triage. |
| security-engineer | AA | keep | GCP and data security; follows security-audit. |
| ontologist | AA | keep | Ontology and context-layer work. |
| architect | AA | drop | Generic design role; GCP shows in one line; depends on writing-plans. |
| implementer | SP | drop | SP implementer prompt; only orchestrating-agents dispatches it. |
| reviewer | SP, AA | drop | Only review and orchestrating-agents dispatch it. |
| tester | AA | drop | Generic; follows wraith:tdd. |
| junior-dev | AA | drop | Generic mechanical edits. |
| docs-writer | AA | drop | Generic documentation. |
| git-workflow-master | AA | drop | Generic git hygiene. |

Both hosts have general-purpose subagents built in, and SP's subagent-driven-development carries its own implementer and reviewer prompts.

## Companion review

| Key | Repository | Ref | SHA | License |
|---|---|---|---|---|
| SP | https://github.com/obra/superpowers | v7.0.1 | 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b | MIT |
| MP | https://github.com/mattpocock/skills | v1.3.2 | d1478fcb140db0b93c0c8df17bcfd311844749d0 | MIT |
| GS | https://github.com/garrytan/gstack | v1.91.318.0 | 1bd2330350a6aa978f5c91de3c0be97004d0617b | MIT |

- Reviewed 2026-11-09, read only, from `.upstream/<KEY>`. Each checkout's HEAD matches the SHA above.
- Scope: each `SKILL.md` listed below, the plugin manifests and the hooks. The skills were searched for commands, network calls, git writes and wording that pressures the agent to invoke skills. They were not read line by line; that is gate G1.
- Quotes are single sentences or single commands, kept short to show a risk or a conflict.

**Credential rule.** A companion skill that reads, captures or writes local credentials is a vetting risk. That covers `.env` files, tokens, auth files, cloud credentials and CI secrets. Such a skill gets "do not recommend" unless a later ADR clears it. This follows the credential hold that WSK-00107 cleared.

### SP

The plugin ships `hooks/hooks.json`, which has a `SessionStart` hook running `"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd" session-start` to inject `using-superpowers` into every session. Installing any SP skill through the plugin installs this hook too.

| Skill | Replaces | Risky instructions (quoted) | Conflicts with wraith rules | Verdict |
|---|---|---|---|---|
| `brainstorming` | brainstorming | Its description begins "You MUST use this before any creative work"; it offers a "Visual Companion" that starts a local server. | It writes and commits `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`, outside `artifacts_dir`. | recommend with caveat |
| `writing-plans` | writing-plans | `git commit -m "feat: add specific feature"` | "**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`", so the plan reviews must accept any path (Card 3). The project's commit format wins over the example. | recommend with caveat |
| `subagent-driven-development` | orchestrating-agents | Its final review deletes the plan workspace with `rm -rf <workspace>`. | none | recommend with caveat |
| `executing-plans` | orchestrating-agents (inline) | none | none | recommend |
| `dispatching-parallel-agents` | orchestrating-agents (parallel) | none | none | recommend |
| `using-git-worktrees` | orchestrating-agents (worktrees) | `if [ -f package.json ]; then npm install; fi` | It runs installs (npm, pip, poetry, cargo, go) without naming the download first (G11). | recommend with caveat |
| `test-driven-development` | tdd (alternative to MP `tdd`) | none | none | recommend |
| `systematic-debugging` | systematic-debugging | none | none | recommend |
| `verification-before-completion` | verification-before-completion | none | none | recommend |
| `requesting-code-review`, `receiving-code-review` | review | none | none | recommend |
| `finishing-a-development-branch` | ship | `git branch -D <feature-branch>`, only after the typed word `discard` | none; pushes only on the user's chosen option, which matches careful | recommend |
| `writing-skills` | writing-skills | none | none | recommend |
| `using-superpowers` | nothing | "If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill." | It is injected each session, the pattern ADR 0005 removed from wraith. | do not recommend (it installs with the plugin anyway) |
| `diagnosing-superpowers` | nothing | It reads session transcripts on disk and calls the GitHub API with `curl`. | outside wraith scope | do not recommend |

### MP

The plugin has no hooks. 13 of its 27 promoted skills set `disable-model-invocation: true`, so only the user can start them.

| Skill | Replaces | Risky instructions (quoted) | Conflicts with wraith rules | Verdict |
|---|---|---|---|---|
| `tdd` | tdd | none | none | recommend |
| `diagnosing-bugs` | systematic-debugging (alternative) | It replays captured payloads, which can hold personal data. | Personal-data rules from wraith:bigquery apply to captured payloads. | recommend with caveat |
| `grilling` | grilling | none | none | recommend |
| `handoff` | handoff | none; user-invoked only | none | recommend |
| `domain-modeling` | knowledge-base | none | Uses the same `GLOSSARY.md` and `docs/adr` defaults as the wraith block; keep `glossary` aligned. | recommend with caveat |
| `code-review` | review | "The issue tracker should have been provided to you." | Needs `setup-matt-pocock-skills` to run first. | recommend with caveat |
| `setup-matt-pocock-skills` | nothing (needed by `code-review`) | "This fits almost every repo; write it without asking." | It edits an `## Agent skills` block in CLAUDE.md or AGENTS.md and writes `docs/agents/`. It updates its own block in place and does not touch the `## wraith` block. | recommend with caveat |
| `pr` | ship (PR body) | none | none | recommend |
| `wizard` | wizard | It writes captured values to `.env` and GitHub secrets. | It reads and writes local credentials, so the credential rule applies. | do not recommend |
| `writing-for-agents` | writing-skills | none | none | recommend |
| the other 17 promoted skills | nothing | not read | not read | out of scope (not read) |

### GS

GS installs as one unit, so it is judged as a package.

- **Install route.** At the pin there is no `.claude-plugin` manifest. The documented route is `git clone` plus `./setup`, which needs Bun 1.4.2 or later.
- **Hooks.** "In team mode it registers the `SessionStart` auto-update hook (`gstack-session-update`; `./setup --no-team` skips it)." Setup also registers a default-on Stop hook in the user's Claude settings file, and asks before adding PreToolUse and PostToolUse hooks.
- **Network calls and credentials by default.** The README says the update check (GitHub requests) is on by default. "Outside reviews" are also on by default: they send code to Codex or Claude Code under the user's own login, which the credential rule covers.
- **GitHub Copilot.** Install is `./setup --host copilot` and the tier is `experimental`. The upstream notes say: "Unverified without a real Copilot CLI (why it is not `full`): autopilot may answer `ask_user` itself, plan mode blocks mutating shell commands, symlinked skill dirs need Copilot CLI 1.0.62 or later, and `COPILOT_HOME` other than `~/.copilot` is refused for now." Whether GS installs and works under Copilot is unknown to this project (gate G3).
- **Verdict: do not recommend.** Default calls home, use of local logins, registered hooks and a setup script all conflict with what wraith promises its users. No dropped skill needs GS: SP brainstorming covers office-hours, and SP finishing-a-development-branch, MP `pr` and wraith:deploy cover ship and land-and-deploy.

### Install

These commands are copied from the upstream READMEs. wraith has not run them yet (gate G2).

| Companion | Claude Code | Copilot CLI |
|---|---|---|
| SP | `/plugin install superpowers@claude-plugins-official` | `copilot plugin marketplace add obra/superpowers-marketplace`, `copilot plugin install superpowers@superpowers-marketplace` |
| MP | `claude plugin install mattpocock-skills@claude-plugins-official` | `copilot plugin marketplace add mattpocock/skills`, `copilot plugin install mattpocock-skills@mattpocock` |

`claude-plugins-official` and `obra/superpowers-marketplace` serve whatever version they list, which may not match the pins above. The MP plugin installs `wizard` with everything else, so the docs name the skills wraith recommends and say that `wizard` is not one of them.

## Rewiring

Every reference from a kept file to a dropped skill or agent is rewritten:

| File | Line | Now | Becomes |
|---|---|---|---|
| skills/plan-data-review/SKILL.md | 13, 14, 44, 79 | writing-plans, orchestrating-agents | "a written plan, by any author"; the plan path is the one the user gives, else the newest `plan.md` under `artifacts_dir`, else `docs/superpowers/plans/`; "before anyone builds it" |
| skills/plan-infra-review/SKILL.md | 13, 14, 44, 82 | same | same |
| skills/odcs-contracts/SKILL.md | 36 | wraith:brainstorming design | the request or design: objects, keys, owners, sensitive fields; ask for what is missing |
| skills/dbt-bigquery/SKILL.md | 52, 76 | wraith:tdd | `references/data-tests.md`; "for test-first work on a dbt model" |
| skills/terraform-gcp/SKILL.md | 60 | wraith:tdd | "plan-mode and mock tests for a module" |
| skills/ontology-modeling/SKILL.md | 26, 38 | wraith:knowledge-base | write terms to the `glossary` file from the wraith block |
| skills/deploy/SKILL.md | 34, 60 | wraith:systematic-debugging | the "When it fails" section of wraith:cloud-run or wraith:dbt-bigquery |
| agents/data-engineer.md | 21 | wraith:systematic-debugging | "When it fails" in wraith:dbt-bigquery |
| agents/sre.md | 18 | wraith:systematic-debugging | "When it fails" in wraith:cloud-run and wraith:terraform-gcp |
| skills/using-wraith/** | all | sprint table, KA house rules, SP tool notes | rewritten router; `references/` deleted |
| skills/setup/SKILL.md | 39 to 45 | `test_command`, `lint_command`, `release_tooling`, `knowledge_dir`, `adr_dir` | removed (only ship and knowledge-base read them); step 5 gains one line naming SP and MP as optional |

The line numbers come from before WSK-00107; the implementer finds each line again with grep. After Card 5 this command must print nothing. `wizard` stays in the pattern to catch leftovers.

```bash
grep -rnE 'wraith:(brainstorming|writing-plans|orchestrating-agents|tdd|systematic-debugging|verification-before-completion|grilling|handoff|knowledge-base|writing-skills|review|ship|wizard|architect|implementer|reviewer|tester|junior-dev|docs-writer|git-workflow-master)\b' skills agents evals com.github.copilot README.md docs/reference.md docs/example AGENTS.md
```

## Effects

- **evals/.** Twelve trigger evals go: brainstorming, writing-plans, orchestrating-agents, tdd, systematic-debugging, verification-before-completion, grilling, handoff, knowledge-base, writing-skills, review and ship (trigger-wizard went in v0.7.0). Fourteen trigger evals and all five quality evals stay. These evals still run in Claude Code only, so Copilot evidence comes from gate G4, not from `evals/`.
- **README.**
  - "27 + 12" becomes "15 + 5".
  - "Start here" loses orchestrating-agents.
  - "One sprint" becomes "Where wraith fits": wraith covers plan review, contracts, domain builds, security, QA, deploy and careful; the general workflow comes from your own process or the companions.
  - The "One sprint" bullet in "Why wraith" goes.
  - The FAQ answer "Do I need GCP?" is rewritten.
  - Proof numbers are labelled "wraith v0.6.0, Claude Code" until G4.
  - Companions adds SP and MP, and says SP installs a SessionStart hook of its own.
- **docs/reference.md.** The sprint table, 15 skill rows, 5 agent rows, the Superpowers and Matt Pocock install sections with their recommended skills and a note that MP's `wizard` is not recommended, and the review note "docs/adr/0002 to 0004" becoming "0002 to 0004 and 0006".
- **docs/example.** `sprint/review.md` and `sprint/ship.md` go, since the skills that wrote them are gone. The README table marks `design.md` and `plan.md` as inputs that wraith does not write, and keeps the Data review note.
- **THIRD_PARTY_NOTICES.md.**
  - GS, MP and AA stay, because kept files still carry their source lines.
  - SP and KA leave the derived list only if `grep -rnE 'SP@|KA@' skills agents` prints nothing. SP then moves to "Companions (not included)".
  - MP gets a companion note as well.
  - Credits in the README follow the same result.
- **.upstream and sync.**
  - SP and MP stay in `upstream-pins.txt`, so drift in a skill wraith names can trigger a re-vet.
  - KA is removed if its notice goes.
  - Today's "Companion drift" report covers DBT, GCP and TF. It has not been checked whether wraith-sync-upstream treats SP and MP as companions once no file derives from them (G5).
  - Seen, not changed here: the AA pin (`b859c51`) differs from the vendored and notice commit (`b37b5bb`).
- **com.github.copilot.** Regenerate it with `wraith-build-copilot`, never by hand. Its output must list five agents. If the tool does not delete generated agents whose source is gone, the fix goes into wraith-tooling (G6).
- **ADRs 0002 and 0004.** Each gets an addendum.
  - 0002: `adding-dbt-unit-test` is now named by wraith:dbt-bigquery, not wraith:tdd.
  - 0004: `terraform-style-guide` is named by the wraith:terraform-gcp review checklist, not wraith:review.
  - ADR 0001's evidence lines stay as history.
- **Users.**
  - `/wraith:<dropped>` commands and dispatches of the seven dropped agents stop working.
  - RELEASE_NOTES.md tells users what to install instead.
  - SP's writing-plans hands off to SP execution and knows nothing of wraith's plan reviews. The user, or the plan-review descriptions, must start the review.

## Benchmark impact

All three published results measure kept skills:

- **Plan review.** wraith:plan-data-review was called in 57 of 60 with-arm runs, and no other skill was called.
- **Careful.** careful was called in 11 of 40 with-arm runs, and "No other skill was called."
- **ODCS.** wraith:odcs-contracts was loaded in 25 of 25 with-arm runs.

Each benchmark compared the whole plugin against nothing, at v0.6.0. Removing skills that were never called should not lower these numbers, but that is a prediction, not a measurement. The README keeps the v0.6.0 label until the rerun.

**Gate G4.** Before the new submission issue, rerun plan review, careful and ODCS on the release tag of this change, in Claude Code and in GitHub Copilot CLI, with and without wraith. Publish the results in wraith-benchmarks.

- **Unchanged from 2026-11-07:** fixtures, answer keys, judge and runs per arm.
- **Logins:** subscription only (Copilot login; Claude Code login for the judge). No API keys.
- **Spend:** stays within the Copilot plan's included premium requests, with overage turned off. If the allowance does not cover about 250 runs, run plan review first.
- **The results file records:** the Copilot CLI version, the agent model, the wraith tag, per-arm skill-call counts from the traces, and Wilson 95% intervals.
- **Publication:** results are published whatever they show. If Copilot shows no uplift, the README and the submission say so.

## Release

This is a breaking change.

- PR title: `👻 break/WSK-00108: trim wraith to data and GCP skills, process skills become companions`.
- With `major_version_zero: true`, the bump is 0.7.0 to 0.8.0.
- RELEASE_NOTES.md carries the user paragraph (Card 6).

## Gates

- **G1:** read in full every SP and MP skill marked recommend before this ADR is accepted. Confirm that none reads or writes local credentials; any that does becomes "do not recommend".
- **G2:** run the install commands on both hosts as a throwaway user. Record the version that lands, the skill count, and whether SP's SessionStart hook runs under Copilot. Re-vet any version that differs from the pin.
- **G3:** GS under Copilot is unknown. Before any wraith text names GS, run `./setup --host copilot` as a throwaway user and record the result in an addendum.
- **G4:** the benchmark rerun above, before the resubmission.
- **G5:** confirm, or fix in wraith-tooling, that sync watches the SP and MP skills that wraith names.
- **G6:** confirm that `wraith-build-copilot` deletes generated agents whose source is gone.
- **G7:** after Card H is released, the owner clicks "Check for new commits" in the directory. If the hold remains on 0.7.1, the owner replies to the reviewer that wraith has no MCP servers and no credential-reading text, and links this ADR.

## Consequences

- wraith becomes 15 skills and 5 agents, all data or GCP.
- The remaining derived text is GS structure, MP setup and AA agents.
- Kept skills work alone. Companions are optional, and are named only in the router, setup and the docs.
- The sprint is no longer a wraith feature. Users who want it install SP and MP.
- Companion skills that handle local credentials are never recommended without a new ADR.
- If the pins move, the companion review here is re-run before the docs change.

## Plan

Card H is its own branch and PR, merged first. Cards 1 to 7 then run on one branch with one commit per card, and that PR is squash-merged. Each card follows the Execution model above. Each acceptance list ends with `uvx --python 3.12 pre-commit run --all-files` passing.

### Card 0: commit this ADR (haiku)
**Owns:** docs/adr/0006-process-skills-to-companions.md.
**Acceptance:** `grep -c $'\xe2\x80\x94' docs/adr/0006-process-skills-to-companions.md` prints `0`.
**Commit:** `👻 docs/WSK-00108: add ADR 0006 process skills to companions`

### Card H: clear the credential hold (haiku, own PR)
**Owns:** skills/qa/SKILL.md, skills/cloud-run/references/rollout.md, docs/adr/0002-companion-dbt.md.
**Decisions:** replace both `curl ... print-identity-token` lines with the proxy pair from the Decision; replace the ADR 0002 line 32 quote cell with "It writes an MCP server config that starts a downloaded server and needs a dbt platform token."
**Acceptance:**
- `git grep -nE 'print-(identity|access)-token|DBT_TOKEN|Bearer' -- skills agents docs README.md` prints nothing.
- `claude plugin validate --strict .` passes.

**Commit:** `👻 fix/WSK-00108: smoke-test Cloud Run through gcloud proxy instead of a bearer token`

### Card 1: dbt and BigQuery salvage (sonnet, medium)
**Owns:** skills/dbt-bigquery/SKILL.md, skills/dbt-bigquery/references/data-tests.md (new), skills/bigquery/SKILL.md, skills/odcs-contracts/SKILL.md.
**Decisions:**
- Copy `skills/tdd/references/data-tests.md` verbatim to the new file and link it from dbt-bigquery.
- From `review/references/checklists.md`: "dbt and SQL" goes to a dbt-bigquery `## Review checklist`; "BigQuery" goes to bigquery; "Contracts and ontology" goes to odcs-contracts. Skip lines that are already rules.
- From `data-infra-triage.md`: the dbt and BigQuery sections go to a `## When it fails` section in those skills.
- Apply the Rewiring rows for these files.

**Acceptance:**
- `test -f skills/dbt-bigquery/references/data-tests.md`
- `grep -n 'bq show -j' skills/bigquery/SKILL.md` prints 1 line.
- The Rewiring grep, limited to these three skill folders, prints nothing.

**Commit:** `👻 refactor/WSK-00108: move data tests, checklists and triage into dbt and BigQuery skills`

### Card 2: infra salvage (sonnet, medium)
**Owns:** skills/cloud-run/SKILL.md, skills/terraform-gcp/SKILL.md, skills/security-audit/SKILL.md.
**Decisions:**
- The Cloud Run and Terraform checklists and triage sections go to those skills.
- "CI" goes to security-audit. "Python" goes nowhere.
- Apply the terraform-gcp Rewiring row.

**Acceptance:**
- `grep -n 'force-unlock' skills/terraform-gcp/SKILL.md` prints a line.
- `grep -n 'PORT' skills/cloud-run/SKILL.md` prints a line.
- `grep -n 'full SHA' skills/security-audit/SKILL.md` prints a line.
- The Rewiring grep, limited to these three folders, prints nothing.

**Commit:** `👻 refactor/WSK-00108: move infra checklists and triage into Cloud Run, Terraform and security skills`

### Card 3: standalone plan reviews, deploy, ontology and agents (sonnet, medium)
**Owns:** skills/plan-data-review/SKILL.md, skills/plan-infra-review/SKILL.md, skills/ontology-modeling/SKILL.md, skills/deploy/SKILL.md, agents/data-engineer.md, agents/sre.md.
**Decisions:** the Rewiring rows for these files, including the plan-path rule.
**Acceptance:** the Rewiring grep over these six files prints nothing.
**Commit:** `👻 refactor/WSK-00108: make kept skills and agents standalone`

### Card 4: router and setup (sonnet, medium)
**Owns:** skills/using-wraith/**, skills/setup/SKILL.md.
**Decisions:**
- New description: "Use when the user asks what wraith does or which wraith skill or agent fits a data or GCP task. Lists the wraith skills and agents and the rules they share."
- The body has:
  - the 15 skills and 5 agents;
  - the rules: the wraith block; production changes, pushes, deletes and spending need the user's go-ahead; every number states its mechanism; careful before destructive commands; companions are optional and wraith's data and GCP rules win.
- No KA or SP sentence remains. Delete `references/`.
- `metadata.source` becomes `new`, or GS only if a GS line remains.
- In setup, remove the five keys and add the SP/MP line to step 5. That line names no credential-handling skill.

**Acceptance:**
- `grep -c 'every session' skills/using-wraith/SKILL.md` prints `0`.
- `grep -nE 'SP@|KA@' skills/using-wraith/SKILL.md` prints nothing.
- `ls skills/using-wraith` prints `SKILL.md`.
- `grep -nE 'test_command|lint_command|release_tooling|knowledge_dir|adr_dir' skills/setup/SKILL.md` prints nothing.

**Commit:** `👻 refactor/WSK-00108: shrink using-wraith to a router and trim setup keys`

### Card 5: delete (haiku)
**Owns:** the 12 dropped skill folders, the 7 dropped agents, the 12 trigger evals, and com.github.copilot/** (only through `wraith-build-copilot`).
**Acceptance:**
- `ls skills | wc -l` prints `15`.
- `ls agents | wc -l` prints `5`.
- `ls com.github.copilot/agents | wc -l` prints `5`.
- `ls -d evals/trigger-* | wc -l` prints `14`.
- The full Rewiring grep, minus the doc paths, prints nothing.
- `claude plugin validate --strict .` passes.
- If the generated agents remain after `wraith-build-copilot`, stop and report (G6).

**Commit:** `👻 refactor/WSK-00108: remove generic process skills, agents and their trigger evals`

### Card 6: docs (haiku)
**Owns:** README.md (all except Credits), docs/reference.md, docs/example/**, AGENTS.md, RELEASE_NOTES.md.
**Decisions:** the orchestrator writes every replacement paragraph and table row into the prompt, including the new "Where wraith fits" section and the companion install sections.
- Source: the README, reference and example items under Effects.
- AGENTS.md drops "run as a plan, build, review, ship sprint".
- RELEASE_NOTES body: "wraith now ships only its data and GCP skills. The process skills (brainstorming, writing-plans, orchestrating-agents, tdd, systematic-debugging, verification-before-completion, grilling, handoff, knowledge-base, writing-skills, review and ship) and the architect, implementer, reviewer, tester, junior-dev, docs-writer and git-workflow-master agents are gone. Install obra/superpowers and mattpocock/skills for those workflows; docs/reference.md lists which skill replaces which. The wraith block keys test_command, lint_command, release_tooling, knowledge_dir and adr_dir are no longer read."

**Acceptance:**
- The full Rewiring grep prints nothing.
- `grep -nE '2[78] \+ 12|2[78] skills' README.md docs/reference.md` prints nothing.

**Commit:** `👻 docs/WSK-00108: describe wraith as data and GCP skills with process companions`

### Card 7: notices, pins and ADR addenda (haiku)
**Owns:** THIRD_PARTY_NOTICES.md, upstream-pins.txt, the README.md Credits section, and appended addenda in docs/adr/0002-companion-dbt.md and docs/adr/0004-companion-hashicorp.md.
**Decisions:** keep one notice per key that `grep -rnE 'SP@|KA@|MP@|GS@|AA@' skills agents` still prints; apply the notices, pins and ADR items under Effects.
**Acceptance:** every key in that grep output has a notice, and no notice key is missing from it.
**Commit:** `👻 docs/WSK-00108: update notices, credits and companion ADR pointers`

The owner then runs G1 and G2, opens the break PR and merges it, which releases 0.8.0. Card H's ticket is shared: one ADR, one ticket.

### Card 8: benchmark (wraith-benchmarks repository, owner)
Run G4 on the 0.8.0 tag.
**Acceptance:** a results file names both hosts, the versions and models, the skill-call counts and the totals with intervals.

### Card 9: proof and resubmission (haiku)
**Owns:** the README.md Proof section and docs/launch/awesome-lists.md.
**Decisions:** every number links to a wraith-benchmarks commit; the counts become 15 and 5.
**Acceptance:** every number in the Proof section has a link to a commit.
**Commit:** `👻 docs/WSK-00108: add Copilot CLI benchmark results`

The owner then opens the new awesome-copilot submission issue.
