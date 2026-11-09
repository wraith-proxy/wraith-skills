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

wraith now ships only its data and GCP skills: 15 skills and 5 agents. The process skills (brainstorming, writing-plans, orchestrating-agents, tdd, systematic-debugging, verification-before-completion, grilling, handoff, knowledge-base, writing-skills, review and ship) and the architect, implementer, reviewer, tester, junior-dev, docs-writer and git-workflow-master agents are gone. Install obra/superpowers and mattpocock/skills for those workflows; docs/reference.md lists which skills wraith recommends. The wraith block keys test_command, lint_command, release_tooling, knowledge_dir and adr_dir are no longer read.
