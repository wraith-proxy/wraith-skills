# wraith reference

Back to the [README](../README.md).

## The sprint

| Phase | Skill | Writes (in your project) | Hands to |
|---|---|---|---|
| Think | `brainstorming` | `docs/wraith/<date>-<topic>/design.md` | `writing-plans` |
| Plan | `writing-plans` | `.../plan.md` | `plan-data-review`, `plan-infra-review` |
| Plan | `plan-data-review` | appends `## Data review` to plan.md | `orchestrating-agents` |
| Plan | `plan-infra-review` | appends `## Infra review` to plan.md | `orchestrating-agents` |
| Plan | `grilling` | nothing (conversation) | any |
| Build | `orchestrating-agents` | commits, `.../progress.md` | `review` |
| Build | `tdd`, `systematic-debugging`, `verification-before-completion` | tests, evidence | |
| Build | `odcs-contracts`, `dbt-bigquery`, `bigquery`, `cloud-run`, `terraform-gcp`, `ontology-modeling`, `context-layer` | domain files | |
| Review | `review` | `.../review.md` | `qa` |
| Review | `security-audit` | `.../security.md` | `qa` |
| Test | `qa` | `.../qa.md` (evidence) | `ship` |
| Ship | `ship` | changelog, version bump, PR body | `deploy` |
| Ship | `deploy` | `.../deploy.md` | `handoff` |
| Reflect | `handoff` | `.../handoff.md` | |
| Reflect | `knowledge-base` | knowledge files, GLOSSARY.md, ADRs | |
| Safety | `careful` | `.wraith/guard-mode` (Copilot CLI) | |
| Meta | `using-wraith`, `setup`, `writing-skills`, `wizard` | AGENTS.md `## wraith` block (setup) | |

Sprint artifacts go to `docs/wraith/<YYYY-MM-DD>-<topic>/` by default.

## Skills

| Name | Phase | Purpose |
|---|---|---|
| using-wraith | Meta | Routes work to the right wraith skill and states house rules |
| brainstorming | Think | Turns a request into an approved design doc |
| writing-plans | Plan | Writes phased plans of model-tagged cards agents can execute |
| grilling | Plan | Stress-tests a plan, decision or idea with relentless questions |
| plan-data-review | Plan | Reviews data plans for grain, contracts, cost, personal data, rollback |
| plan-infra-review | Plan | Reviews GCP infrastructure plans for identity, ingress, rollback, blast radius |
| orchestrating-agents | Build | Runs a plan's cards through fresh subagents with checked results |
| tdd | Build | Test-first Python, SQL and dbt with behaviour-level tests |
| systematic-debugging | Build | Finds the root cause through a fast reproduction loop |
| verification-before-completion | Build | Requires quoted verification output before claiming work is done |
| odcs-contracts | Build | Writes and validates ODCS v3.2.0 data contracts |
| dbt-bigquery | Build | Builds, tests and runs dbt models on BigQuery safely |
| bigquery | Build | BigQuery cost, performance, access control and personal-data handling |
| cloud-run | Build | Builds, deploys and operates Cloud Run services and jobs |
| terraform-gcp | Build | Writes and applies GCP Terraform with a safe plan workflow |
| ontology-modeling | Build | Models business entities and relations in a YAML source of truth |
| context-layer | Build | Prepares warehouses for AI agents and text-to-SQL |
| review | Review | Reviews diffs against repository standards and the plan |
| security-audit | Review | Audits IAM, secrets, ingress and personal data, with evidence |
| qa | Test | Proves a data or infrastructure change against a dev target |
| ship | Ship | Runs final checks, writes the PR body, integrates your chosen route |
| deploy | Ship | Rolls out to production with traffic splits and a rollback plan |
| handoff | Reflect | Narrates decisions and writes a handover doc for a fresh session |
| knowledge-base | Reflect | Records quirks, conventions and decisions so they survive the session |
| careful | Safety | Stops to confirm destructive commands; sets the Copilot CLI guard mode |
| setup | Meta | Records project commands and targets in an AGENTS.md wraith block |
| writing-skills | Meta | Creates and edits skills, agents, AGENTS.md and CLAUDE.md |
| wizard | Meta | Generates interactive bash wizards for steps only humans can do |

