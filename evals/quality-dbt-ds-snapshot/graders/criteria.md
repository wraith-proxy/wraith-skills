---
type: llm
---

PASS if the model is partitioned on a DATE column named ds, writes one ds per run idempotently (insert_overwrite or equivalent), takes ds from a var, and tests uniqueness on (subscription_id, ds). FAIL if it uses dbt snapshots or SCD2 valid_from and valid_to columns, or has no ds partition.
