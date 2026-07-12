# Evaluation Run 004A — Stale Claim Reconciliation

## Environment

- Harness: Cursor
- Model: Grok 4.5
- CSDD invocation: explicit
- Skill commit: [record commit]
- Fixture commit: [record baseline commit]
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