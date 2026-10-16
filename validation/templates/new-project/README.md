# New Validation Project

This is the template for a repository-specific validation project. The generic
evaluator is reused; only the repository pin, candidates, review decisions, and
Gold are new.

## Required files

```text
manifest.json
source-manifest.json
ground-truth.json
candidates.json
gold-additions.json
review-table.csv
review-checklists/
```

## Workflow

```text
pin repository and commit
-> run URL-Subagent Clang pipeline
-> collect analyzer candidates into review-table.csv
-> review every decision and evidence anchor
-> add manually discovered Gold to gold-additions.json
-> build ground-truth.json
-> pin source hashes
-> check registry
-> run the generic evaluator
```

Candidate-derived Gold covers the analyzer's candidate space. Manual additions
are required to measure recall for facts the analyzer missed.
