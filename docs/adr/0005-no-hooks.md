# ADR 0005: no hooks

Status: accepted. Date: 2026-11-06. Ticket: WSK-00099.

## Context

The Claude plugin directory accepts `command` hooks only from Verified
organizations, and there is no way to apply. It warned about this first, then
refused `85b78ad` (v0.5.11). wraith shipped two command hooks per host: the
session-start router and the destructive-command guard.

`SessionStart` takes only `command` and `mcp_tool` hooks, so the router has no
prompt-hook form. A prompt-hook guard would be a model call per tool call.

The directory scan reads the whole repository, not only the Claude manifest,
so the Copilot hooks could count against the plugin too.

## Decision

Remove every hook from both hosts: `hooks/`, `com.github.copilot/hooks/` and
their tests, with no replacement hook. The `careful` skill becomes the safety
net: an instruction to stop and get approval for the exact command.

This supersedes the hook parts of ADR 0001.

## Consequences

- wraith has no enforced guard on either host. README, PRIVACY, SECURITY and
  TERMS say so.
- The router is no longer injected; skills trigger from their descriptions.
- Restore the hooks from git if the organization becomes Verified.
