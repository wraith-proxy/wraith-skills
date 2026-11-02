# Rules from experience

- Set the model on every dispatch: opus only for orchestration and hard synthesis, sonnet for implementation, review and fixes, haiku for mechanical edits and lookups. Never let a subagent inherit the session model.
- Run at most two implementers at once.
- Give deadlines as absolute epoch seconds, never as clock times.
- Recount any number an agent reports from the artifact itself (file, table, CSV) before repeating it.
- Haiku agents must write their output file, read it back and confirm it exists; check the file yourself after the run.
- Give prose-writing agents every fact inline and low effort; they never re-explore.
- Agents that run dbt or other tools cd into the project directory first. After each card, run `git status --short --ignored` and `du -sh` on the worktree to catch spill files.
- Each card ends in exactly one commit and no push.
- Reviewers read only the diff and the card, and check the owned-files boundary with `git diff --name-only`.
- Prefer wraith agents (wraith:implementer, wraith:reviewer, wraith:junior-dev and the specialists) when the host lists them.
