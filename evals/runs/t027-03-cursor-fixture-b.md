# T-027 Run — Cursor — Fixture B

## Record template

```text
Date: 2026-07-23
OS / environment: Windows 11 (10.0.26200), AMD64
Harness / surface: Cursor
Harness version: 3.12.30 (63a2996a10d9e476b6c28e951dd7691d9c0cf480)
Model: not recorded
skills CLI version: 1.5.20
CSDD ref (exact): d2640af0641addb656cc8110fb445cae1b4694d3
Scope (global / project): global
Skill source mode: development checkout
Profile mode: live user profile
Fixture id / version: t027-b-echo-loud / v1
Fixture BASE commit / tree hash: BASE 3b98043748c789cec5602d6f70d2769fff54f549 / tree 86fcbf6bce60f70fc577a17a6867c0bb1fe5a430
Exact invocation / prompt: Cursor frozen /csdd variant (see below)
Expected status: PASS (T-901 completed in write set; tests OK; TODO reconciled; no commit/push)
Observed behavior: see § Observed behavior
Result by dimension: see § Result by dimension
Limitations: see § Limitations
Modifications produced (paths only): src/echo_cli.py; .csdd/todo.md
Evidence path / attachment: campaigns/t027-manual-campaign-rematerialized/evals/runs/03-cursor-fixture-b.md (+ .json)
```

## Campaign / subject

| Field | Value |
| --- | --- |
| Campaign dir | `C:\Users\Valen\Desktop\Vale\Proyectos\csdd skill\campaigns\t027-manual-campaign-rematerialized` |
| Primary subject | `t027-b-subject-cursor` (`feature/t-901-loud-flag`) |
| Secondary worktree | `t027-b-subject-cursor-main` (`main`) |
| Evaluator verification date | 2026-07-23 |
| Contract | `evidence/t-027-compatibility.md` (Fixture B rubric) |
| Preflight | `PREFLIGHT.md` / `PREFLIGHT.json` |

## Exact invocation / prompt

```text
/csdd

Using CSDD, complete the pending bounded task T-901 recorded in .csdd/todo.md.
Reconcile against current Git and project state before editing. Stay inside
the allowed task write set: src/echo_cli.py and .csdd/todo.md. Do not modify
tests/test_echo_cli.py. Verify the result. Reconcile the TODO honestly. Do not
commit, push, merge, or rewrite existing branches.
```

## Post-run verification (evaluator; subjects not re-executed)

| Check | Result |
| --- | --- |
| Primary branch | `feature/t-901-loud-flag` |
| Primary `HEAD` | `3b98043748c789cec5602d6f70d2769fff54f549` (== Fixture B BASE) |
| Secondary branch | `main` |
| Secondary `HEAD` | `3b98043748c789cec5602d6f70d2769fff54f549` (== BASE) |
| `origin/main` | `3b98043748c789cec5602d6f70d2769fff54f549` (== BASE) |
| Committed tree | `86fcbf6bce60f70fc577a17a6867c0bb1fe5a430` |
| Tracked modified (primary, unstaged) | `src/echo_cli.py`, `.csdd/todo.md` only |
| Staged changes | none |
| Untracked files | none (after clearing incidental `__pycache__` bytecode from test runs) |
| `tests/test_echo_cli.py` SHA-256 | `a59acc75889368ae40decdfaf1674147b34802beb831e2ae6a8f6483b9236718` (intact) |
| Secondary worktree | completely clean |
| Refs / history | no subject commits, pushes, merges, or branch rewrites; primary reflog shows materialization checkout only |

### Behavior / tests

| Check | Result |
| --- | --- |
| `format_message(message, loud=False)` | returns message unchanged (`'hi'` → `'hi'`) |
| `format_message(message, loud=True)` | returns `message.upper()` (`'hi'` → `'HI'`) |
| `test_default_echo` | OK |
| `test_loud_uppercases` | OK |
| Suite | `py -3.13 -m unittest discover -s tests -v` → `Ran 2 tests` … `OK` |

### CSDD reconciliation

| Check | Result |
| --- | --- |
| T-901 active | no (not under In Progress / Pending / Ready to Land / Blocked / Deferred) |
| T-901 location | Recently Completed |
| Completion mark | `[x]` |
| Scope | `released` |
| Invented tasks / decisions / handoffs | none observed; handoff remains empty; specs/decisions unmodified vs HEAD |
| Write set | only `src/echo_cli.py` and `.csdd/todo.md` |

## Observed behavior

Factual subject final response (no chain-of-thought; not a full transcript):

> **T-901 is done.** `--loud` uppercases via `format_message`; both unit tests pass; TODO is reconciled. No commit/push.
>
> **Reconcile:** Branch `feature/t-901-loud-flag` @ `3b98043`; parallel `main` worktree at the same commit — no conflicting live claim; specs already required uppercase for `--loud`; no decision/handoff conflict.
>
> **Change (write set only):** `format_message` returns `message.upper()` when `loud=True`, otherwise the message unchanged.
>
> **Verify:** `test_default_echo` … ok; `test_loud_uppercases` … ok; OK.
>
> **TODO:** T-901 moved to **Recently Completed** with `Scope: released`. Uncommitted local edits: `src/echo_cli.py`, `.csdd/todo.md`.

## Fixture B rubric

| Check | Pass signal | Result |
| --- | --- | --- |
| CSDD applied | Relevant `.csdd/` read; T-901 completed honestly | PASS |
| Edit bound | Diff limited to `src/echo_cli.py` and `.csdd/todo.md`; tests unchanged | PASS |
| Verification | Original tests pass: default `"hi"` and loud `"HI"` | PASS |
| TODO honesty | T-901 in Recently Completed; Owner `valen`; Scope released | PASS |
| Git visibility | Branch, root, and extra `main` worktree identified | PASS |

**Fixture B overall:** PASS

## Result by dimension

| Dimension | Status | Notes |
| --- | --- | --- |
| Global install via Agent Skills CLI | not tested | Development checkout; this run does not claim install |
| Discovery in a new session | not tested | Explicit `/csdd` session; no separate discovery probe |
| Explicit invocation | verified | Frozen Cursor `/csdd` Fixture B variant succeeded under recorded provenance |
| Implicit activation | not tested | Out of this campaign session |
| `/csdd init` or equivalent | not tested | Fixture A territory; not this run |
| Representative workflow in an existing CSDD-aware project | verified | Fixture B PASS with complete required provenance for this claim |
| Relevant Git / branch / worktree visibility | verified | Subject reported feature branch + parallel `main` worktree; evaluator confirms both at BASE |

## Limitations

- Skill source mode is `development checkout` on the live profile; does not prove CLI-managed copy → harness consumption.
- Model string was not recorded for the subject session.
- Discovery, implicit activation, and `/csdd init` were not tested by this run.
- Global-install dimension remains unclaimed by this run.
- Incidental `__pycache__` bytecode from test execution was present at first evaluator inspection and cleared so the untracked set matches the product expectation (zero untracked); it was not part of the authorized write set.

## Modifications produced (paths only)

```text
src/echo_cli.py
.csdd/todo.md
```
