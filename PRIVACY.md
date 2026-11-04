# Privacy

Last updated: <HUMAN: date>

wraith is a plugin made of instructions (skills and agents) and two small
local hook scripts. It has no server, no account and no analytics.

## What wraith collects

Nothing. wraith sends no telemetry, checks for no updates and makes no
network requests from anything it runs on its own. It reads no personal
data and stores no data.

## What runs on your machine

- **Session start hook** reads wraith's own `using-wraith` skill file and adds
  it to your agent's session context.
- **Guard hook** runs before shell commands. In Claude Code it also runs
  before MCP tool calls; in GitHub Copilot CLI it checks only `bash` and
  `powershell` commands, so MCP tool calls are not checked there. The host
  passes the hook the pending command, or for MCP calls the full tool
  arguments as JSON, plus the working directory. The hook checks that text
  against a list of destructive patterns and answers "ask" or "deny", or
  nothing. The check happens locally and the text is discarded when the
  hook exits. To choose its mode and any extra patterns it reads the
  `WRAITH_GUARD` environment variable, and `.wraith/guard-mode` and
  `.wraith/guard-patterns.txt` in your project if they exist. It stores
  nothing, writes no files and sends nothing; its only output is its
  answer to your agent host.

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
Questions: <HUMAN: contact address or "open an issue">.
