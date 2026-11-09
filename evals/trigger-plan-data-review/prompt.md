---
plugins: ["../../plugin"]
max_turns: 4
allowed_tools: [Read, Glob, Grep, Skill]
runs: 2
tags: [trigger]
---

My plan adds an incremental dbt model fct_payouts on BigQuery, partitioned by payout_date, merging on payout_id. Review the data side before we build it.
