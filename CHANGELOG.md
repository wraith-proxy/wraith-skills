# Changelog

## v0.5.8 (2026-11-03)

### Bug Fixes

- add plugin icon for the directory listing (#28)

## v0.5.7 (2026-11-03)

### Bug Fixes

- ignore HANDOVER.md (#27)

## v0.5.6 (2026-11-03)

### Bug Fixes

- bump GCP companion pin to 0c369ce (#26)

## v0.5.5 (2026-11-03)

### Bug Fixes

- use default-branch HEAD when newest tag is older than the pin (#25)

## v0.5.4 (2026-11-03)

### Bug Fixes

- sync PRs carry , ci merges on green (#24)
- sync upstream report only (#23)

## v0.5.3 (2026-11-02)

### Bug Fixes

- show in-session plugin install commands in README (#22)

## v0.5.2 (2026-11-02)

### Bug Fixes

- skip release when no files changed (#21)

## v0.5.1 (2026-11-02)

### Bug Fixes

- sync upstream report only (#18)

## v0.5.0 (2026-11-02)

### Features

- upstream sync and release automation (#17)
- add upstream sync engine
- print keys whose pins are safe to bump
- add release workflow
- add nightly upstream sync workflow

## v0.4.0 (2026-11-02)

### Bug Fixes

- let codespell accept disjointness
- guard asks on git branch -D only, not -d

### Features

- hooks, evals and README (#16)
- add session-start router and destructive-command guard
- add trigger and quality evals
- write README

## v0.3.0 (2026-11-02)

### Features

- sprint skills and agents (#15)
- add security-audit and careful
- add qa
- add deploy
- add core agents
- add specialist agents

## v0.2.0 (2026-11-02)

### Bug Fixes

- match ghost prefix in changelog patterns

### Features

- release workflow (#14)
- auto-merge only PRs titled [automerge]
- add release workflow

## v0.1.0 (2026-11-02)

### Bug Fixes

- backtick bigquery vendor skill names
- name Google alert skills in terraform-gcp
- isolate privacy scan test from hook git env
- tidy vendored leftovers
- inline AGENTS.md rules, drop PLAN.md pointer

### Features

- domain skills (#13)
- vet dbt companion
- vet google companion
- vet hashicorp companion
- add odcs-contracts
- add dbt-bigquery
- add bigquery
- add cloud-run
- add terraform-gcp
- add ontology-modeling and context-layer
- add plan-data-review and plan-infra-review
- auto squash merge PRs when CI passes
- core process skills (#12)
- vendor brainstorming and writing-plans
- add using-wraith router
- vendor tdd, debugging and verification
- add orchestrating-agents
- vendor handoff, knowledge-base and setup
- vendor grilling, wizard and writing-skills
- vendor review and ship
- scaffold and guardrails (#11)
- scaffold tooling and manifests
- add privacy scanner
- add skill and agent linter
- add manifest tests
- add copilot agent generator and upstream fetcher
- add skill and agent stubs
- add CI and activate hooks
- record dual-host tracer results
- add gitignore
