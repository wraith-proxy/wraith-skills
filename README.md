<p align="center">
  <img src="assets/icon.png" width="120" alt="wraith">
</p>

<h1 align="center">wraith</h1>

<p align="center">
  <em>Agents improvise. wraith makes them plan, review and prove it.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/wraith-proxy/wraith-skills?style=flat-square&label=release" alt="Latest release">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT license">
  <img src="https://img.shields.io/badge/works%20with-Claude%20Code%20%2B%20Copilot-blue?style=flat-square" alt="Works with Claude Code and Copilot">
  <img src="https://img.shields.io/github/actions/workflow/status/wraith-proxy/wraith-skills/ci.yml?branch=main&style=flat-square&label=ci" alt="CI status">
</p>

<!-- hero: 3 benchmark numbers land here after Card 3.3 -->

For data and platform engineers on GCP: dbt, BigQuery, Cloud Run, Terraform,
ODCS contracts. Left alone, an agent improvises, and on BigQuery improvisation
is billed by the terabyte.

<!-- demo GIF of the guard lands here after Card 4.1 -->

## Start here

- `careful`: stops the agent running a destructive command on production
  without asking you first.
- `plan-data-review`: checks a data plan for grain, contracts, cost, personal
  data and rollback before anyone builds it.
- `odcs-contracts`: writes and validates the data contract, and keeps your dbt
  models in step with it.
- `orchestrating-agents`: runs a written plan one card at a time through fresh
  subagents, and checks each result.

<!-- before/after image lands here after Card 4.2 -->

## Install

Claude Code or GitHub Copilot CLI, inside a session:

```text
/plugin marketplace add wraith-proxy/wraith-skills
```

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

## Why wraith and not a general skills pack

General packs are good, and wraith stands on them (see Credits). wraith adds
what a GCP data team keeps needing:

- Grain and cost review of data plans before they are built.
- ODCS data contracts as the source of truth for your models.
- Blast-radius review of GCP infrastructure plans.
- A guard that asks before destructive commands.
- One sprint: plan, build, review, ship.

## What wraith runs, sends and stores

wraith runs two local Python hooks. At session start it adds the wraith router
text to the conversation. Before shell commands it checks the command against
a list of destructive patterns and asks you, or blocks, depending on the guard
mode. In Claude Code the guard also checks MCP tool calls, reading their
arguments as JSON; the Copilot CLI guard checks only `bash` and `powershell`
commands.

The guard checks the pending command text locally and discards it. It stores
nothing. wraith sends nothing, fetches nothing, collects no telemetry and
checks for no updates.

To choose its mode and extra patterns the guard reads the `WRAITH_GUARD`
environment variable, and `.wraith/guard-mode` and
`.wraith/guard-patterns.txt` in your project if they exist.

Skills may suggest commands that download packages (for example
`uvx check-jsonschema`); the agent runs them in the open.

See [PRIVACY.md](PRIVACY.md) for the full statement.

## Reference

The full sprint, skills, agents and companions are in
[docs/reference.md](docs/reference.md).

## Companions

wraith does not copy vendor skills. It names them, and you install them from
the vendors (dbt Labs, Google, HashiCorp). Install steps and notes are in
[docs/reference.md](docs/reference.md#companions). Vendor skills run with your
agent's full permissions, so skim each SKILL.md before installing.

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
