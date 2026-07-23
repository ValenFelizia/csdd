# T-027 Run — Codex — Fixture A

## Record template

```text
Date: 2026-07-23
OS / environment: Windows 11 (10.0.26200), AMD64
Harness / surface: Codex
Harness version: not user-visible
Model: not recorded
skills CLI version: 1.5.20
CSDD ref (exact): d2640af0641addb656cc8110fb445cae1b4694d3
Scope (global / project): global
Skill source mode: development checkout
Profile mode: live user profile
Fixture id / version: t027-a-catalog-init / v1
Fixture BASE commit / tree hash: BASE 6b632495f7e07623bc363ba629a5c24ab760dcbb / tree 823e63e6961a52f5e1474bb11dd77aff32e9bdb6
Exact invocation / prompt: Codex frozen $csdd init variant (see below)
Expected status: PASS (Fixture A Absent-only init; product/Git safety; empty operational TODO/handoff)
Observed behavior: see § Observed behavior
Result by dimension: see § Result by dimension
Limitations: see § Limitations
Modifications produced (paths only): .csdd/specs.md; .csdd/todo.md; .csdd/decisions.md; .csdd/handoff.md
Evidence path / attachment: campaigns/t027-manual-campaign-rematerialized/evals/runs/02-codex-fixture-a.md (+ .json)
```

## Campaign / subject

| Field | Value |
| --- | --- |
| Campaign dir | `C:\Users\Valen\Desktop\Vale\Proyectos\csdd skill\campaigns\t027-manual-campaign-rematerialized` |
| Subject | `t027-a-subject-codex` |
| Subject path | `...\t027-manual-campaign-rematerialized\t027-a-subject-codex` |
| Evaluator verification date | 2026-07-23 |
| Contract | `evidence/t-027-compatibility.md` (Fixture A rubric) |
| Preflight | `PREFLIGHT.md` / `PREFLIGHT.json` |

## Exact invocation / prompt

Frozen Codex variant:

```text
$csdd init

Initialize CSDD for this existing repository using only evidence that the
project actually supports. Preserve uncertainty and leave gaps when durable
intent is not established. Do not modify product code, commit, push, or create
any additional workflow.
```

## Post-run verification (evaluator; subject not re-executed)

| Check | Result |
| --- | --- |
| Branch | `main` |
| `HEAD` | `6b632495f7e07623bc363ba629a5c24ab760dcbb` (== Fixture A BASE) |
| `origin/main` | `6b632495f7e07623bc363ba629a5c24ab760dcbb` (== BASE) |
| `HEAD^{tree}` | `823e63e6961a52f5e1474bb11dd77aff32e9bdb6` |
| Tracked changes | none |
| Staged changes | none |
| Untracked files (exact) | `.csdd/specs.md`, `.csdd/todo.md`, `.csdd/decisions.md`, `.csdd/handoff.md` |
| `.csdd/archive/` | absent |
| Extra files / workflow | absent |
| Reflog | only `clone` entry; no subject commits or ref moves |
| Ahead/behind `origin/main` | `0 0` |
| Tests | `py -3.13 -m unittest discover -s tests -v` → `Ran 1 test` … `OK` (`test_list_names`) |

## Observed behavior

Factual Codex final response (no chain-of-thought; not a full transcript):

> Initialized CSDD at the repository root.
>
> Created: `.csdd/specs.md`, `.csdd/todo.md`, `.csdd/decisions.md`, `.csdd/handoff.md`
>
> Persisted README-backed requirements and the documented architecture decision. Tasks, invariants, and handoff remain empty due to insufficient durable evidence.
>
> Structure validated successfully. No product code, staging, commit, push, PR, migration, or workflow was added.

Observable durable state (evaluator inspection of subject files/Git):

1. Exactly four primary documents under `.csdd/`; archive absent.
2. Specs record the five README-accepted requirements and offline/no-network constraints, each cited to `README.md`; CSV note absent (not promoted).
3. Decisions record accepted DEC-001 (whole-document load) with evidence `docs/architecture.md`.
4. Todo has the six canonical H2 headings in order, `Retention: 5`, zero tasks.
5. Handoff has no active entry (template comment only).
6. Product tree and Git refs unchanged vs BASE; reflog still clone-only.

## Fixture A rubric

| Check | Pass signal | Result |
| --- | --- | --- |
| Absent-only write set | Exactly the four primaries under `.csdd/` | PASS |
| Product / Git safety | No tracked file changes; no commit/push | PASS |
| Evidence discipline | Specs/decisions only from authoritative fixture evidence | PASS |
| Uncertainty preserved | CSV note not promoted | PASS |
| TODO / handoff | Canonical empty operational state | PASS |

**Fixture A overall:** PASS

## Result by dimension

| Dimension | Status | Notes |
| --- | --- | --- |
| Global install via Agent Skills CLI | not tested | This run used an existing development checkout; does not change any inherited matrix cell for install |
| Discovery in a new session | not tested | Session opened on frozen explicit `$csdd init`; no separate discovery probe |
| Explicit invocation | verified | Frozen Codex `$csdd init` variant succeeded under recorded provenance |
| Implicit activation | not tested | Out of this campaign session |
| `/csdd init` or equivalent | verified | Fixture A PASS with complete required provenance for this claim |
| Representative workflow in an existing CSDD-aware project | not tested | Fixture B not executed in this record |
| Relevant Git / branch / worktree visibility | verified | Subject reported clean `main` / Absent `.csdd` at root; post-run inspection confirms `main`/`origin/main`/`HEAD` remain BASE |

## Limitations

- Skill source mode is `development checkout` on the live profile; this run does **not** prove CLI-managed copy → harness consumption.
- Codex harness version was not user-visible; model string was not recorded (not inferred).
- Discovery and implicit activation were not separately tested.
- Fixture B (existing-project workflow) is out of scope for this record.
- Global-install dimension remains unclaimed by this run (inherited matrix evidence may still be **partial** elsewhere; this record does not upgrade it).

## Modifications produced (paths only)

```text
.csdd/specs.md
.csdd/todo.md
.csdd/decisions.md
.csdd/handoff.md
```
