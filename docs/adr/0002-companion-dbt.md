# ADR 0002: dbt companion

Status: proposed (Gate 3). Date: 2026-11-02. Ticket: WSK-00004.

## Context

wraith points to the dbt Labs agent skills as a companion and never copies
them (G21). This ADR vets that companion before any wraith skill names it.

- Repository: https://github.com/dbt-labs/dbt-agent-skills
- Ref reviewed: `main`, SHA `b8facde20b7a92c40ce3e6b86b71c4b92aa44040`
- License: Apache-2.0
- Reviewed: 2026-11-02
- Scope: every `SKILL.md` at that SHA, 16 in all: 12 under
  `skills/dbt/skills/`, 1 under `skills/dbt-extras/skills/` and 3 under
  `skills/dbt-migration/skills/`.

Quotes below are single sentences or single commands, kept short to show a
risk or a conflict. Em dashes in quoted text are replaced per G8.

## Review

Section 2.6 stances are cited by their first words. "Commands" lists the
`allowed-tools` frontmatter where a skill sets it, otherwise the commands
the body tells the agent to run.

| Skill | Purpose | Use for | Commands it may run | Risky instructions (quoted) | Conflicts with 2.6 (quoted) | Verdict |
|---|---|---|---|---|---|---|
| `skills/dbt/skills/adding-dbt-unit-test/SKILL.md` | Write dbt unit test YAML that mocks inputs and checks outputs. | Test-first work on a dbt model, beside `wraith:tdd`. | `dbt build --select`, `dbt run --empty` | none | none | recommend |
| `skills/dbt/skills/answering-natural-language-questions-with-dbt/SKILL.md` | Answer business questions with Semantic Layer or ad-hoc SQL. | Read-only metric questions when a dbt MCP server is already configured. | MCP `query_metrics`, `execute_sql`; reads `target/manifest.json` | "`get_metrics_compiled_sql`, then `execute_sql`" (runs SQL on the warehouse) | "Define once, consume many": modifying compiled metric SQL on the fly defines a metric outside its model. | recommend with caveat |
| `skills/dbt/skills/building-dbt-semantic-layer/SKILL.md` | Create semantic models, metrics, entities and time spines. | Defining a metric once in the model layer. | MetricFlow validation, `uvx dbt-autofix deprecations --semantic-layer` | "`uvx dbt-autofix deprecations --semantic-layer`" (downloads and edits project files) | none | recommend with caveat |
| `skills/dbt/skills/configuring-dbt-mcp-server/SKILL.md` | Generate dbt MCP server config and auth. | Nothing: needs dbt platform tokens and a hosted endpoint. | `uvx dbt-mcp` (written into config) | It writes an MCP server config that starts a downloaded server and needs a dbt platform token. | none | do not recommend |
| `skills/dbt/skills/fetching-dbt-docs/SKILL.md` | Fetch dbt docs pages as LLM-friendly markdown. | Looking up a dbt reference page. | WebFetch of `docs.getdbt.com` | "WebFetch: https://docs.getdbt.com/llms.txt" (network call) | none | recommend with caveat |
| `skills/dbt/skills/maintaining-dbt-documentation/SKILL.md` | Audit doc coverage and draft missing descriptions. | Backfilling model and column descriptions, with review. | `Bash(dbt *)`, `Bash(python3 *)`, `Bash(git *)`, Write, Edit | none | none | recommend with caveat |
| `skills/dbt/skills/querying-the-dbt-information-schema/SKILL.md` | Query dbt v2 project metadata with `dbt show --info`. | Project-rule checks on dbt v2 only. | `dbt show --info`, `dbt check`, `dbt parse --generate-info-schema` | "`dbt build --skip-checks` bypasses them." | none | recommend with caveat |
| `skills/dbt/skills/running-dbt-commands/SKILL.md` | Choose the dbt executable and format CLI commands. | Any dbt command run from a wraith skill. | `dbt build --select`, `dbt show`, `dbt compile` | "`dbt build --select my_model --full-refresh`"; "`dbt build --select my_model --defer --state prod-artifacts`" | "Same input, same output": deferral reads production objects, not the `ds` snapshot. | recommend with caveat |
| `skills/dbt/skills/troubleshooting-dbt-job-errors/SKILL.md` | Diagnose dbt platform job failures from run logs and the Admin API. | Nothing: needs a dbt platform account. | Admin API calls, git history reads | "https://<DBT_ENDPOINT>/api/v2/accounts/<ACCOUNT_ID>/runs/<RUN_ID>/artifacts/run_results.json" (network call with a token) | none | do not recommend |
| `skills/dbt/skills/using-dbt-for-analytics-engineering/SKILL.md` | Build and modify models, tests and checks with `dbt show`. | Everyday dbt model work. | `Bash(dbt *)`, `Bash(jq *)`, Write, Edit | "Use deferral (`--defer --state path/to/prod/artifacts`) to reuse production objects" | "Same input, same output": deferral to production objects. | recommend with caveat |
| `skills/dbt/skills/using-dbt-state/SKILL.md` | Configure dbt State, the server-backed build reuse. | Nothing: needs a vendor account and server. | `pip install dbt-state`, `dbt-state explain` | "It calls the dbt State **server** and requires authentication" | "Full rebuild until scan cost is measurably too high": it skips or clones nodes instead of rebuilding them. | do not recommend |
| `skills/dbt/skills/working-with-dbt-mesh/SKILL.md` | Judge breaking changes; model versions, contracts, access, mesh. | Changing a model that consumers depend on. | `dbt`, YAML edits | "Do not set up cross-project refs if you cannot confirm the plan level is Enterprise or higher." | none | recommend with caveat |
| `skills/dbt-extras/skills/creating-mermaid-dbt-dag/SKILL.md` | Draw dbt model lineage as a Mermaid flowchart. | Documenting lineage in markdown. | `mcp__dbt__get_lineage_dev`, `mcp__dbt__get_lineage`, `Bash(jq *)` | none | none | recommend |
| `skills/dbt-migration/skills/migrating-dbt-core-to-v2/SKILL.md` | Triage dbt-core to dbt v2 migration errors. | Nothing: a one-off Fusion migration, outside wraith scope. | `Bash(dbt:*)`, `Bash(git:*)`, `Bash(uvx:*)`, WebFetch `api.github.com` | "`uvx --from git+https://github.com/dbt-labs/dbt-autofix.git dbt-autofix deprecations`" | none | do not recommend |
| `skills/dbt-migration/skills/migrating-dbt-project-across-platforms/SKILL.md` | Move a dbt project between warehouses using Fusion. | Nothing: a one-off platform move that requires Fusion. | `dbtf compile`, `rm -rf target/` | "Run `rm -rf target/` before compiling against a new platform." | none | do not recommend |
| `skills/dbt-migration/skills/upgrading-dbt/SKILL.md` | Upgrade a dbt v1 project to 1.12 step by step. | Nothing: a one-off upgrade; 38 KB and reports telemetry. | `Bash(git:*)`, `Bash(dbt:*)`, `Bash(uvx:*)`, `Bash(uv:*)` | "The platform profile also reports migration telemetry before every stop or give-up" | none | do not recommend |

