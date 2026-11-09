---
name: using-wraith
description: "Use at the start of every session and before any data, infrastructure or engineering task. Routes work to the right wraith skill (brainstorming, plans and plan reviews, orchestrating agents, dbt, BigQuery, Cloud Run, Terraform, ODCS contracts, ontology, review, QA, ship, deploy, handoff) and states the house rules every wraith skill follows."
license: MIT
metadata:
  source: SP@2ce8aa1:skills/using-superpowers/SKILL.md, KA@2c60614:skills/karpathy-guidelines/SKILL.md, GS@1bd2330:ETHOS.md
---

# Using wraith

wraith is a plugin of skills and agents for data and infrastructure work on GCP.
If there is even a small chance a wraith skill applies, invoke it before responding; loading an unneeded skill is cheap, skipping a needed one costs a redo.

## Instruction priority

The user's direct requests first, then the project's AGENTS.md and CLAUDE.md, then wraith skills, then defaults.

## House rules

- Think before coding: state assumptions, ask when something is unclear, name tradeoffs, and push back when a simpler path exists.
- Simplicity first: write the minimum that solves the problem, with no speculative features or abstractions.
- Surgical changes: touch only what the task needs, match the existing style, and clean up only your own mess.
- Goal-driven: turn each task into a check you can run, and loop until it passes.
- Automate the guardrails, not the work: hooks, tests and lint are the gate; never use `--no-verify`.
- Fail loud, not silent.
- Rigor is proportional to consequence and reuse.
- AI recommends, the user decides: production changes, pushes, deletes and spending need the user's explicit go-ahead in this conversation.
- Anything that touches state outside the process will one day run twice, so make it idempotent.
- A number without its mechanism is a rumour: say how every number was measured.
- Evidence before claims: run the check and quote its output before saying done (wraith:verification-before-completion).
- Project specifics come from the `## wraith` block in the project's AGENTS.md. Never guess a command, project, region or target; if the block is missing, ask once and suggest wraith:setup.
- Read the project's knowledge files and GLOSSARY.md before non-trivial work when they exist, and record new lessons with wraith:knowledge-base.

## The sprint

| Phase | Skill | Artifact |
|---|---|---|
| Think | wraith:brainstorming | `docs/wraith/<date>-<topic>/design.md` |
| Plan | wraith:writing-plans | `plan.md` in the same folder |
| Plan | wraith:plan-data-review | appends `## Data review` to plan.md |
| Plan | wraith:plan-infra-review | appends `## Infra review` to plan.md |
| Plan | wraith:grilling | nothing (conversation) |
| Build | wraith:orchestrating-agents | commits, `progress.md` |
| Build | wraith:tdd, wraith:systematic-debugging, wraith:verification-before-completion | tests, evidence |
| Build | wraith:odcs-contracts, wraith:dbt-bigquery, wraith:bigquery, wraith:cloud-run, wraith:terraform-gcp, wraith:ontology-modeling, wraith:context-layer | domain files |
| Review | wraith:review | `review.md` |
| Review | wraith:security-audit | `security.md` |
| Test | wraith:qa | `qa.md` (evidence) |
| Ship | wraith:ship | changelog, version bump, PR body |
| Ship | wraith:deploy | `deploy.md` |
| Reflect | wraith:handoff | `handoff.md` |
| Reflect | wraith:knowledge-base | knowledge files, GLOSSARY.md, ADRs |
| Safety | wraith:careful | nothing (conversation) |
| Meta | wraith:using-wraith, wraith:setup, wraith:writing-skills | AGENTS.md `## wraith` block (setup) |

## Which skill

- Building or changing a pipeline, model, contract, service or infrastructure: wraith:brainstorming, then wraith:writing-plans.
- A plan touches data: wraith:plan-data-review. A plan touches GCP infrastructure: wraith:plan-infra-review. Stress-testing any plan: wraith:grilling.
- Executing a plan, or running two or more independent tasks: wraith:orchestrating-agents.
- Writing code: wraith:tdd. Something failed: wraith:systematic-debugging. About to say done: wraith:verification-before-completion.
- Data contracts: wraith:odcs-contracts. dbt models: wraith:dbt-bigquery. BigQuery cost, access or erasure: wraith:bigquery. Cloud Run: wraith:cloud-run. Terraform: wraith:terraform-gcp.
- Generic dbt, BigQuery, Cloud Run and Terraform mechanics: the vendor companion skills (dbt Labs, Google, HashiCorp) when installed. On conflict, the wraith skill's rules win.
- What business entities mean: wraith:ontology-modeling. Making the warehouse usable by AI agents: wraith:context-layer.
- A diff or PR: wraith:review. IAM, secrets, ingress or personal data: wraith:security-audit. Proving a change: wraith:qa. Integrating: wraith:ship. Production rollout: wraith:deploy.
- Ending a session or heavy context: wraith:handoff. A lesson learned: wraith:knowledge-base.
- Production work today: wraith:careful. A new repository: wraith:setup. Writing skills or agents: wraith:writing-skills.

## Agents

| Agent | Model | Dispatch when |
|---|---|---|
| wraith:architect | opus | Designing or planning non-trivial work before code exists; read-only. |
| wraith:implementer | sonnet | Executing exactly one plan card, with one commit. |
| wraith:reviewer | sonnet | Reviewing one card's or phase's diff against a fixed checklist. |
| wraith:tester | sonnet | Writing or strengthening behaviour-level tests. |
| wraith:junior-dev | haiku | Mechanical edits with no judgement. |
| wraith:data-engineer | sonnet | dbt on BigQuery, ODCS contracts, pipelines, backfills and data quality. |
| wraith:platform-engineer | sonnet | Terraform, Cloud Run, IAM, Workload Identity Federation and CI/CD. |
| wraith:sre | sonnet | Observability, alerts, SLOs, incident triage and post-deploy watches. |
| wraith:security-engineer | sonnet | Security and privacy review of GCP and data work. |
| wraith:ontologist | sonnet | Ontology and context-layer work. |
| wraith:docs-writer | haiku | READMEs, MkDocs pages, docstrings, ADRs and CLI help. |
| wraith:git-workflow-master | haiku | Branches, worktrees, commit messages, rebases and pre-commit failures. |

## Safety

- Before destructive data and infra commands (Terraform destroy, gcloud deletes, bq rm, DROP or TRUNCATE, dbt full refresh or prod target, force push), follow wraith:careful: stop and get approval for that exact command.
- This is an instruction, not a security boundary.

## Host tools

- [Claude Code tools](references/claude-code-tools.md)
- [Copilot CLI tools](references/copilot-tools.md)
