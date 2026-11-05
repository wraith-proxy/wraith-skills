<p align="center">
  <img src="assets/social-preview.png" width="720" alt="wraith. Agents improvise. wraith makes them plan, review and prove it. Skills and agents for dbt, BigQuery, Cloud Run and Terraform on GCP.">
</p>

<p align="center">
  <em>Agents don't hesitate before prod. wraith is the ghost that does.</em>
</p>

<p align="center">
  <a href="https://github.com/wraith-proxy/wraith-skills/stargazers"><img src="https://img.shields.io/github/stars/wraith-proxy/wraith-skills?style=flat-square&amp;label=stars" alt="GitHub stars"></a>
  <a href="https://github.com/wraith-proxy/wraith-skills/releases"><img src="https://img.shields.io/github/v/release/wraith-proxy/wraith-skills?style=flat-square&amp;label=release" alt="Latest release"></a>
  <a href="https://github.com/wraith-proxy/wraith-skills/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/wraith-proxy/wraith-skills/ci.yml?branch=main&amp;style=flat-square&amp;label=ci" alt="CI status"></a>
  <a href="#install"><img src="https://img.shields.io/badge/works%20with-Claude%20Code%20%2B%20Copilot-blue?style=flat-square" alt="Works with Claude Code and Copilot"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT license"></a>
</p>

Every data team has a ghost story. The `DELETE FROM` with no `WHERE`. The
backfill nobody costed. The `terraform apply` that took the network with it.
The engineer who learned those lessons the hard way left years ago.

Your agent never met them. It improvises, and on BigQuery improvisation is
billed by the terabyte.

**wraith is the ghost they left behind.** It reviews the plan before anyone
builds it, writes the data contract before the model, and waits at the door
to prod asking *are you sure?*

<table align="center">
<tr>
<td align="center" width="25%"><h3>+35%</h3>planted problems caught in plan review<br><sub><a href="https://github.com/wraith-proxy/wraith-benchmarks/blob/8db2c97bc72c7a7e57d2ba936120d29b86346a64/benchmarks/results/2026-11-04.md?plain=1#L64-L69">127 vs 94 of 180</a></sub></td>
<td align="center" width="25%"><h3>3 of 3</h3>planted defects found on case p10, against 1 of 3 without<br><sub><a href="https://github.com/wraith-proxy/wraith-benchmarks/blob/8db2c97bc72c7a7e57d2ba936120d29b86346a64/benchmarks/results/2026-11-04.md?plain=1#L57-L58">median run per arm</a></sub></td>
<td align="center" width="25%"><h3>28 + 12</h3>skills and agents for dbt, BigQuery, Cloud Run, Terraform and ODCS<br><sub><a href="docs/reference.md">full list</a></sub></td>
<td align="center" width="25%"><h3>0</h3>calls home. No telemetry, no fetches, no update checks<br><sub><a href="PRIVACY.md">privacy</a></sub></td>
</tr>
</table>

## Install

Claude Code or GitHub Copilot CLI, inside a session:

```text
/plugin marketplace add wraith-proxy/wraith-skills
```

```text
/plugin install wraith@wraith-proxy
```

That's it. The guard starts in `ask` mode and there is nothing to configure.

<details>
<summary>From a terminal instead</summary>

```bash
claude plugin marketplace add wraith-proxy/wraith-skills
claude plugin install wraith@wraith-proxy

copilot plugin marketplace add wraith-proxy/wraith-skills
copilot plugin install wraith@wraith-proxy
```

</details>

In Claude Code, skills appear as `/wraith:<skill>` and agents as
`wraith:<agent>`.

## Proof

<p align="center">
  <img src="assets/numbers.png" width="640" alt="Plan review, planted problems found: with wraith 70.6% (127 of 180), without 52.2% (94 of 180)">
</p>

<p align="center"><sub>12 plan-review cases, 5 runs per arm, 3 planted problems each, judged by majority vote. Whiskers are Wilson 95% intervals. Source: <a href="https://github.com/wraith-proxy/wraith-benchmarks/blob/8db2c97bc72c7a7e57d2ba936120d29b86346a64/benchmarks/results/2026-11-04.md?plain=1#L64-L69">Totals in the results</a>.</sub></p>

Same 12 plans, same planted problems. With wraith the agent catches 127 of
180. Without it, 94. The intervals do not overlap.

<p align="center">
  <img src="assets/before-after.png" width="640" alt="The same plan review with and without wraith: without finds 1 of 3 planted defects, with finds all 3">
</p>