## Agents

| Name | Model | Use for |
|---|---|---|
| architect | opus | Designing and planning non-trivial work; read-only, never writes code |
| implementer | sonnet | Executing exactly one plan card with one commit |
| reviewer | sonnet | Reviewing one card or phase against a fixed checklist |
| tester | sonnet | Writing behaviour-level pytest, dbt unit and data tests |
| junior-dev | haiku | Mechanical edits: formatting, renames, regenerating files, lint fixes |
| data-engineer | sonnet | dbt on BigQuery, ODCS contracts, pipelines, backfills, data quality |
| platform-engineer | sonnet | Terraform, Cloud Run, IAM, Workload Identity Federation, CI/CD |
| sre | sonnet | Observability, alerts, SLOs, incident triage, runbooks, post-mortems |
| security-engineer | sonnet | Security and privacy review of GCP and data work |
| ontologist | sonnet | Ontology and context-layer work, question-to-SQL pairs |
| docs-writer | haiku | READMEs, MkDocs pages, docstrings, ADRs and CLI help |
| git-workflow-master | haiku | Git hygiene: branches, worktrees, commit messages, rebases |

## Companions

wraith does not copy vendor skills. It names them, and you install them from
the vendors. Install only what you need.

### dbt Labs

Claude Code:

```bash
claude plugin marketplace add dbt-labs/dbt-agent-skills
claude plugin install dbt@dbt-agent-marketplace
```

Copilot CLI:

```bash
copilot plugin marketplace add dbt-labs/dbt-agent-skills
copilot plugin install dbt@dbt-agent-marketplace
```

wraith recommends `running-dbt-commands`, `using-dbt-for-analytics-engineering`,
`adding-dbt-unit-test`, `maintaining-dbt-documentation`,
`building-dbt-semantic-layer`, `creating-mermaid-dbt-dag` and
`working-with-dbt-mesh`.

### Google

Claude Code, as a plugin (this holds only `bigquery-ai-ml` and a BigQuery MCP
server):

```bash
claude plugin marketplace add google/skills
claude plugin install bigquery@google-plugins
```

Claude Code and Copilot CLI, individual skills (the other BigQuery and Cloud
Run skills live outside any plugin; this needs Node 22.20.0 or later):

```bash
npx skills add google/skills --skill cloud-run-basics -a claude-code -y
npx skills add google/skills --skill bigquery-basics -a github-copilot -y
```

wraith recommends, each with a caveat, `bigquery-basics`,
`bigquery-optimization`, `bigquery-troubleshooting`, `bigquery-observability`,
`cloud-run-basics`, `cloud-build-basics`, `cloud-run-alert-configuration`,
`google-cloud-waf-security`, `google-cloud-waf-reliability`,
`google-cloud-waf-cost-optimization`, `iam-helper-for-policy-simulator` and
`gcloud`. The full list is in docs/adr/0003-companion-google.md.

### HashiCorp

Claude Code:

```bash
claude plugin marketplace add hashicorp/agent-skills
claude plugin install terraform@hashicorp
```

Copilot CLI:

```bash
copilot plugin marketplace add hashicorp/agent-skills
copilot plugin install terraform@hashicorp
```

wraith recommends `terraform-style-guide`, `terraform-test`, `refactor-module`
and `terraform-search-import`.

### Notes on companions

- Vendor skills run with your agent's full permissions. Skim each SKILL.md before installing, especially anything that can run `terraform apply` or touch production.
- `npx skills` may install into `.agents/skills/`, which Claude Code may not read. Check where the files landed. Copilot reads `.github/skills/`, `.claude/skills/` and `.agents/skills/`.
- Google marks its skills as under active development. Keep them away from production without a plan review (wraith:plan-infra-review).
- wraith reviewed these companions at the refs recorded in docs/adr/0002 to 0004. Newer versions have not been reviewed by this project.
- When a skill wraith names changes upstream, the nightly sync opens a `re-vet` issue and the bot drafts a pull request with the pin bump, the diff, an automated scan and a machine read by a model with no tools. Nothing merges it automatically: the maintainer's merge is the review.
- MCP servers (dbt, Google) are set up per project with the vendors' own skills.
