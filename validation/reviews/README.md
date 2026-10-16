# Simulated Review

`simulated-review-2026-10-16.json` contains a row-level AI-assisted review of
the 356 entries in `validation/人工复核表-2026-10-16.xlsx`.

The review checks every evidence anchor against the pinned libuv/Redis source
checkouts, then applies category rules. It is not a human confirmation:

```text
human_review = pending
method = simulated_manual_review_by_codex
```

Decisions:

```text
Confirmed
Confirmed with condition
Rejected
Needs fix
```

The reviewed Excel workbook is:

```text
validation/人工复核表-2026-10-16-simulated.xlsx
```

Reviewed Gold snapshots are separate from the official pending-review
benchmarks:

```text
validation/benchmarks/libuv/ground-truth.simulated.json
validation/benchmarks/redis/ground-truth.simulated.json
validation/benchmarks/libuv/source-check.simulated.json
validation/benchmarks/redis/source-check.simulated.json
```

The generator is `scripts/simulate_validation_review.py`.

Reproduce without Excel dependencies:

```bash
python3 scripts/simulate_validation_review.py --skip-workbook
```

To regenerate the Excel file, run it with a Python environment that has
`openpyxl` installed:

```bash
python3 scripts/simulate_validation_review.py
```