## Decision

- `wraith:dbt-bigquery` may point to `running-dbt-commands`,
  `using-dbt-for-analytics-engineering`, `adding-dbt-unit-test` and
  `maintaining-dbt-documentation`.
- `wraith:tdd` may point to `adding-dbt-unit-test` for dbt model tests.
- `wraith:context-layer` may point to `building-dbt-semantic-layer`,
  `maintaining-dbt-documentation` and `creating-mermaid-dbt-dag`.
- `wraith:odcs-contracts` may point to `working-with-dbt-mesh` for contract
  enforcement, versioning and breaking-change judgment.
- No wraith skill points to a "do not recommend" skill. Migration skills are
  one-off work and are not part of the sprint.

Where a recommended skill disagrees with a wraith rule, the wraith rule wins,
citing section 2.6:

- Deferral to production objects (`--defer --state`) is for CI slim
  builds only (wraith:dbt-bigquery `references/ci.md`). Elsewhere it loses
  to "Datestamp first" and "Same input, same output": a run rewrites one
  `ds` from its `ds` inputs.
- `--full-refresh` is used only under "Full rebuild until scan cost is
  measurably too high", with the threshold stated per model.
- Ad-hoc edits of compiled metric SQL lose to "Define once, consume many":
  the metric changes in its one model.
- A contract is the source of truth: "The contract is the source of truth."
  Skill advice on contracts and versions follows the ODCS file, not the
  dbt YAML.
- "Fail loud, not silent": `dbt build --skip-checks` is never suggested.
- Any command that downloads (`uvx`) or calls the network (WebFetch) is
  named in the wraith skill and runs visibly (G11).

## Install

Copied from the ADR 0001 C10 table.

| Host | Command that worked | Lands in |
|---|---|---|
| Claude Code | `claude plugin marketplace add dbt-labs/dbt-agent-skills`, `claude plugin install dbt@dbt-agent-marketplace` | plugin cache, `dbt` 1.6.0, 12 skills |
| Copilot | `copilot plugin marketplace add dbt-labs/dbt-agent-skills`, `copilot plugin install dbt@dbt-agent-marketplace` | `~/.copilot/installed-plugins/dbt-agent-marketplace/`, 12 skills |

The `dbt` plugin carries only the 12 `skills/dbt/skills/` entries.
`creating-mermaid-dbt-dag` (dbt-extras) and the migration skills belong to
other plugins in the same repository and are not installed by these commands.

## Consequences

- PLAN.md counted 13 skills under `skills/dbt/skills/`; the pinned SHA has
  12, so the review has 16 rows, not 17.
- Two skills are recommended, eight are recommended with a caveat and six
  are not recommended.
- Wraith skills name only the companion skills listed under Decision (G21).
- Skills with a caveat run only when the project has the tool they need (dbt
  v2 for the information schema, a dbt MCP server for natural-language
  questions).
- The companion is optional. Every wraith skill works with the companion
  absent and says so.
- If the pinned ref moves, this ADR is re-run before the pointers change.
