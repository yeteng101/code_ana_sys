# Analyzer Enhancements (2026-10-21)

## 1. Synchronization

Implemented:

- Cross-function queue publication/consume pairs.
- Atomic release/acquire and relaxed-unknown relations.
- Thread create/join relations.
- Visible `held_locks` and improved thread-context hints.
- Source scanning for atomic macros that do not produce standalone call edges.

Validation:

- Redis synchronization: `9 TP / 13 FN`, recall 40.91%, F1 58.06%.
- Synthetic fixtures cover queue, atomic and thread-join relations.

## 2. Resource Flow

Implemented:

- Function-local assignment and return scanning.
- Alias closure for simple pointer assignments.
- Cross-function returned-resource ownership transfer.
- `assignment_chain` and `data_flow` facts on resource results.

Remaining:

- Path-sensitive points-to analysis.
- Heap object identity beyond simple variable aliases.
- Full error-path and branch sensitivity.

## 3. Call Graph

Implemented:

- Builtin normalization such as `__builtin_memset -> memset`.
- Macro invocation-line mapping instead of macro-definition-line mapping.
- Platform `#if/#ifdef` conditions recorded on call edges.
- Macro definitions used during verification of expanded call targets.

## 4. Human Review

Human-only steps are listed in:

```text
validation/reviews/HUMAN_REVIEW_PENDING.md
validation/reviews/human-review-status.json
```

Status remains `pending`. The strict gate will fail until a human reviewer
sets `review.human_review=confirmed`.

## 5. Validation and CI

Use:

```bash
python3 scripts/run_validation_project.py \
  --project-id <project-id> \
  --ground-truth <ground-truth.json> \
  --predictions <external-json-dir> \
  --output <report-dir> \
  --max-fp 0
```

Outputs:

```text
report.json
report.md
gate.json
```

Threshold failures return a non-zero exit code. Add `--strict-review` for the
final post-human-review gate.
