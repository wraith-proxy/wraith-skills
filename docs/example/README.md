# Worked example: one wraith sprint

A toy dbt-on-BigQuery project and the artifacts one sprint leaves behind, so you can see what plan, build, review and ship look like in committed files.

**Honest scope.** This is an illustrative walkthrough. No warehouse was queried, no `dbt build` was run and no number here is a measurement. Names (`shop-analytics`, `raw.raw_orders`) are made up. The point is the shape of the artifacts, not the data.

## The task

"Finance wants a daily revenue table by country." One mart, one source, one personal-data field to keep out.

## Read in this order

| Phase | Skill | File |
|---|---|---|
| Think | `wraith:brainstorming` | [sprint/design.md](sprint/design.md) |
| Plan | `wraith:writing-plans`, `wraith:plan-data-review` | [sprint/plan.md](sprint/plan.md) |
| Build | `wraith:odcs-contracts`, `wraith:dbt-bigquery` | [project/](project/) |
| Review | `wraith:review` | [sprint/review.md](sprint/review.md) |
| Ship | `wraith:ship` | [sprint/ship.md](sprint/ship.md) |

## What to notice

- The contract is written first and the models follow it.
- The plan review changed the plan before any code existed (see `plan.md`, "Data review").
- The reviewer's blocker is something a test can fail on, not an opinion.
- Nothing ships until the checks in `ship.md` are run for real; the file lists them as to-run, because this example did not run them.
