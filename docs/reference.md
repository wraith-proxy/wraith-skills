# wraith reference

Back to the [README](../README.md).

## Artifacts

Skills that write files put them under `docs/wraith/<YYYY-MM-DD>-<topic>/` by default (`artifacts_dir` in the wraith block). The plan reviews append `## Data review` or `## Infra review` to the plan, `security-audit` writes `security.md`, `qa` writes `qa.md` and `deploy` writes `deploy.md`.

## Skills

| Name | Area | Purpose |
|---|---|---|
| using-wraith | Meta | Lists the wraith skills and agents and the rules they share |
| setup | Meta | Records project values in an AGENTS.md wraith block |
| plan-data-review | Plan | Reviews data plans for grain, contracts, cost, personal data, rollback |
| plan-infra-review | Plan | Reviews GCP infrastructure plans for identity, ingress, rollback, blast radius |
| odcs-contracts | Build | Writes and validates ODCS v3.2.0 data contracts |
| dbt-bigquery | Build | Builds, tests and runs dbt models on BigQuery safely |
| bigquery | Build | BigQuery cost, performance, access control and personal-data handling |
| cloud-run | Build | Builds, deploys and operates Cloud Run services and jobs |
| terraform-gcp | Build | Writes and applies GCP Terraform with a safe plan workflow |
| ontology-modeling | Build | Models business entities and relations in a YAML source of truth |
| context-layer | Build | Prepares warehouses for AI agents and text-to-SQL |
| security-audit | Review | Audits IAM, secrets, ingress and personal data, with evidence |
| qa | Test | Proves a data or infrastructure change against a dev target |
| deploy | Ship | Rolls out to production with traffic splits and a rollback plan |
| careful | Safety | Makes the agent stop and confirm before destructive commands |

## Agents

| Name | Model | Use for |
|---|---|---|
| data-engineer | sonnet | dbt on BigQuery, ODCS contracts, pipelines, backfills, data quality |
| platform-engineer | sonnet | Terraform, Cloud Run, IAM, Workload Identity Federation, CI/CD |
| sre | sonnet | Observability, alerts, SLOs, incident triage, runbooks, post-mortems |
| security-engineer | sonnet | Security and privacy review of GCP and data work |
| ontologist | sonnet | Ontology and context-layer work, question-to-SQL pairs |

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

### Superpowers (general workflow)

obra/superpowers covers designs, plans, plan execution, test-first work, debugging, verification, code review and finishing a branch. It installs a SessionStart hook of its own.

Claude Code:

```bash
claude plugin install superpowers@claude-plugins-official
```

Copilot CLI:

```bash
copilot plugin marketplace add obra/superpowers-marketplace
copilot plugin install superpowers@superpowers-marketplace
```

wraith recommends `brainstorming`, `writing-plans`, `executing-plans`,
`subagent-driven-development`, `dispatching-parallel-agents`,
`using-git-worktrees`, `test-driven-development`, `systematic-debugging`,
`verification-before-completion`, `requesting-code-review`,
`receiving-code-review`, `finishing-a-development-branch` and
`writing-skills`. Run wraith:plan-data-review or wraith:plan-infra-review on
the plan that `writing-plans` writes before building it.

### Matt Pocock (general workflow)

mattpocock/skills covers test-first work, debugging, grilling, handoffs, domain modeling, code review and PR bodies.

Claude Code:

```bash
claude plugin install mattpocock-skills@claude-plugins-official
```

Copilot CLI:

```bash
copilot plugin marketplace add mattpocock/skills
copilot plugin install mattpocock-skills@mattpocock
```

wraith recommends `tdd`, `diagnosing-bugs`, `grilling`, `handoff`,
`domain-modeling`, `code-review`, `setup-matt-pocock-skills`, `pr` and
`writing-for-agents`. The plugin also installs `wizard`, which wraith does
not recommend because it writes captured secrets to `.env` and GitHub.

### Notes on companions

- Vendor skills run with your agent's full permissions. Skim each SKILL.md before installing, especially anything that can run `terraform apply` or touch production.
- `npx skills` may install into `.agents/skills/`, which Claude Code may not read. Check where the files landed. Copilot reads `.github/skills/`, `.claude/skills/` and `.agents/skills/`.
- Google marks its skills as under active development. Keep them away from production without a plan review (wraith:plan-infra-review).
- wraith reviewed these companions at the refs recorded in docs/adr/0002 to 0004 and 0006. Newer versions have not been reviewed by this project.
- When a skill wraith names changes upstream, the nightly sync opens a `re-vet` issue and the bot drafts a pull request with the pin bump, the diff and an automated scan. Nothing merges it automatically: the maintainer's merge is the review.
- MCP servers (dbt, Google) are set up per project with the vendors' own skills.
