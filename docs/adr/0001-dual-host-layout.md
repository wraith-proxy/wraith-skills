# ADR 0001: dual-host layout

Status: proposed (Gate 0). Date: 2026-11-02. Ticket: WSK-00001.

## Context

PLAN.md section 2.11 puts one plugin in one repository for two hosts: Claude
Code reads `.claude-plugin/`, `agents/` and `hooks/`; Copilot reads a root
Agent Plugins 1.0 `plugin.json` and `com.github.copilot/`. Phase 0 built the
smallest such plugin (one skill, one agent, one hook script answering four
modes) and ran checks C1 to C10 against it before any content exists.

Environment: Claude Code 2.1.316, GitHub Copilot CLI 1.0.105 (default model
chosen by Copilot Fusion: gpt-6-luna), Node 22.23.4, Python 3.12.3,
uv 0.10.12, git 2.43.0.

Headless runs used `claude -p` and `copilot -p` in scratch projects; menu and
prompt checks (C3 a and c, C7) used an interactive Copilot session. Every
install was removed afterwards.

## Checks

| Check | Result |
|---|---|
| C1 validate | pass, after one manifest fix |
| C2 Claude Code | pass (a, b, c, d) |
| C3 Copilot CLI | pass (a to e); root variable `${PLUGIN_ROOT}` |
| C4 marketplaces | pass on both hosts |
| C5 AGENTS.md import | pass |
| C6 evals | pass |
| C7 Copilot ask | Copilot prompts the user |
| C8 Copilot agent `model` | loads with a warning, falls back to auto |
| C9 pins | pass; ODCS pin moved to v3.2.0 |
| C10 companions | pass on both hosts |

### C1 `claude plugin validate --strict .`

With the spike manifests exactly as PLAN.md 0.3 gives them:

```text
⚠ Found 1 warning:
  ❯ description: No marketplace description provided. Adding a description helps users understand what this marketplace offers
✘ Validation failed (--strict treats warnings as errors)
```

No warning names the root `plugin.json` or `com.github.copilot/`. Adding a
top-level `"description"` to `.claude-plugin/marketplace.json` clears it:

```text
✔ Validation passed
```

Two non-verdict notices remain and do not fail `--strict`:

