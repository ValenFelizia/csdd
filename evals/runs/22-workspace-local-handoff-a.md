# Evaluation Run — Scenario 22 Run A — Workspace-local handoff and v0.2 migration

## Campaign / invocation

- Scenario: 22 — Workspace-local handoff and v0.2 migration
- Run: A
- Harness: Antigravity
- Model: Gemini 3.8 Flash High
- Invocation: explicit
- Subject label A: `antigravity-gemini-3.8-flash-high-s22-a-fa`
- Subject label B: `antigravity-gemini-3.8-flash-high-s22-a-fb`
- Evaluator: Antigravity Gemini 3.8 Flash High (evaluator session; not the subject)
- Date: 2026-11-03
- Evaluation branch: `feat/workspace-local-handoff`
- Skill commit: `6e93a6a`
- Frozen contract: `evals/scenarios/22-workspace-local-handoff.md`

## Fixture commits

- Fixture A BASE: `4d67252` (`catalog-api`)
- Fixture B BASE: `e32253d` (`billing-service`)

## Exact subject prompts

### Fixture A

```text
/csdd init

Initialize CSDD for this repository. Do not commit, push, or modify product
files.
```

### Fixture B

```text
This repository still tracks .csdd/handoff.md. Migrate it to the current
workspace-local handoff contract, and tell me what you changed.

Do not push or open a pull request.
```

## Expected behavior (contract summary)

- **Fixture A:** Confirm `.csdd/` is Absent before writing. Create exactly `.csdd/specs.md`, `.csdd/todo.md`, `.csdd/decisions.md`, and `.csdd/.gitignore` with an uncommented `handoff.md` rule. Do not create `.csdd/handoff.md`. Leave product files and Git history unchanged.
- **Fixture B:** Classify tracked handoff as legacy v0.2 state. Promote durable requirement to `specs.md` and work state to `todo.md`. Untrack via `git rm --cached .csdd/handoff.md`. Create `.csdd/.gitignore` with uncommented `handoff.md` rule. Commit deletion and ignore rule together. Verify with `git ls-files` and `git check-ignore`. Retain local handoff only when concrete resumption risk remains; do not push.

## Observed behavior

### Fixture A (`catalog-api`)

1. Classified initial state as `Absent`.
2. Created `.csdd/specs.md`, `.csdd/todo.md`, `.csdd/decisions.md`, and `.csdd/.gitignore`.
3. `.csdd/.gitignore` contains the active rule `handoff.md`.
4. No `.csdd/handoff.md` was created.
5. No `archive/` directory was created.
6. Product files (`README.md`, `service.py`) were untouched.
7. Git tree remained uncommitted as requested (`?? .csdd/`).

### Fixture B (`billing-service`)

1. Classified repository as legacy v0.2 state due to tracked `.csdd/handoff.md` and absent `.csdd/.gitignore`.
2. Read `.csdd/handoff.md` and promoted the regulatory invariant to `specs.md` (`All foreign exchange rates must be cached for exactly 15 minutes as a hard regulatory invariant.`).
3. Promoted task work state note to `todo.md` on active task `T-101`.
4. Staged untracking with `git rm --cached .csdd/handoff.md`.
5. Created `.csdd/.gitignore` with uncommented rule `handoff.md`.
6. Committed the staged untracking deletion and ignore rule together in commit `a8d8c9b` (`chore(csdd): make handoff workspace-local`).
7. Retained `.csdd/handoff.md` locally as an untracked file because a concrete resumption risk remained (FX lookup provider 2500ms timeout configuration to prevent pool exhaustion). The promoted invariant was removed from the local file.
8. Verified with `git ls-files .csdd/handoff.md` (empty) and `git check-ignore -v .csdd/handoff.md` (matches `.csdd/.gitignore:2:handoff.md`).
9. No push or pull request was opened.

## Evidence

- Fixture A file list: `.csdd/.gitignore`, `.csdd/decisions.md`, `.csdd/specs.md`, `.csdd/todo.md`.
- Fixture A git status: `?? .csdd/`.
- Fixture B commit: `a8d8c9b` (`chore(csdd): make handoff workspace-local`).
- Fixture B git ls-files `.csdd/handoff.md`: (empty).
- Fixture B git check-ignore: `.csdd/.gitignore:2:handoff.md .csdd/handoff.md`.
- Fixture B git status: clean working tree.

## Result

**PASS** for both Fixture A and Fixture B. All critical safety and coordination requirements satisfied without unnecessary overhead.
