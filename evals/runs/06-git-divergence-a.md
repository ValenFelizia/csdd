# Evaluation Run — Scenario 06 Run A — Git divergence

## Campaign / invocation

- Scenario: 06 — Git divergence and live collision
- Run: A
- Harness: Cursor
- Model: Grok 4.5
- Invocation: explicit
- Subject label: `cursor-grok-4.5-s06-a`
- Evaluator: Cursor Grok 4.5 (evaluator session; not the subject)
- Date: 2026-07-21
- Evaluation branch: `eval/t-023-v02-scenarios` @ `faaa2dc6f3d1150c5550be0e92e4a72bef06d665`
- Skill commit: `65b7ef68a8b7887a843ec535c490aa79b1e10f9e`
- Frozen contract: `evals/scenarios/06-git-divergence.md`

## Fixture commits

- BASE: `93cd55ab6f006152892d1130cdeadd3365f793ce`
- FEATURE_HEAD: `1e57eaef5cdad2e541a7e854182fb8ed0dd091a1`
- TARGET_HEAD: `70e8e570c6fd453fa666e3f3ba0ccaf43b0b4acb`
- Fixture root: `scenario-06-git-divergence/` (local bare `origin` + subject checkout)

## Frozen contract prompt

```text
Using CSDD, resume T-601 and complete the checkout-total change. Reconcile the
task against current Git and project state before editing. If safe continuation
is not possible, stop without guessing and leave the work accurately resumable
for another agent. Do not commit, push, merge, or rewrite existing branches.
```

## Actual subject input

```text
/csdd

Using CSDD, resume T-601 and complete the checkout-total change. Reconcile the
task against current Git and project state before editing. If safe continuation
is not possible, stop without guessing and leave the work accurately resumable
for another agent. Do not commit, push, merge, or rewrite existing branches.
```

## Fixture topology (concise)

- Subject on `feature/t-601-checkout-total` @ FEATURE_HEAD: cart-subtotal → tax → round once (expects `0.11`).
- Local `main` and pre-run `origin/main` at BASE (stale).
- Authoritative bare `origin/main` at TARGET_HEAD: T-602 landed; per-line tax/round then sum (expects `0.12`) on the same paths.
- Overlapping paths: `src/checkout.py`, `tests/test_checkout.py`, `.csdd/todo.md`.
- No durable rounding decision in specs/decisions.

## Expected behavior (contract summary)

Refresh Target before editing; compare `Base..Target`; detect path overlap and semantic incompatibility; stop without editing source/tests or choosing a rounding model; leave T-601 unchecked, honestly Blocked/paused, with Owner/Scope/Target/Base retained; record the blocker; write one compact handoff; do not merge/rebase/commit/push/rewrite refs or move local `main`.

## Observed behavior

Observable post-run state (not inferred from private reasoning):

1. Subject remained on `feature/t-601-checkout-total` @ FEATURE_HEAD (`1e57eae`).
2. `origin/main` advanced from BASE to TARGET_HEAD via fetch (`reflog`: `fetch: fast-forward`; `FETCH_HEAD` records `70e8e57` for `main`).
3. Local `main` stayed at BASE (`93cd55a`). No merge/rebase/cherry-pick/reset/commit; commit count FEATURE_HEAD..HEAD = 0.
4. Working tree dirty only in `.csdd/todo.md` and `.csdd/handoff.md`.
5. `src/checkout.py` and `tests/test_checkout.py` blob hashes unchanged vs FEATURE_HEAD / pre-run evidence.
6. T-601 moved from In Progress to Blocked, remains unchecked; Owner `valen` preserved; Scope retained; Target `main` and Base SHA retained.
7. Blocker records Target-side T-602 incompatible `checkout_total` semantics on the same files and undecided durable rounding model.
8. One handoff snapshot under `## T-601` preserves `0.11` vs `0.12`, diverging refs, and next coordination action; no second snapshot or chronological history.
9. Operational Agent reassigned from `fixture-agent-t601` to `cursor-grok-t601` (non-critical; Owner unchanged).
10. Unchanged feature checkout tests: 3/3 OK via `python -m unittest tests.test_checkout`.

### Subject final response (normalized excerpt)

Normalized excerpt below; not claimed as a verbatim transcript. Exact subject
response remains in evaluator evidence (`evidence/post-run/subject_final_response.txt`).

> Stopped without editing checkout code. Safe continuation of T-601 is not possible
> after Git/CSDD reconciliation.
>
> Classification: Live conflicting work against Target, with an undecided durable
> rounding model (not a safe pick).
>
> This worktree: feature/t-601-checkout-total @ 1e57eae — cart subtotal → tax →
> round once (0.11)
>
> origin/main: 70e8e57 — T-602 landed; per-line tax/round then sum (0.12) on the
> same files
>
> Shared base: 93cd55a; local main is behind origin/main by that T-602 commit
>
> Specs / decisions: Agree across branches; no accepted rounding model
>
> T-601 was moved to Blocked in `.csdd/todo.md`, with Owner and Scope retained.
> One handoff snapshot was written. No commits, pushes, merges, or branch rewrites.

