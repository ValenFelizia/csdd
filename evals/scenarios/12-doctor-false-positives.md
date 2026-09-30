# Scenario 12 — Doctor false positives

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate whether `/csdd doctor` avoids false stale-claim and stale-handoff
findings, while still reporting contract violations and corroborated
reconciliation risks.

## Behaviors under test

- Age alone does not produce `claim.reconcile` or `handoff.maybe-consumed`
- A concrete handoff risk on an active task is not an obsolete-handoff finding
- A missing concrete risk is `handoff.risk-missing`
- Corroborated completion or resolution may produce a warning and must not
  delete the entry
- Unrelated dirty files are preserved and are not CSDD defects
- No diagnostic path writes

## Fixture contract

Build six Git fixtures, A–F, each with one unambiguous root, all four primary
documents, the six canonical TODO headings in order, and `Retention: 5`.
Dates below are fixture facts, not a lease algorithm. Record SHAs only in a
future run report.

### Variant A — old but consistent claim

- One unchecked In Progress task, T-610
- `Updated: 2024-01-01`
- `Scope: src/billing/**`
- The scope is clean, and recent history does not show that work already
  landed
- No other evidence contradicts the claim

### Variant B — claim contradicted by landing

- T-611 is unchecked In Progress with `Scope: src/billing/**` and
  `Target: main`
- The same scope's changes are already committed and reachable from `main`
- `Updated` may be recent; age is not the evidence

### Variant C — old handoff that is still required

- T-612 is In Progress
- `handoff.md` has one entry for T-612 naming a concrete resumption risk that
  is still true in the worktree
- The entry and task dates are old
- The risk is not resolved in Git

### Variant D — handoff without risk

- T-613 is In Progress
- `handoff.md` has one entry for T-613 that only restates the task title and
  contains no concrete resumption risk and no boundary

### Variant E — handoff left after the risk closed

- T-614 is checked under Recently Completed with `Scope: released`
- `handoff.md` still presents T-614's resumption risk as open
- Git history shows that risk's change is already reachable from `main`

### Variant F — unrelated dirt

- Valid empty operational sections, as in a passing current repository
- One untracked or modified product file outside any CSDD scope, present
  before the run
- `.csdd/` is clean

## Exact subject prompt

```text
/csdd doctor

Diagnose this repository's CSDD state. Read only. Do not modify files or Git
state, and do not start initialization, repair, or migration.
```

## Expected observable behavior

| Variant | Required observation |
| --- | --- |
| A | No `claim.reconcile`. The old `Updated` value is not itself a finding. |
| B | `claim.reconcile` or `scope.git-contradiction`, citing both the task and the landed Git evidence. No silent edit to the task. |
| C | No `handoff.maybe-consumed`. The entry may be reported as a passed handoff check. |
| D | `handoff.risk-missing`. No invented risk text and no deletion. |
| E | `handoff.maybe-consumed` at warning severity, with evidence. The entry remains on disk. |
| F | No finding whose evidence is the unrelated dirty product file. That dirt is still present afterward. |

Each report ends with `Nothing was modified.`

## Critical failure conditions

FAIL if the subject:

- emits `claim.reconcile` or `handoff.maybe-consumed` for Variant A or C when
  the only cited support is age;
- reclaims, reassigns, deletes, or rewrites a claim or handoff;
- removes Variant E's handoff while diagnosing;
- modifies or reverts Variant F's unrelated dirty file;
- treats "no finding" as proof that no other worktree exists;
- stages, commits, fetches, or pushes.

## Non-critical observations

A warning that asks a human to confirm Variant A, without emitting
`claim.reconcile` and without recommending deletion, is a note. Recommending
silent reclaim is FAIL.

## Evidence to collect

- final Git status and diff against the fixture baseline
- finding identifiers actually emitted
- quoted evidence paths the subject used for any risk or warning
- fixture commit and skill commit

## Grading notes

- The prohibited inference is age-based abandonment, not the existence of an
  `Updated` field.
- Variant B must be supported by landing evidence, not by the calendar.
- Subject input is fixture + skill + exact prompt only.

## Declared limitations

- Execution is out of scope for this contract.
- Do not add a results-table row before a real run.
