# Worked example

A toy dbt-on-BigQuery project and the artifacts a plan review and a contract-first build leave behind, so you can see what wraith's part of the work looks like in committed files.

**Honest scope.** This is an illustrative walkthrough. No warehouse was queried, no `dbt build` was run and no number here is a measurement. Names (`shop-analytics`, `raw.raw_orders`) are made up. The point is the shape of the artifacts, not the data. The dbt models in `project/models/*/*.md` are Markdown with the SQL in a fenced block, so the project does not build as shipped: copy each block into a `.sql` file under `models/` before running the dbt build command.

## The task

"Finance wants a daily revenue table by country." One mart, one source, one personal-data field to keep out.

## Read in this order

| Step | Skill | File |
|---|---|---|
| Design (input) | your own process or a companion; wraith does not write it | [sprint/design.md](sprint/design.md) |
| Plan (input) and its Data review | `wraith:plan-data-review` appends the review | [sprint/plan.md](sprint/plan.md) |
| Build | `wraith:odcs-contracts`, `wraith:dbt-bigquery` | [project/](project/) |

## What to notice

- The contract is written first and the models follow it.
- The plan review changed the plan before any code existed (see `plan.md`, "Data review").
