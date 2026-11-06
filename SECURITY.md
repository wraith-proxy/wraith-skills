# Security

Report a vulnerability privately through GitHub:
https://github.com/wraith-proxy/wraith-skills/security/advisories/new

Please include what you found, how to reproduce it and the affected
version. You will get an acknowledgement on a best-effort basis.

wraith's `careful` skill is an instruction to the agent, and its Copilot CLI
guard hook is best-effort pattern matching. Neither is a security boundary.
A command that slips past them is a bug worth reporting, but not a
vulnerability in the sense of this policy.
