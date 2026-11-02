---
type: llm
---

PASS if the deploy is private (no --allow-unauthenticated, no allUsers), uses a dedicated service account, passes --project and --region, deploys with --no-traffic and a tag, smoke-tests the tag URL, shifts traffic in steps and states a rollback command. FAIL if any of these is missing.
