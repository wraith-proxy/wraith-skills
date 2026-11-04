# wraith

wraith is a plugin of skills and agents for data and infrastructure
engineering on GCP: dbt, BigQuery, Cloud Run, Terraform, ODCS data contracts
and ontologies. It is for engineers who want an agent to follow a disciplined
plan, build, review, ship sprint rather than improvise. It works in both
Claude Code and GitHub Copilot from one repository.

## Install

One repository installs into both Claude Code and GitHub Copilot.

Claude Code or GitHub Copilot CLI, inside a session:

Register the marketplace:

```text
/plugin marketplace add wraith-proxy/wraith-skills
```

Install the plugin from this marketplace:

```text
/plugin install wraith@wraith-proxy
```

Or from a terminal:

```bash
claude plugin marketplace add wraith-proxy/wraith-skills
claude plugin install wraith@wraith-proxy

copilot plugin marketplace add wraith-proxy/wraith-skills
copilot plugin install wraith@wraith-proxy
```

In Claude Code, skills appear as `/wraith:<skill>` and agents as
`wraith:<agent>`.

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
| Safety | `careful` | `.wraith/guard-mode` | |
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
| careful | Safety | Sets the destructive-command guard to ask, deny or off |
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
- MCP servers (dbt, Google) are set up per project with the vendors' own skills.

## What wraith runs, sends and stores

wraith runs two local Python hooks. At session start it adds the wraith router text to the conversation. Before shell commands it checks the command against a list of destructive patterns and asks you, or blocks, depending on the guard mode. In Claude Code the guard also checks MCP tool calls, reading their arguments as JSON; the Copilot CLI guard checks only `bash` and `powershell` commands.

The guard checks the pending command text locally and discards it. It stores nothing. wraith sends nothing, fetches nothing, collects no telemetry and checks for no updates.

To choose its mode and extra patterns the guard reads the `WRAITH_GUARD` environment variable, and `.wraith/guard-mode` and `.wraith/guard-patterns.txt` in your project if they exist.

Skills may suggest commands that download packages (for example `uvx check-jsonschema`); the agent runs them in the open.

See [PRIVACY.md](PRIVACY.md) for the full statement.

## Requirements

`python3` 3.9 or later on PATH for the hooks. Without it, Claude Code shows a
hook error and carries on, and Copilot carries on because each hook ends with
`|| true`.

## Safety

The guard has three modes. `ask` is the default and prompts before a
destructive command. `deny` blocks it. `off` disables the guard. The
`wraith:careful` skill sets the mode for your project and explains what the
guard catches. The guard is best-effort string matching, not a security boundary.
Anything that changes production, pushes, deletes or spends beyond your dev
cost cap still needs your explicit go-ahead in the conversation.

## Uninstall

```bash
claude plugin uninstall wraith@wraith-proxy
copilot plugin uninstall wraith
```

## Credits

wraith builds on MIT-licensed work. Full notices are in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

- [obra/superpowers](https://github.com/obra/superpowers)
- [mattpocock/skills](https://github.com/mattpocock/skills)
- [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
- [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)
- [garrytan/gstack](https://github.com/garrytan/gstack)

## Contributing

Read [AGENTS.md](AGENTS.md) first. Commits use the format
`👻 <type>/WSK-<5 digits>: <summary>`, where the type is `feature`, `fix`,
`bug` or `break` (these four cut a release) or `docs`, `chore`, `ci`, `test`
or `refactor` (no release), and the ticket is the zero-padded GitHub issue
number. Report problems and propose changes as issues on GitHub.

---

[Privacy](PRIVACY.md) | [Terms](TERMS.md) | [Support](SUPPORT.md) | [Security](SECURITY.md)
