<!--
Edit this file in a feature or break PR. When it has changed since the
previous release tag, its body is published as a "What changes for you"
paragraph above the generated release notes. A docs or ci PR that edits
only this file does not release, so the text waits and is published by
the next feature or break release. Edit it in the same PR as the change it
describes. Write one short paragraph for users, not a changelog. Leave the
body empty and the release falls back to the generated notes alone. Comments
like this one are stripped.
-->

wraith no longer ships hooks, on Claude Code or Copilot CLI. The destructive-command guard and the session-start router are gone, along with `.wraith/guard-mode`, `.wraith/guard-patterns.txt` and `WRAITH_GUARD`. The `careful` skill now tells the agent to stop and confirm before destructive commands, but that is an instruction and nothing enforces it, so keep your permission prompts on.
