---
plugins: ["../../plugin"]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill, Write]
runs: 2
tags: [quality]
---

Create a dbt model on BigQuery that keeps a daily snapshot of the source raw.subscriptions (subscription_id, customer_id, plan, status, updated_at). Write the model file and its YAML.
