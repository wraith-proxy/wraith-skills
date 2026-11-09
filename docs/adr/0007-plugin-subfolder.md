# ADR 0007: serve the plugin from a subfolder

Status: accepted. Date: 2026-11-09. Ticket: WSK-00109.

## Context

The Claude directory has held every version from v0.7.0 to v0.8.1 under "Uses a credential from the user's machine" (rule `MCP_FORWARDS_CREDENTIAL_ENV`, anchored on `.claude-plugin/plugin.json`). ADR 0006 removed the curl token text (Card H) and the model API key steps from CI (first addendum). The hold stayed.

The marketplace entry was `"source": "./"`, so the plugin folder was the repository root, and the scan read CI workflows, docs, ADRs and evals as plugin content. The workflows still pass the release bot's GitHub App token to `gh` through the environment. `skills/`, `agents/` and `README.md` hold no credential text. The directory's submit page says: "If the plugin is one folder in a larger repository, give that folder as the plugin path when you submit; the directory reads and scans only that folder." It also says a submission's repository and folder cannot change after submission.

The root layout also shipped `docs/`, `evals/`, `.github/`, `CHANGELOG.md` and `upstream-pins.txt` to every Claude Code and Copilot user.

## Options

1. **Relative subfolder in this repo, `"source": "./plugin"` (chosen).** One repo, one marketplace, the same install commands. Both hosts resolve relative sources from the repository root.
2. **A CI-built plugin-only branch or repo.** Generated trees, two sources of truth, and a release workflow that pushes them.
3. **Move CI, docs and evals to another repo that watches this one.** Keeps the current submission, but PR gating and releases become cross-repo, run with the bot token, and docs live apart from the code.
4. **Keep the root and remove non-plugin files.** Impossible: CI must live in `.github/workflows`.

Option 1 is the smallest change that puts only plugin content in the scanned folder, and the directory documents it.

## Decision

The plugin lives in `plugin/`. The marketplace entry is `"source": "./plugin"`.

```text
.claude-plugin/marketplace.json   stays (marketplace root = repo root)
.github/ .pre-commit-config.yaml .cz.yaml .secrets.baseline.json
.gitignore .claude/ AGENTS.md CHANGELOG.md RELEASE_NOTES.md
SECURITY.md upstream-pins.txt docs/ evals/        stay
README.md LICENSE                                  stay (GitHub page)
assets/ (before-after, demo-careful, numbers, social-preview)  stay
plugin/
  .claude-plugin/plugin.json       moved
  plugin.json                      moved (Agent Plugins manifest)
  com.github.copilot/agents/       moved (generated)
  skills/ agents/                  moved
  assets/icon.png                  moved ("icon": "./assets/icon.png" unchanged)
  PRIVACY.md TERMS.md SUPPORT.md THIRD_PARTY_NOTICES.md   moved
  LICENSE                          copy of root LICENSE, kept identical by a check
  README.md                        new listing README
```

- THIRD_PARTY_NOTICES.md moves because the MIT notices travel with the adapted skills.
- No symlinks: lint rule L15 forbids them.
- The listing URLs become `https://github.com/wraith-proxy/wraith-skills/blob/main/plugin/{SUPPORT,PRIVACY,TERMS}.md`.
- `plugin/README.md` is the listing description (the directory requires at least 40 words in the plugin folder). It says what wraith is, how to install it, and what it runs, sends and stores.

### Hosts

- Claude Code resolves a relative source from the marketplace root, so `./plugin` means `<repo>/plugin`. No `metadata.pluginRoot`.
- Copilot CLI resolves a relative source from the repository root and reads the Agent Plugins manifest at the plugin root, so `plugin/plugin.json` and `plugin/com.github.copilot/agents/` should work with no extra file (gate G3).
- A direct Copilot install of the repo root stops working; the direct form becomes `wraith-proxy/wraith-skills:plugin`. The README never recommended direct installs.

### Evals

`evals/` stays at the root so it never ships. Each case names the plugin under test with `plugins: ["../../plugin"]` (relative to the case directory). Runs go from the repo root (gate G5).

### Tooling

wraith-tooling reads the plugin root from `.claude-plugin/marketplace.json` (`layout.plugin_root`). Lint, the Copilot agent build and the plugin checks work on that folder, and a subfolder plugin may hold only the allowlisted plugin content. A missing marketplace file or `"./"` still means the repo root.

## Effects

- Marketplace `wraith-proxy` and plugin `wraith` keep their names and install commands. `claude plugin update` and `copilot plugin update` should fetch the moved plugin (gate G6). Released as a patch.
- The directory review starts over as a new submission with Plugin path `plugin`; the held submission is withdrawn after the new one validates.
- awesome-copilot: submit with path `plugin` (gate G8).

## Gates

- **G1 (before merge):** `claude plugin validate --strict .` and `claude plugin validate --strict plugin` both pass.
- **G2 (before merge), Claude Code:** under a throwaway HOME, add the marketplace from the PR branch, install `wraith@wraith-proxy`, confirm 15 skills and 5 agents, and confirm the install has no `.github`, `docs` or `evals`.
- **G3 (before merge), Copilot CLI:** under a throwaway HOME, add the marketplace from the local checkout, install `wraith@wraith-proxy`, confirm 15 skills, and that the installed tree holds only plugin content.
- **G4 (before merge), directory:** the owner validates the PR branch in the portal with Plugin path `plugin`. Pass means no blocking finding and no credential hold.
- **G5 (before merge), evals:** one trigger eval runs from the repo root against `plugin/`.
- **G6 (after release):** `claude plugin update wraith@wraith-proxy` and `copilot plugin update wraith` on a throwaway HOME with the previous release report the new version.
- **G7 (after release):** new directory submission with path `plugin`, then withdraw the held one.
- **G8:** read the live awesome-copilot form before resubmitting.

## Consequences

- Only plugin content ships, and `wraith-check-plugin` enforces the allowlist.
- Two LICENSE copies and two READMEs: the GitHub page at the root, the listing in `plugin/`.
- The directory review restarts as a new submission.
