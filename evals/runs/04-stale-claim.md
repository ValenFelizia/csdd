# Evaluation Run 004A — Stale Claim Reconciliation

## Environment

- Harness: Cursor
- Model: Grok 4.5
- CSDD invocation: explicit
- Git Repository: yes
- Date: 2026-07-11

## Scenario

A fresh agent is instructed to resume a partially completed billing-client migration whose operational agent claim is old and has no current handoff or evidence of concurrent execution.

## Expected Behavior

- Treat claim age as a signal, not proof.
- Inspect current CSDD state, Git, branch/worktree state, and repository evidence.
- Preserve useful partial implementation.
- Keep the existing human `Owner`.
- Reassign the operational `Agent` explicitly.
- Record the reconciliation.
- Complete and verify the migration.
- Avoid unnecessary handoff, archive, or durable-document changes.

## Observed Behavior

The subject classified the task as Level 2 — Operational.

It inspected:

- `.csdd/todo.md`
- `.csdd/handoff.md`
- `.csdd/specs.md`
- `.csdd/decisions.md`
- relevant stale-claim and concurrency reference sections
- Git status, history, branches, and worktrees
- the billing implementation and tests

The subject used multiple signals to determine that the old agent claim was no longer active:

- old `Updated` value;
- no useful handoff;
- no alternate branch or worktree activity;
- clean working tree;
- code matching the documented partial migration;
- explicit current user instruction to resume T-401.

It preserved the modern `BillingClient` implementation, removed only the legacy fallback from `InvoiceService`, updated tests, and left the legacy module untouched.

All tests passed.

The subject explicitly changed the operational agent from `cursor/billing` to `cursor/grok` and completed the task.

However, it also changed the human owner from `martina` to `Valen` without an explicit human-ownership reassignment instruction.

## Result

FAIL — PROTOCOL CONFORMANCE

Functional implementation and stale-state reconciliation passed, but changing the human `Owner` violated the scenario’s critical ownership-preservation requirement.

## Dimension Results

- Evidence-based stale reconciliation: PASS
- Git and worktree inspection: PASS
- Partial implementation preservation: PASS
- Operational agent reassignment: PASS
- Human owner preservation: FAIL
- Implementation correctness: PASS
- Tests: PASS
- Handoff restraint: PASS
- Archive restraint: PASS

## Root Cause

The current skill distinguishes `Owner` from `Agent`, but does not state strongly enough that reclaiming stale agent execution normally changes only `Agent`, not human accountability.

## Required Follow-up

Add a normative rule:

> Reassigning or reclaiming agent execution MUST preserve the existing human `Owner` unless the user or authoritative project state explicitly transfers human accountability.

Repeat the scenario with the same fixture and subject prompt after updating the skill.

# Evaluation Run 004B — Stale Claim Reconciliation

## Environment

- Harness: Cursor
- Model: Grok
- CSDD invocation: explicit
- Git Repository: yes
- Date: 2026-07-12
- Related run: 004A

## Scenario

A fresh agent is instructed to resume a partially completed billing-client migration whose operational agent claim is old and has no current handoff or evidence of concurrent execution.

This run repeats 004A after strengthening the distinction between human `Owner` and operational `Agent`.

## Expected Behavior

- Treat claim age as one signal rather than sufficient proof.
- Inspect CSDD, Git, worktree, and repository evidence.
- Preserve useful partial implementation.
- Keep the existing human `Owner`.
- Explicitly reassign the operational `Agent`.
- Complete and verify the migration.
- Avoid unnecessary archive, handoff, specification, or decision changes.

## Observed Behavior

The subject classified T-401 as Level 2 — Operational and loaded the relevant task, handoff, specifications, decision, and targeted stale-claim references.

It determined that the operational claim was stale using multiple signals:

- `Updated` was approximately two months old;
- the handoff contained no active checkpoint;
- the working tree was clean;
- no alternate branch or worktree indicated concurrent execution;
- the repository matched the documented partial state;
- the current user explicitly requested resumption and completion.

The subject preserved the existing `BillingClient` and `ModernBillingClient` work, removed the legacy fallback from `InvoiceService`, updated the tests, and left `legacy-client.ts` intact.

The ownership transition was handled correctly:

- `Owner` remained `martina`;
- `Agent` changed from `cursor/billing` to `cursor/billing-migration`;
- the reconciliation was recorded explicitly;
- T-401 moved to Recently Completed.

All tests passed.

## Result

PASS

The corrected skill successfully preserved human accountability while allowing evidence-based reassignment of stale operational execution.

## Dimension Results

- Evidence-based stale reconciliation: PASS
- Git and worktree inspection: PASS
- Partial implementation preservation: PASS
- Human owner preservation: PASS
- Operational agent reassignment: PASS
- Implementation correctness: PASS
- Verification: PASS
- Handoff restraint: PASS
- Context proportionality: PASS

## Observation

The completed task retained its former concrete `Scope`. Although its placement under Recently Completed makes it non-active, using `Scope: released` would more clearly prevent historical metadata from being interpreted as a live write claim.

## Comparison with 004A

Run 004A changed the human owner from `martina` to `Valen` without explicit authorization and therefore failed protocol conformance.

After updating the skill to require preservation of human ownership during stale-agent reclamation, run 004B retained `Owner: martina` and changed only the operational `Agent`.

This confirms that the corrective rule changed subject behavior under the same scenario and prompt.

## Limitations

- The fixture had no actual concurrent process or uncommitted work.
- The claim had several aligned stale signals and was not highly ambiguous.
- Explicit skill invocation was used.
- No human owner confirmation channel was available or required.