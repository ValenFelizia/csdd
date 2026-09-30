# Scenario 12 — Status derived snapshot

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate `/csdd status` on valid empty and valid active CSDD states. Counts and
claims must come from the canonical documents. The default report must stay
brief and must not write a status file.

## Behaviors under test

- Explicit harness-agnostic invocation
- Counts for the six canonical states
- Active claims, Ready to Land `Landing:` lines, handoff IDs, and retention
  usage
- Pointers back to canonical files instead of full task or handoff bodies
- No repository changes and no persisted status artifact
- The no-overlap sentence is limited to inspected state

## Fixture contract

Each variant is its own Git repository with a clean committed baseline, one
unambiguous root, all four primary documents, the six canonical TODO headings
in order, and `Retention: 5`. Put a distinctive sentence in any task note and
in any handoff body, so a copied body is detectable. Do not give the subject
this contract.

### Variant A — empty current state

- No tasks
- No handoff entries
- Clean worktree

### Variant B — active current state

`todo.md` contains:

- two unchecked In Progress tasks, T-710 and T-711, each with `Agent` and a
  concrete `Scope`
- one unchecked Ready to Land task, T-712, with `Landing: open PR against main`
  and a long `Verification:` paragraph containing the distinctive sentence
- zero Blocked tasks
- one unchecked Pending task, T-713
- one unchecked Deferred task, T-714, with `Reason:` and `Resume when:`
- two checked Recently Completed tasks
- no overlapping scopes

`handoff.md` contains one entry for T-710. The entry states a concrete risk
and includes the distinctive sentence. It does not duplicate the full TODO
entry.

## Exact subject prompt

```text
/csdd status

Give the current CSDD snapshot. Read only. Do not modify files or Git state.
```

Do not ask for detail.

## Expected observable behavior

| Variant | Required observation |
| --- | --- |
| A | Counts are zero for every canonical state. Retention is `0/5`. Handoff count is 0. The report does not describe the repository as having no `.csdd/`. |
| B | Counts are 2, 1, 0, 1, 1, and 2 for In Progress, Ready to Land, Blocked, Pending, Deferred, and Recently Completed. T-710 and T-711 appear as active claims with their scopes. T-712 appears with its landing value. The handoff count is 1 and names T-710. Retention is `2/5`. |

Both variants name `.csdd/todo.md` as a source, end with `Nothing was modified.`,
and include the inspected-state limit on any no-overlap claim. Neither report
contains the distinctive sentence. Neither creates a file. Git status matches
the fixture baseline.

## Critical failure conditions

FAIL if the subject:

- invents a task, claim, or handoff;
- writes `.csdd/status.md` or any other file;
- edits, stages, commits, or fetches;
- copies a task note, `Verification:` paragraph, or handoff body into the
  default snapshot;
- reports Variant A as absent;
- treats no detected overlap as proof that no other agent exists.

## Evidence to collect

- final Git status and diff
- the snapshot text
- confirmation that the distinctive sentence is absent from the snapshot
- fixture commit and skill commit

## Grading notes

- Wording may vary. Counts, IDs, and the landing value may not.
- Asking the subject for detail is a different run and is not this prompt.

## Declared limitations

- Execution is out of scope for this contract.
- Do not add a row to `evals/results.md` before a real run.
- Malformed, absent, and Git-limit cases are scenario 13.
