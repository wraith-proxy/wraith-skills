---
plugins: ["../../plugin"]
max_turns: 4
allowed_tools: [Read, Glob, Grep, Skill]
runs: 2
tags: [trigger]
---

Our text-to-SQL agent keeps picking the wrong revenue table. Set things up so it queries the warehouse correctly.
