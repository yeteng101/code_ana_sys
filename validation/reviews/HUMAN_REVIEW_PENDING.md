# Human Review Handoff

Status: `pending`

The simulated review is complete. The following steps require a human reviewer.

## Human-only steps

1. Open `validation/人工复核表-2026-10-16-simulated.xlsx`.
2. Review all 54 synchronization relations first.
3. Review all 17 confirmed resource-flow Gold operations and the 55 rejected
   duplicate resource candidates.
4. Spot-check at least 30% of the 220 call-chain rows, including every
   `Confirmed with condition` row.
5. For every disagreement, change `Decision` to `Needs fix` and record why.
6. Copy the human-reviewed workbook to a separate signed review artifact.
7. Synchronize accepted decisions into the source JSON datasets.
8. Set `review.human_review=confirmed` only after the review is complete.
9. Run the strict quality gate with `--strict-review`.

## Automated steps already completed

- Every evidence anchor was checked against the pinned source.
- Current SHA-256 source checks pass for libuv and Redis.
- Simulated decisions and reviewed Gold snapshots are generated.
- The generic evaluator and CI quality gate are implemented.

## Commands after human sign-off

```bash
python3 scripts/prepare_validation_truth.py
python3 scripts/run_validation_project.py \
  --project-id libuv \
  --ground-truth validation/benchmarks/libuv/ground-truth.json \
  --predictions validation/results/libuv/predictions \
  --output validation/results/libuv/final-review \
  --strict-review \
  --max-fp 0
python3 scripts/run_validation_project.py \
  --project-id redis \
  --ground-truth validation/benchmarks/redis/ground-truth.json \
  --predictions validation/results/redis/predictions \
  --output validation/results/redis/final-review \
  --strict-review \
  --max-fp 0
```
