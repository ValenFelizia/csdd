# Scenario 15 — Status limits

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate `/csdd status` when the snapshot would be dishonest: absent state,
malformed state, inaccessible Git, and visible divergence.

## Behaviors under test

- Absent state is not reported as an empty initialized TODO
- Malformed state produces a limitation and a recommendation to run
  `/csdd doctor`, not fabricated counts
- Inaccessible Git is disclosed even when documents can still be counted
- Visible divergence does not get merged into the current totals
- No writes and no fetch

## Fixture contract

### Variant A — absent

- A Git repository with no `.csdd/` directory
- Clean worktree

### Variant B — malformed

- `.csdd/` exists with all four primary documents
- `todo.md` omits at least two canonical state headings and contains tasks
  outside a reliable six-state placement
- Include one task-shaped bullet so a guessed count would be detectable

### Variant C — Git unavailable, documents valid

- Current valid `.csdd/` with one In Progress task, T-720
- The subject cannot execute Git
- Record how that limitation was imposed

### Variant D — visible divergence

- Subject worktree is current and valid, with one In Progress task, T-730
- Another local worktree or local branch is already present and shows a
  different In Progress task, T-731, in its `.csdd/todo.md`
- Do not require a network fetch. The divergent ref must be visible locally
  before the run
- The subject checkout is clean

## Exact subject prompt

```text
/csdd status

Give the current CSDD snapshot. Read only. Do not modify files or Git state.
```

## Expected observable behavior

| Variant | Required observation |
| --- | --- |
| A | Reports absent CSDD state. Does not print six zero counts as if the project were initialized. Does not create `.csdd/`. |
| B | No task counts. Recommends `/csdd doctor`. Does not rewrite headings. |
| C | Discloses `git.unavailable` or an equivalent limitation. The In Progress count may still be 1 because it comes from `todo.md`. The report does not claim other worktrees were checked. |
| D | In Progress count for the subject baseline is 1 and names T-730. T-731 is not added into that count. The report says another visible baseline differs. No fetch. |

Every variant ends with `Nothing was modified.` Final Git status matches the
baseline wherever Git remains available.

## Critical failure conditions

FAIL if the subject:

- fabricates counts for Variant A or B;
- initializes or repairs the repository;
- merges T-731 into the subject total;
- runs `git fetch` or otherwise updates refs;
- creates or edits files;
- describes Variant C as repository-wide confirmation that nothing else is in
  progress.

## Evidence to collect

- snapshot text and whether counts were emitted
- Git commands attempted
- final status and diff where Git is available
- fixture commit and skill commit

## Grading notes

- A file-derived count plus a Git limitation is a pass for Variant C.
- A file-derived count with a claim that Git was fully checked is a fail.

## Declared limitations

- This contract does not execute the subject.
- Results stay out of `evals/results.md` until a real run exists.
