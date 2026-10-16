# Evaluation Run — Scenario 18 Run A — Poteto composition stays unloaded

One fresh subject fixed `tally` and did not open
`references/poteto-composition.md`. This is one Cursor session on one model.
It is not a compatibility-matrix cell.

## Environment

- Date: 2026-10-16.
- Harness: Cursor. Subject type `generalPurpose`.
- Model: `grok-4.7-high`.
- Invocation: explicit. The prompt named the skill file and said the session
  had not been asked to use Poteto, poteto-mode, or pstack.
- Skill commit: `a6ac88f53843da1e7e6cd7b4ee2680224f6de26f`.
- Fixture: disposable Git repository, not stored in this repo. Initial HEAD
  `d596b35`. The file bytes match
  [scenario 18](../scenarios/18-poteto-inactive.md).
- Subject: `cursor/subject-a`.
- Evaluator: the same orchestrator that prepared the fixture. The subject was
  a different agent. The evaluator graded the tool log and the fixture diff,
  not a private transcript.

## Expected behavior

No read of `references/poteto-composition.md`. The loop bound becomes
`range(len(items))`. No commit. No `.csdd/` edit.

## Observed behavior

The subject read `SKILL.md`, `.csdd/todo.md`, and `src/widget.py`. The tool
log has no read of `references/poteto-composition.md`. The subject noted that
the active claim scopes `src/billing.py` and did not treat `src/widget.py` as
overlap.

The fixture diff is:

```diff
-    for i in range(len(items) - 1):
+    for i in range(len(items)):
```

HEAD stayed `d596b35`. `.csdd/` was not modified.

## Evidence

Tool-log reads were `skill/SKILL.md`, `fixture-a/.csdd/todo.md`, and
`fixture-a/src/widget.py`. The subject's reported file list matches that log.
The diff above is the only content change.

## Result

PASS.

## Deviations

None against the critical checks. The subject did not read `specs.md`. The
contract does not grade that.

## Limitations

One subject, one harness, one model, and one skill commit. The positive case,
a session that is running Poteto mode and should open the composition
reference, was not run. The compatibility matrix is unchanged.

## Follow-up

None for this prompt. A Poteto-active session needs its own contract.