- Plugin directory warning `ICON_MISSING` ("These plugin directory checks do
  not change the result below").
- Advice: the README has no marketplace install line
  (`/plugin install wraith --marketplace wraith-proxy/wraith-skills`, Claude
  Code 2.1.275+).

### C2 Claude Code (`claude -p --plugin-dir <repo>`, stream-json init event)

- (a) `slash_commands` and `skills` contain `wraith:using-wraith`.
- (b) "What does the wraith router say?" answered `PINEAPPLE` with no tool
  call: "It came from the session-start hook output (`wraith router:
  PINEAPPLE`). I used no tools."
- (c) `agents` contains `wraith:reviewer`.
- (d) With Bash pre-allowed, `terraform destroy -auto-approve` returned
  `PreToolUse:Bash hook error: wraith spike: terraform destroy blocked`; the
  command did not run.
- Hook environment: `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` are set; the
  hook cwd is the session's project directory, not the plugin root.
- PreToolUse stdin keys (snake_case): `cwd`, `effort`, `hook_event_name`,
  `permission_mode`, `prompt_id`, `session_id`, `tool_input`, `tool_name`,
  `tool_use_id`, `transcript_path`. SessionStart also sets `CLAUDE_ENV_FILE`.

### C3 Copilot CLI

`copilot plugin install <repo>` printed `Plugin "wraith" installed
successfully. Installed 1 skill.` plus `Warning: Direct plugin installs
(repos, URLs, local paths) are deprecated. Only plugin@marketplace installs
will be supported in a future release.` `copilot plugin list` showed
`wraith (v0.0.1)`. A direct local install copies the whole directory,
gitignored files included.

- (a) `/skills` lists `using-wraith`, "Plugin-contributed".
- (b) With the skill tool excluded (`--excluded-tools skill`), "What does the
  wraith router say?" answered `PINEAPPLE` with no tool call. Without that
  flag the model calls the `using-wraith` skill first, so the exclusion is
  what proves injection.
- (c) `/agent` lists `reviewer · plugin`. On the command line the name is
  namespaced: `--agent reviewer` gives `No such agent: reviewer, available:
  wraith:reviewer`; `--agent wraith:reviewer` replies `MANGO`. Copilot reads
  `com.github.copilot/agents/reviewer.agent.md`, not `agents/reviewer.md`
  (changing only the Copilot file's word changed the reply).
- (d) `terraform destroy -auto-approve` (shell tool `bash`, granted only as
  `shell(terraform:*)`): `Denied by preToolUse hook: wraith spike: terraform
  destroy blocked`.
- (e) `${PLUGIN_ROOT}` expanded on the first try. Hook cwd is the plugin root.
  Hook environment also carries `COPILOT_PLUGIN_ROOT`, `COPILOT_HOOK_DIR`,
  `COPILOT_PLUGIN_DATA`, `COPILOT_PROJECT_DIR` and, for compatibility,
  `CLAUDE_PLUGIN_ROOT`, `CLAUDE_PLUGIN_DATA`, `CLAUDE_PROJECT_DIR` (not
  inherited: absent from the parent shell). `preToolUse` stdin keys are
  camelCase: `cwd`, `sessionId`, `timestamp`, `toolArgs` (a JSON object, not
  a string), `toolName`. `sessionStart` stdin was empty. `preToolUse` also
  fires for the `skill` tool.

### C4 marketplaces

- Claude: `claude plugin marketplace add --scope local <repo>` printed
  `✔ Successfully added marketplace: wraith-proxy`; `claude plugin install
  --scope local wraith@wraith-proxy` printed `✔ Successfully installed
  plugin: wraith@wraith-proxy (scope: local)`.
- Copilot: `copilot plugin marketplace add <repo>` printed `Marketplace
  "wraith-proxy" added successfully.`; `copilot plugin install
  wraith@wraith-proxy` printed `Plugin "wraith" installed successfully.
  Installed 1 skill.` and `It is loaded live from <repo>, so edits take effect
  on the next session - nothing was copied.`

### C5 AGENTS.md through `.claude/CLAUDE.md`

C1 still passes with `AGENTS.md` and `.claude/CLAUDE.md` (`@../AGENTS.md`).
A session in the repo answered the AGENTS.md marker word. Control run with
`.claude/CLAUDE.md` removed: "NOT IN CONTEXT". The import is required; Claude
Code does not load `AGENTS.md` on its own here.

### C6 evals

`claude plugin eval init --bare smoke` created `evals/smoke/prompt.md` and
`evals/smoke/graders/criteria.md` (an `llm` grader). A grader with
frontmatter `type: regex`, `pattern: PINEAPPLE` works:

```text
✓ pineapple (weight 1): matched PINEAPPLE
smoke  1.00  100%  1    $0.04
```

Exit 0. Evals are available on 2.1.316 without early access. Reports go to
`evals/results/` (gitignored).

### C7 Copilot `ask`

With the Copilot guard answering `{"permissionDecision": "ask"}`, the
interactive session showed `Do you want to allow this tool call?` with
`1. Yes` and `2. No (Esc to stop)`. The session was ended without answering.

### C8 Copilot agent `model`

With `model: sonnet` in `com.github.copilot/agents/reviewer.agent.md` the
agent loads and replies `MANGO`, after `Warning: Custom agent
"wraith:reviewer" specifies model "sonnet" which is not available; using
"auto" instead`.

### C9 pins

- (a) ODCS v3.2.0 was released 2026-09-08, so the pin moved from v3.1.0
  (PLAN.md 1.3 and Card 3A updated). Schema:
  `https://raw.githubusercontent.com/bitol-io/open-data-contract-standard/v3.2.0/schema/odcs-json-schema-v3.2.0.json`
  (HTTP 200 at tag `v3.2.0`, `f0bdad9`). Official example:
  `docs/examples/all/full-example.odcs.yaml` (`apiVersion: v3.2.0` at that
  tag). The schema's `apiVersion` enum still accepts v3.1.0 and v3.0.x.
- (b) `hashicorp/google` 8.9.0 (2026-10-27): major version 8.
- (c) `datacontract-cli` 1.2.9 (2026-10-30, Python >=3.10,<3.15). Supports
  ODCS 3.2.0 (lints the v3.2.0 server types and stable ids "as in the
  released ODCS v3.2.0 schema") and 3.1.0.
- (d) `check-jsonschema` 0.39.0 (2026-10-26).
- (e) `@anthropic-ai/claude-code` 2.1.316; `@github/copilot` 1.0.105.
- (f) All five vendored upstreams check out at their table 1.1 SHAs; the tags
  match (SP `v7.0.1`, MP `v1.3.2`, GS `v1.91.318.0`). Every cited source in
  Phases 2 to 4 exists: 59 `<KEY>[@sha7]:<path>` citations (all sha7 values
  match the pins), the 13 AA agent files of section 2.8, MP
  `SKILL-MECHANICS.md`, `ADR-FORMAT.md`, `GLOSSARY-FORMAT.md`, SP
  `code-reviewer.md` and the seven SP subagent-driven-development
  `references/*.md`. No fallback commit needed; table 1.1 is unchanged.

### C10 companions

| Companion | Host | Command that worked | Lands in |
|---|---|---|---|
| DBT | Claude Code | `claude plugin marketplace add dbt-labs/dbt-agent-skills`, `claude plugin install dbt@dbt-agent-marketplace` | plugin cache, `dbt` 1.6.0, 12 skills |
| DBT | Copilot | `copilot plugin marketplace add dbt-labs/dbt-agent-skills`, `copilot plugin install dbt@dbt-agent-marketplace` | `~/.copilot/installed-plugins/dbt-agent-marketplace/`, 12 skills |
| TF | Claude Code | `claude plugin marketplace add hashicorp/agent-skills`, `claude plugin install terraform@hashicorp` | plugin cache, `terraform` 1.0.0, 16 skills |
| TF | Copilot | `copilot plugin marketplace add hashicorp/agent-skills`, `copilot plugin install terraform@hashicorp` | `~/.copilot/installed-plugins/hashicorp/`, 16 skills |
| GCP | Claude Code | `claude plugin marketplace add google/skills` (name `google-plugins`), `claude plugin install bigquery@google-plugins` | plugin cache, `bigquery` 0.2.5 |
| GCP | Claude Code | `npx skills add google/skills --skill cloud-run-basics -a claude-code -y` | project `.claude/skills/cloud-run-basics/` |
| GCP | Copilot | `npx skills add google/skills --skill bigquery-basics -a github-copilot -y` | project `.agents/skills/bigquery-basics/` |

- The Google `bigquery` plugin holds only the `bigquery-ai-ml` skill plus a
  BigQuery MCP server, and asks for two userConfig values (`bigquery_project`,
  `bigquery_location`). `bigquery-basics`, `-optimization`,
  `-troubleshooting`, `-observability`, `cloud-run-basics` and
  `cloud-build-basics` live under `skills/cloud/` in `google/skills`, outside
  any plugin, so they come from `npx skills`.
- `npx skills` (npm `skills` 1.7.4, vercel-labs) needs Node >=22.20.0 (on
  Node 18 it crashes at module load). It also writes `skills-lock.json` to
  the project root, has install telemetry (its `--help` documents an
  install telemetry event), and ends with "Review skills
  before use; they run with full agent permissions." `copilot skill list`
  showed both skills as project skills.

## Decisions

- **Copilot plugin-root variable:** `${PLUGIN_ROOT}`, double-quoted. Hook cwd
  is also the plugin root on Copilot (not on Claude Code).
- **CI validate mode:** `claude plugin validate --strict .` with no recorded
  exceptions. The marketplace manifest carries a top-level `description`
  (Card 1A).
- **ask versus deny on Copilot:** keep `ask`; Copilot prompts. The D7
  fallback (map to `deny`) is not needed.
- **Copilot agent `model`:** the generator strips it (as planned); Claude
  model names are not Copilot models.
- **Copilot agent names** are namespaced `wraith:<name>`, as in Claude Code.
- **Evals:** available locally on Claude Code 2.1.316. Regex graders use
  `type: regex` and `pattern:`.
- **Pins:** ODCS v3.2.0 schema and example above; `hashicorp/google` major 8;
  `datacontract-cli` 1.2.9; `check-jsonschema` 0.39.0; Claude Code 2.1.316;
  Copilot CLI 1.0.105.
- **Companion install commands:** the C10 table, for the README Companions
  section.

## Consequences

- The 2.11 layout holds on both hosts.
- Card 5A parses two payload shapes: Claude `tool_name` / `tool_input`
  (snake_case), Copilot `toolName` / `toolArgs` (camelCase, object), with
  shell tool `Bash` on Claude and `bash` on Copilot. Copilot's `preToolUse`
  also fires for non-shell tools such as `skill`.
- Copilot skill tool use is eager: an injected router does not stop the
  model calling `using-wraith` as a skill. Harmless, but evals for Copilot
  should not assume zero skill calls.
- Contributor sessions need `.claude/CLAUDE.md` importing `AGENTS.md`.
- README must recommend marketplace installs; Copilot deprecates direct
  installs.
- Cards 3B, 3C and 3D companion text must say the Google `bigquery` plugin
  brings an MCP server and only the AI/ML skill; the basics skills come from
  `npx skills` (Node 22.20+, writes `skills-lock.json`, has telemetry).
- PLAN.md stays local and is never committed (owner instruction,
  2026-11-02); section 2.11 and step 0.2 are superseded on that point.
