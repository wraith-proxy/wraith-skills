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

wraith now lives in the `plugin/` folder of its repository, so an install carries only the plugin: manifests, skills, agents, the icon and the legal files. The marketplace and plugin names are unchanged, so update as usual. A direct Copilot install of the repository root no longer works; use the marketplace, or `copilot plugin install wraith-proxy/wraith-skills:plugin`.
