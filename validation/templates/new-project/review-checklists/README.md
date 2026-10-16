# Review Checklists

Use a Markdown or Excel checklist with:

```text
Category
Project
ID
Source
Source evidence
Target
Target evidence
Type / Order
Expected result
Current status
Decision
Notes
```

Decisions:

```text
Pending
Confirmed
Confirmed with condition
Rejected
Needs fix
```

`Confirmed` and `Confirmed with condition` become positive Gold.
`Rejected` becomes a negative Gold case for the same identity/kind.
`Pending` and `Needs fix` are excluded from Gold until resolved.

Do not edit generated `ground-truth.json` directly. Put missed facts in
`gold-additions.json`, rebuild Gold, then run the registry checker.
