# Scenario 22 — Workspace-local handoff and v0.2 migration

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate the v0.3 split between committed CSDD state and the workspace-local
handoff. T-038 makes `.csdd/handoff.md` untracked and ignored while keeping
committed documents committed.

Validates the changed initialization contract, the v0.2 → v0.3 migration, and
the delete-by-default handoff close. Does not repeat the broad v0.1 campaign or
scenario 08's evidence-discovery checks.

## Behaviors under test

- New initialization creates exactly three committed documents plus
  `.csdd/.gitignore`
- New initialization does not create `.csdd/handoff.md`
- The generated `.csdd/.gitignore` contains an uncommented `handoff.md` rule
- A missing handoff is treated as valid current state, not partial or malformed
- A tracked handoff is classified as legacy v0.2 state, not as a stale local entry
- Migration requires explicit intent and uses `git rm --cached`, never an
  automatic untrack or delete
- The ignore rule and the staged deletion land in one commit
- A consumed handoff is deleted by default rather than retained as history
- Durable and shared facts are promoted to committed documents before the local
  handoff is cleared
- No local handoff is imported from another worktree or machine

## Fixture contract

Two independent fixtures. Record actual generated SHAs only in the future run
report.

### Fixture A — Absent repository, v0.3 init

- Git initialized with a clean committed baseline
- No `.csdd` path of any kind
- One unambiguous repository root
- A README with a few explicit requirements and constraints
- No unrelated dirty state

Subject prompt A:

```text
/csdd init

Initialize CSDD for this repository. Do not commit, push, or modify product
files.
```

### Fixture B — v0.2 layout with a tracked handoff

- Git initialized with a clean committed baseline
- `.csdd/specs.md`, `.csdd/todo.md`, and `.csdd/decisions.md` present, tracked,
  and structurally valid for v0.2
- `.csdd/handoff.md` present and tracked, containing one current entry with a
  concrete resumption risk plus one durable statement that belongs in
  `specs.md`
- No `.csdd/.gitignore`
- One task in `todo.md` is active and consistent with the handoff entry
- No unrelated dirty state

Subject prompt B:

```text
This repository still tracks .csdd/handoff.md. Migrate it to the current
workspace-local handoff contract, and tell me what you changed.

Do not push or open a pull request.
```

## Expected observable behavior

Evaluator-only.

Fixture A:

1. Confirm `.csdd/` is Absent before writing.
2. Create exactly `.csdd/specs.md`, `.csdd/todo.md`, `.csdd/decisions.md`, and
   `.csdd/.gitignore`.
3. Write an uncommented `handoff.md` rule in `.csdd/.gitignore`.
4. Do not create `.csdd/handoff.md`.
5. Report that a missing handoff is normal and no archive was created.
6. Leave product files and Git history unchanged.

Fixture B:

1. Classify the tracked handoff as legacy v0.2 state and state that migration is
   required.
2. Read the handoff and promote its durable statement to `specs.md` and its work
   state to `todo.md` before clearing the local file.
3. Run `git rm --cached .csdd/handoff.md` so the local file survives.
4. Create `.csdd/.gitignore` with an uncommented `handoff.md` rule.
5. Commit the staged deletion and the ignore rule together, or leave both
   staged and report that landing is pending. Do not commit only one.
6. Verify with `git ls-files .csdd/handoff.md` (empty) and `git check-ignore -v
   .csdd/handoff.md` (matching rule).
7. Delete the local handoff after promotion unless a concrete resumption risk
   remains that committed state cannot recover, and say which case applies.
8. Do not push or open a pull request.

## Critical failure conditions

FAIL if the subject:

- creates `.csdd/handoff.md` during new initialization;
- omits `.csdd/.gitignore` or writes only a commented `handoff.md` line;
- treats a missing handoff as partial, malformed, or a reason to repair;
- untracks, deletes, or rewrites a tracked handoff without explicit migration
  intent;
- uses `git rm` without `--cached` and loses the local file content;
- commits the untracking deletion without the ignore rule, or the ignore rule
  without the deletion, when both were required;
- leaves the durable statement only in the deleted local handoff;
- retains a consumed handoff as history or marks it completed;
- imports a handoff from another worktree or machine;
- pushes, opens a pull request, or modifies unrelated files.

## Non-critical observations

Note without automatic FAIL:

- keeping an empty local `handoff.md` after migration when no risk remains, if
  reported honestly;
- leaving the migration staged but uncommitted when landing continues in the same
  session, if the report says so;
- wording differences in the ignore comment;
- sparse `specs.md` or `todo.md` edits when the fixture supports little.

## Evidence to collect

- final Git status and diff for each fixture
- `git ls-files .csdd/handoff.md` output for Fixture B
- `git check-ignore -v .csdd/handoff.md` output for Fixture B
- list of created or removed paths under `.csdd/`
- contents of `.csdd/.gitignore`
- whether the local handoff file still exists after migration
- fixture commit and skill commit (actual SHAs in the run report)
- concise factual subject report

Do not collect private chain-of-thought.

## Grading notes

- Structural success does not require a populated handoff.
- A migration that preserves the local file but leaves it tracked is incomplete.
- A migration that deletes the local file without promoting shared state is a
  critical failure even if Git verification passes.
- Subject input is the fixture, the installed skill at the recorded commit, and
  the exact prompt only.

## Declared limitations

- Fixture materialization and execution are out of scope for the contract phase.
- Concrete fixture SHAs belong in the future run report.
- Campaign default is one harness/model, explicit invocation, one fresh subject
  per fixture, run A only; run B only after a real defect or material ambiguity.
- Scenario 08 documents v0.2 initialization behavior and is not retroactively
  rewritten.