<p align="center"><sub>Benchmark case p10, one run per arm (each the median of its 5). Source rows: <a href="https://github.com/wraith-proxy/wraith-benchmarks/blob/8db2c97bc72c7a7e57d2ba936120d29b86346a64/benchmarks/results/2026-11-04.md?plain=1#L57-L58">p10 in the results</a>.</sub></p>

**What this does not prove:** these numbers measure plan review and nothing
else. Every other claim on this page is a description, not a measurement.

## The guard

Your agent reaches for `bq rm -r -f`. The ghost gets there first.

<p align="center">
  <img src="assets/demo-careful.gif" width="640" alt="An agent tries bq rm -r -f and the wraith guard blocks it">
</p>

<p align="center"><sub>A real Claude Code run with the guard in <code>deny</code> mode (<code>WRAITH_GUARD=deny</code>). The default, <code>ask</code>, prompts you instead.</sub></p>

Before the command runs, the guard checks it for the classics:
`terraform destroy`, `terraform apply -auto-approve`, `terraform state rm`,
`gcloud ... delete`, recursive `gsutil rm` and `gcloud storage rm`, `bq rm`,
`DROP TABLE`, `TRUNCATE TABLE`, `DELETE FROM`, `dbt build --full-refresh`,
`--target prod`, `git push --force`, `git reset --hard`, `git clean -f`,
`git branch -D` and `rm -rf` on `/` or `~`.

Three modes. `ask`, the default, prompts you. `deny` blocks. `off` steps
aside. `/wraith:careful` sets the mode for your project and explains what the
guard catches.

## Start here

- `careful`: stops the agent running a destructive command on production
  without asking you first.
- `plan-data-review`: checks a data plan for grain, contracts, cost, personal
  data and rollback before anyone builds it.
- `odcs-contracts`: writes and validates the data contract, and keeps your dbt
  models in step with it.
- `orchestrating-agents`: runs a written plan one card at a time through fresh
  subagents, and checks each result.

## One sprint

```text
think → plan → build → review → test → ship → reflect
```

Every phase leaves a file under `docs/wraith/<date>-<topic>/`, so the next
session, or the next engineer, picks up where the last one stopped. To see one
sprint as committed files, read the [worked example](docs/example/README.md).
Every skill and agent is in [docs/reference.md](docs/reference.md).

## Why wraith and not a general skills pack

General packs are good, and wraith stands on them (see Credits). wraith adds
what a GCP data team keeps needing:

- Grain and cost review of data plans before they are built.
- ODCS data contracts as the source of truth for your models.
- Blast-radius review of GCP infrastructure plans.
- A guard that asks before destructive commands.
- One sprint: plan, build, review, ship.

## FAQ

**Is the guard a security boundary?**
No. It is best-effort string matching that asks first. Anything that changes
production, pushes, deletes or spends beyond your dev cost cap still needs
your explicit go-ahead in the conversation.

**Do I need GCP?**
The sprint and the guard work on any project. The domain skills (BigQuery,
dbt on BigQuery, Cloud Run, Terraform on GCP) are written for data teams on
GCP.

**Claude Code or Copilot?**
Both, from one repository, with the same skills and agents. The Copilot CLI
guard checks shell commands only; the details are below.

**Why "wraith"?**
Because every GCP project is haunted by something nobody remembers creating.

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

## Companions

wraith does not copy vendor skills. It names them, and you install them from
the vendors (dbt Labs, Google, HashiCorp). Install steps and notes are in
[docs/reference.md](docs/reference.md#companions). Vendor skills run with your
agent's full permissions, so skim each SKILL.md before installing.

## Requirements

`python3` 3.9 or later on PATH for the hooks. Without it, Claude Code shows a
hook error and carries on, and Copilot carries on because each hook ends with
`|| true`.

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
number. Only the subject line decides a release; commit bodies are ignored.
Report problems and propose changes as issues on GitHub.

## Star history

<a href="https://star-history.com/#wraith-proxy/wraith-skills&amp;Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=wraith-proxy/wraith-skills&amp;type=Date&amp;theme=dark">
    <img src="https://api.star-history.com/svg?repos=wraith-proxy/wraith-skills&amp;type=Date" width="640" alt="Star history for wraith-proxy/wraith-skills">
  </picture>
</a>

---

<p align="center">👻 <b>A star costs nothing. A dropped prod dataset costs your weekend.</b></p>

<p align="center">
  <a href="PRIVACY.md">Privacy</a> | <a href="TERMS.md">Terms</a> | <a href="SUPPORT.md">Support</a> | <a href="SECURITY.md">Security</a> | <a href="LICENSE">License (MIT)</a>
</p>
