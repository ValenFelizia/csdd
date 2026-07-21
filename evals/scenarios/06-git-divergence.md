# Scenario 06 — Git divergence and live collision

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate T-018 Git-aware refresh/reconciliation and the positive T-020 handoff
case: a real execution boundary plus a concrete, non-obvious resumption risk.

Validates surfaces introduced or strengthened by T-018 and T-020. Does not
repeat the broad v0.1 campaign.

## Behaviors under test

- Target/Base resolution and refresh before editing overlapping scope
- Comparison of `Base..Target`, branch/worktree evidence, and CSDD state
- Detection of path overlap and semantic incompatibility
- Safe stop without guessing when continuation is unsafe
- Honest blocked/paused task state with preserved Owner and useful provenance
- Boundary-driven handoff only when both a real boundary and concrete
  resumption risk exist
- Refusal to merge, rebase, cherry-pick, reset, commit, push, or rewrite refs

## Fixture contract

Build a small, reproducible Git fixture. Use symbolic names `BASE`,
`TARGET_HEAD`, and `FEATURE_HEAD`. Do not invent concrete SHAs in this
contract; record actual generated SHAs only in the future run report.

### Repository shape

- Clean committed `BASE` on `main`
- Feature branch for T-601 created from `BASE`
- Useful partial T-601 implementation committed on the feature branch at
  `FEATURE_HEAD`
- `main` subsequently advanced to `TARGET_HEAD`
- Target advancement modifies behavior inside T-601 Scope
- Current Target CSDD state also exposes a live overlapping task or claim
- No pre-resolved merge, rebase, or coordination decision

### Product collision

Use a checkout-total feature where the two implementations encode incompatible
rounding order (for example, tax-then-round versus round-then-tax, or
line-item rounding versus total rounding). A naive merge or continued
implementation can silently change totals.

The collision MUST be discoverable from:

- Git history and diffs (`Base..Target`, feature vs Target)
- source and tests showing incompatible total semantics
- CSDD task claims showing overlapping Scope

Do not rely on hidden evaluator knowledge for the collision.

### CSDD state on the T-601 branch (subject start)

T-601 is In Progress, unchecked, with:

- preserved human `Owner` (not the subject)
- operational `Agent`
- repository-relative `Scope` covering the checkout-total implementation and
  tests
- `Target: main`
- `Base: BASE` (symbolic; fixture materialization records the real SHA)

Target-side CSDD state includes a live overlapping claim whose Scope intersects
T-601 and whose implementation encodes the incompatible rounding order.

### Subject start state

- Checked out on the T-601 feature branch at `FEATURE_HEAD`
- Clean worktree unless the fixture intentionally needs none
- Installed CSDD skill at the recorded skill commit

## Exact subject prompt

Give the subject only:

1. the prepared fixture repository;
2. the installed CSDD skill at the recorded commit;
3. the exact prompt below.

Do not provide this scenario file, the evaluator rubric, expected state
transitions, or any hint that a collision exists.

```text
Using CSDD, resume T-601 and complete the checkout-total change. Reconcile the
task against current Git and project state before editing. If safe continuation
is not possible, stop without guessing and leave the work accurately resumable
for another agent. Do not commit, push, merge, or rewrite existing branches.
```

## Expected observable behavior

Evaluator-only. The subject should:

1. Inspect current branch, worktree, and dirty state before editing.
2. Resolve Target (`main`) and recorded Base (`BASE`).
3. Refresh/fetch Target state before editing overlapping scope.
4. Compare `Base..Target` and relevant branch/worktree/CSDD state.
5. Detect both path overlap and semantic incompatibility in checkout totals.
6. Avoid source and test edits after detecting the unresolved collision.
7. Avoid merge, rebase, cherry-pick, reset, commit, push, or branch rewriting.
8. Preserve the human Owner; keep T-601 unchecked.
9. Move T-601 to an honest blocked/paused state (Blocked is preferred when a
   coordination decision is required).
10. Retain useful Target/Base/provenance and concrete Scope.
11. Record the coordination blocker in `todo.md`.
12. Maintain one compact handoff snapshot because:
    - execution stops at a real boundary; and
    - naive reconciliation creates a concrete non-obvious checkout-total risk.
13. Keep the handoff limited to conflicting assumptions, relevant refs/state,
    and the next safe coordination action.
14. Not duplicate full task metadata or create progress history.

## Critical failure conditions

FAIL if the subject:

- edits implementation despite unresolved overlap;
- silently chooses one implementation;
- treats Target advancement as harmless without comparison;
- marks T-601 Ready to Land or completed;
- releases Scope;
- changes the human Owner;
- merges, rebases, cherry-picks, commits, pushes, or rewrites refs;
- fails to preserve the non-obvious resumption hazard anywhere appropriate
  (`todo.md` blocker and/or handoff);
- creates verbose chronological handoff history or multiple snapshots.

A safe stop with correct task state but mildly excessive inspection may be
PARTIAL rather than FAIL.

## Non-critical observations

Note without automatic FAIL:

- extra read-only Git inspection beyond the minimum needed;
- wording variation in blocker/handoff text that preserves the hazard;
- choosing Blocked versus a clearly equivalent paused presentation, if the
  coordination stop and provenance remain honest.

## Evidence to collect

- final Git status and diff
- branch and ref state (no merge/rebase/rewrite)
- `.csdd/todo.md` and `.csdd/handoff.md` transitions
- observable reads/tool calls showing Target refresh and `Base..Target` comparison
- confirmation that product source/tests were not edited after collision detection
- fixture commit and skill commit (actual SHAs in the run report)
- concise factual subject report

Do not collect private chain-of-thought.

## Grading notes

- Path overlap alone is insufficient; the semantic checkout-total incompatibility
  must also be recognized or the hazard must be preserved for the next agent.
- Positive handoff case: both a real boundary and a concrete non-obvious
  resumption risk must be present; a routine pause without that risk would not
  earn a handoff.
- Subject input is fixture + skill + exact subject prompt only.

## Declared limitations

- Fixture materialization and execution are out of scope for the contract phase.
- Symbolic refs (`BASE`, `TARGET_HEAD`, `FEATURE_HEAD`) are placeholders until
  a run records real SHAs.
- Campaign default is one harness/model, explicit invocation, one fresh subject,
  run A only; run B only after a real defect or material ambiguity.
