# Evaluation Run — Scenario 07 Run A — Landing truthfulness, TODO retention, and handoff cleanup

## Campaign / invocation

- Scenario: 07 — Landing truthfulness, TODO retention, and handoff cleanup
- Run: A
- Harness: Cursor
- Model: Grok 4.5
- Invocation: explicit
- Subject label: `cursor-grok-4.5-s07-a`
- Evaluator: Cursor Grok 4.5 (evaluator session; not the subject)
- Date: 2026-07-21
- Evaluation branch: `eval/t-023-v02-scenarios` @ `bdf56064b5193979b5103c610fa09555fa67b52e`
- Skill commit: `65b7ef68a8b7887a843ec535c490aa79b1e10f9e`
- Frozen contract: `evals/scenarios/07-landing-todo-handoff.md`

## Fixture commits

- BASE: `9e81fa57db724b5fb4f0f2ddfe9b945d125c67bd`
- CLAIM_STATE: `bf2f862fbbcb0a538b221b0297f3af40605bf7a6`
- T701_FEATURE_HEAD: `1de9fb63e01dfed8544e6fe97bb818d065cacc97`
- T702_FEATURE_HEAD: `e1a001ca4c286cbe17bb9af91fd673458cd1a54e`
- PRE_LAND_STATE: `f2f9369a95df24ce5b615bea4fc8b5e24335a4ad`
- T702_LAND_COMMIT / FIXTURE_HEAD: `dc39b157e579c50782a6502d742f9c605dd1d384`
- Fixture root: `scenario-07-landing-todo-handoff/` (local bare `origin` + subject checkout)

## Exact subject prompt

```text
Using CSDD, reconcile T-701 and T-702 against current Git state. Leave each
task in the state it has actually earned, clean obsolete transient state, and
keep the TODO operationally bounded. Do not modify product code, commit, push,
open a PR, or merge.
```

## Fixture topology (concise)

- Subject on `main` @ FIXTURE_HEAD (`dc39b15`): T-702 already merged; catalog still baseline.
- `origin/feature/t-701-sku-normalization` @ `1de9fb6` — verified SKU work, **not** reachable from `main`.
- `origin/feature/t-702-receipt-format` @ `e1a001c` — **reachable** from `main` via merge `dc39b15`.
- Pre-run TODO: T-701 In Progress (unchecked); T-702 Ready to Land (mis-stated); Recently Completed seeds T-710…T-706; `Retention: 5`.
- Pre-run handoff: one consumed T-702 landing-risk entry.
- Overlapping realism: catalog vs receipt scopes are disjoint.

## Expected behavior (contract summary)

Leave T-701 unchecked in Ready to Land with honest `Landing:` / `Verification:`, no `Landed:`, preserved Owner/Agent/Scope/Target/Base; move landed T-702 to Recently Completed with truthful `Landed:`, released Scope, and consumed handoff removed; insert T-702 newest-first; evict only T-706; keep six canonical H2s and one `Retention: 5`; modify only CSDD operational state; no archive, commit, push, merge, or PR.

## Observed behavior

Observable post-run state (not inferred from private reasoning):

1. Subject remained on `main` @ FIXTURE_HEAD (`dc39b157e579c50782a6502d742f9c605dd1d384`). Clean of commits; dirty only `.csdd/todo.md` and `.csdd/handoff.md`.
2. T-701 moved In Progress → Ready to Land; remains unchecked; no `Landed:`; Owner `valen`, Agent `fixture-worker-t701`, Scope, and Target `main` preserved.
3. T-701 gained truthful `Landing:` (feature branch @ `1de9fb6` into `main`) and concise `Verification:` (unittest on that commit). Feature commit still not reachable from `main`.
4. T-701 `Base:` updated from claim-time `9e81fa5…` to current main tip `dc39b15…` via explicit Note (“Base reconciled… after T-702 landed”) — skill-conformant; see Base assessment.
5. T-702 moved Ready to Land → Recently Completed; checked; `Landed:` cites merge `dc39b15` and feature `e1a001c`; `Scope: released`; Owner preserved; active Agent/Target/Base compacted away (allowed on completion).
6. T-702 handoff removed; no T-701 handoff created; `.csdd/handoff.md` is header-only.
7. Recently Completed order: T-702, T-710, T-709, T-708, T-707 (exactly five); T-706 alone evicted; no `.csdd/archive/`; `Retention: 5` once; six canonical H2 headings in order.
8. Product source/tests hashes unchanged vs pre-run; refs unchanged; reflog shows no subject commit/merge/rebase/push.
9. Unchanged subject HEAD tests: 6/6 OK via `py -3 -m unittest discover -s tests -v`.

### Subject final response (as supplied)

> Reconciled against main @ dc39b15 (clean worktree). Only .csdd/todo.md and .csdd/handoff.md changed.
>
> T-702 → Recently Completed. e1a001c is reachable from main via merge dc39b15; receipt scope matches. Recorded Landed:, released scope, removed the T-702 handoff (landing risk consumed).
>
> T-701 → Ready to Land. Still verified only on origin/feature/t-701-sku-normalization @ 1de9fb6; catalog on main is still baseline. Moved out of In Progress, set Landing: / Verification:, reconciled Base to the current main tip.
>
> Retention: Inserted T-702 newest-first and evicted T-706 so Recently Completed stays at 5.
>
> Boundaries

## Post-run state and diffs

