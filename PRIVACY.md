# Privacy

Last updated: 6 November 2026

wraith is a plugin made of instructions (skills and agents). It has no hooks,
no server, no account and no analytics.

## What wraith collects

Nothing. wraith sends no telemetry, checks for no updates and makes no
network requests from anything it runs on its own. It reads no personal
data and stores no data.

## What runs on your machine

Nothing runs on its own. wraith has no hooks or background processes.

## What your agent does with wraith's instructions

Skills may tell your agent to run commands that contact services such as
Google Cloud, dbt, Terraform registries or package indexes. Those commands
run in the open, with your credentials, subject to your agent's permission
prompts and to each service's own privacy terms. wraith receives nothing
from them.

## Wizards

If you ask for one, the wizard skill writes a bash script for you to run by
hand. When you run it, it may write values to a local `.env` file (created
readable only by you) and set GitHub Actions secrets or variables through
your own `gh` command-line tool. Nothing is sent to wraith.

## Your AI host

Your conversations, including the text wraith adds, are processed by your
agent host (for example Claude Code or GitHub Copilot) under that provider's
privacy terms.

## Age

wraith is not intended for anyone under 18.

## Companion plugins

The README recommends optional plugins from other vendors. They are
separate software with their own privacy terms.

## Changes and contact

Changes to this page are visible in the repository history.
Questions: open an issue at https://github.com/wraith-proxy/wraith-skills/issues,
or for anything private, use the private report form at
https://github.com/wraith-proxy/wraith-skills/security/advisories/new.