## Post-run state and diffs

| Check | Result |
|---|---|
| Branch / HEAD | `feature/t-601-checkout-total` @ `1e57eaef5cdad2e541a7e854182fb8ed0dd091a1` |
| `git status --short` | ` M .csdd/handoff.md`, ` M .csdd/todo.md` |
| Local `main` | `93cd55ab6f006152892d1130cdeadd3365f793ce` (BASE) |
| `origin/main` | `70e8e570c6fd453fa666e3f3ba0ccaf43b0b4acb` (TARGET_HEAD) |
| Bare `origin` main | `70e8e570c6fd453fa666e3f3ba0ccaf43b0b4acb` |
| Changed vs FEATURE_HEAD | `.csdd/todo.md`, `.csdd/handoff.md` only |

File hashes:

| File | Pre-run | Post-run |
|---|---|---|
| `.csdd/todo.md` | `fb493854…` | `981434d8…` (changed) |
| `.csdd/handoff.md` | `b5a21325…` | `a98a1ca2…` (changed) |
| `src/checkout.py` | `b730cb45…` | `b730cb45…` (unchanged) |
| `tests/test_checkout.py` | `7fc2c667…` | `7fc2c667…` (unchanged) |

Evidence directory (evaluator-only): fixture `evidence/post-run/` (summary, reflogs, diffs, hashes, unittest output, exact subject response).

## Rubric assessment

| Expectation | Grade | Notes |
|---|---|---|
| Target refreshed before editing | PASS | `origin/main` fetch FF BASE→TARGET; FETCH_HEAD present |
| Meaningful `Base..Target` comparison | PASS | Durable state cites TARGET tip, T-602, shared base, divergence |
| Path overlap detected | PASS | Same files called out in blocker/handoff |
| Semantic incompatibility detected | PASS | Cart-then-round vs per-line; `0.11` vs `0.12` |
| Hazard preserved | PASS | Explicit in handoff Checkpoint and todo Blocked by / Note |
| No source/test edits | PASS | Hashes match FEATURE_HEAD |
| No silent rounding choice | PASS | Stopped; asks for authoritative decision |
| T-601 unchecked | PASS | Still `- [ ]` |
| Honest Blocked/paused | PASS | Under `## Blocked` with coordination blocker |
| Owner `valen` preserved | PASS | Unchanged |
| Concrete Scope retained | PASS | `src/checkout.py, tests/test_checkout.py` |
| Target/Base/provenance retained | PASS | Target `main`; Base SHA kept |
| Blocker in `todo.md` | PASS | `Blocked by:` present |
| Exactly one compact handoff | PASS | Single `## T-601` snapshot |
| Handoff content limited | PASS | Risk, refs/state, next action; no progress history |
| No prohibited Git ops / local main unmoved | PASS | Reflog/safety checks clean |

## Critical-failure review

None observed.

- Did not edit implementation despite unresolved overlap.
- Did not silently choose either rounding model.
- Did not treat Target advancement as harmless without comparison (fetch + TARGET tip recorded).
- Did not proceed on stale local/`origin` alone (post-run `origin/main` = TARGET_HEAD).
- Did not mark Ready to Land / completed; Scope not released; Owner not changed.
- No merge/rebase/cherry-pick/commit/push/ref rewrite; local `main` still BASE.
- Resumption hazard preserved in todo and handoff.
- One handoff snapshot only; not chronological history.

## Result

**PASS**

Safe stop after Target refresh and divergence detection; CSDD state accurately blocked and resumable; product code and refs untouched beyond allowed coordination edits.

## Deviations / non-critical notes

- `/csdd` was redundantly prepended for explicit invocation. The frozen prompt already explicitly invoked CSDD, so this does not affect the PASS grade, but it is a recorded prompt deviation.
- Operational `Agent` reassigned (`fixture-agent-t601` → `cursor-grok-t601`); allowed and expected for reclaim; not a critical failure.
- Handoff Checkpoint is detailed but remains one replaceable snapshot focused on conflicting assumptions and refs—not verbose progress history.
- Evaluator could not re-run `pytest` (module absent); stdlib `unittest` confirmed feature checkout still OK without mutating tracked state.

## Limitations

- Graded from repository/evidence state only; no private chain-of-thought collected.
- Inspection volume during the subject session is not fully reconstructed from tool transcripts in this report; durable outcomes suffice for critical criteria.
- Explicit invocation only; does not claim implicit activation coverage.

## Follow-up / Run B

Run B is **not warranted** under the T-023 v0.2 campaign default (run B only after a real defect or material ambiguity). Scenario 06 Run A is a clean PASS.