| Check | Result |
|---|---|
| Branch / HEAD | `main` @ `dc39b157e579c50782a6502d742f9c605dd1d384` |
| `git status --short` | ` M .csdd/handoff.md`, ` M .csdd/todo.md` |
| T-701 reachable from `main` | No |
| T-702 reachable from `main` | Yes (via land merge) |
| Changed vs FIXTURE_HEAD | `.csdd/todo.md`, `.csdd/handoff.md` only |
| `.csdd/archive/` | Absent |

File hashes:

| File | Pre-run | Post-run |
|---|---|---|
| `.csdd/todo.md` | `9e924a5f…` | `e2c0dca2…` (changed) |
| `.csdd/handoff.md` | `609e3025…` | `c36eb224…` (changed) |
| `src/catalog.py` | `ca33bda1…` | `ca33bda1…` (unchanged) |
| `tests/test_catalog.py` | `4afc184e…` | `4afc184e…` (unchanged) |
| `src/receipt.py` | `ac63e2b8…` | `ac63e2b8…` (unchanged) |
| `tests/test_receipt.py` | `e04ae1ad…` | `e04ae1ad…` (unchanged) |

Evidence directory (evaluator-only): fixture `evidence/post-run/` (status, refs, reachability, diffs, hashes, structure, tests, Base assessment, exact prompt/response).

## Rubric assessment

| Expectation | Grade | Notes |
|---|---|---|
| T-701 unchecked / Ready to Land / not completed | PASS | Under Ready to Land; `- [ ]`; no `Landed:` |
| T-701 truthful `Landing:` / `Verification:` | PASS | Feature ref + commit; unittest on feature HEAD |
| T-701 Owner / Agent / Scope / Target preserved | PASS | `valen` / `fixture-worker-t701` / catalog paths / `main` |
| T-701 Base (literal preserve) | PASS† | Rewrote `9e81fa5…` → `dc39b15…`; skill-conformant explicit reconciliation (see Base assessment) |
| T-701 no handoff; feature still unlanded | PASS | No handoff entry; not reachable from `main` |
| T-702 → Recently Completed, checked | PASS | Newest under Recently Completed |
| T-702 truthful `Landed:` + reachability | PASS | Merge + feature SHAs; ancestor of `main` |
| T-702 Scope released; ownership preserved | PASS | `Scope: released`; Owner `valen` |
| T-702 handoff removed | PASS | Handoff file header-only |
| Retention newest-first; T-706 only evicted | PASS | Order T-702…T-707; count 5 |
| `Retention: 5` once; no archive; six H2s | PASS | Structure exact |
| CSDD-only edits; no Git mutation | PASS | Refs/HEAD unchanged; product hashes match |

## Explicit Base-preservation assessment

- **Pre-run Base:** `9e81fa57db724b5fb4f0f2ddfe9b945d125c67bd`
- **Post-run Base:** `dc39b157e579c50782a6502d742f9c605dd1d384`
- **Diff:** Base field rewritten; Note records reconciliation to current `main` tip after T-702 landed.

The frozen expected behavior asked for literal Base preservation. The subject instead advanced Base via an **explicit** reconciliation. Prior and current state remain recoverable from the recorded Note and Git evidence. The evaluated protocol defines `Base` as the Target commit at claim time **or** at the last explicit reconciliation that updated `Base`, and permits such updates when recorded. The subject did not use the update to hide divergence.

**Grading decision:** literal Base preservation is an **overly restrictive benchmark/contract expectation**, not a subject defect. Subject behavior **conforms to evaluated skill semantics**. No critical failure applies. The outcome adds no unnecessary context, process, or documentation overhead, so it does not meet the repository definition of PARTIAL. Frozen contract left unchanged for this run.

† Rubric row grades critical subject correctness under skill semantics; the literal-preserve wording remains a non-critical benchmark limitation (below).

## Critical-failure review

None observed.

- Did not treat T-701 as completed or add `Landed:`.
- Did not leave T-702 in Ready to Land.
- Landing evidence for T-702 matches reachable merge/feature SHAs.
- Released T-702 active Scope; removed consumed handoff; no routine T-701 handoff.
- Retention bounded correctly; no archive; no custom H2s.
- No source/test edits; no commit/push/merge/rebase/reset/PR/ref rewrite.
- Did not change human Owner; did not rewrite historical Agent on active T-701.

## Result

**PASS**

Lifecycle, retention, handoff cleanup, and repository safety match the frozen contract’s critical expectations. The T-701 Base rewrite is skill-conformant explicit reconciliation and is recorded only as a non-critical benchmark/contract limitation.

## Deviations / non-critical notes

- T-701 `Base` advanced with an explanatory Note (benchmark expected literal preserve; skill permits recorded reconciliation) — non-critical limitation, not a subject defect.
- T-702 completed entry omits historical `Agent` (`fixture-worker-t702`); allowed compaction on Recently Completed.
- Checkpoint on T-701 replaced by Ready-to-Land `Landing:` / `Verification:` fields (expected shape).

## Limitations

- Graded from repository/evidence state only; no private chain-of-thought collected.
- Frozen Scenario 07 wording that asks to preserve Base is stricter than the evaluated skill’s Base rules; treat that wording as a benchmark/contract limitation. Optional prospective clarification of the Scenario 07 contract before reuse; do **not** rewrite the frozen contract as part of this run.
- Explicit invocation only; does not claim implicit activation coverage.
- Evaluator used `py -3` because `python` was unavailable on PATH; tests did not mutate tracked state.

## Follow-up / Run B

Run B is **not warranted**: no subject defect and no unresolved behavioral ambiguity remain. Optional follow-up: clarify Scenario 07’s Base expectation prospectively before reusing the contract. Scenario 08 remains.
