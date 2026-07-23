# T-027 Run — Cursor — Fixture A

## Record template

```text
Date: 2026-07-22
OS / environment: Windows 11 (10.0.26200), AMD64
Harness / surface: Cursor
Harness version: 3.12.30 (63a2996a10d9e476b6c28e951dd7691d9c0cf480)
Model: not recorded
skills CLI version: 1.5.20
CSDD ref (exact): d2640af0641addb656cc8110fb445cae1b4694d3
Scope (global / project): global
Skill source mode: development checkout
Profile mode: live user profile
Fixture id / version: t027-a-catalog-init / v1
Fixture BASE commit / tree hash: BASE 6b632495f7e07623bc363ba629a5c24ab760dcbb / tree 823e63e6961a52f5e1474bb11dd77aff32e9bdb6
Exact invocation / prompt: Cursor frozen /csdd init variant (see below)
Expected status: PASS (Fixture A Absent-only init; product/Git safety; empty operational TODO/handoff)
Observed behavior: see § Observed behavior
Result by dimension: see § Result by dimension
Limitations: see § Limitations
Modifications produced (paths only): .csdd/specs.md; .csdd/todo.md; .csdd/decisions.md; .csdd/handoff.md
Evidence path / attachment: campaigns/t027-manual-campaign-rematerialized/evals/runs/01-cursor-fixture-a.md (+ .json)
```

## Campaign / subject

| Field | Value |
| --- | --- |
| Campaign dir | `C:\Users\Valen\Desktop\Vale\Proyectos\csdd skill\campaigns\t027-manual-campaign-rematerialized` |
| Subject | `t027-a-subject-cursor` |
| Subject path | `...\t027-manual-campaign-rematerialized\t027-a-subject-cursor` |
| Evaluator verification date | 2026-07-23 |
| Contract | `evidence/t-027-compatibility.md` (Fixture A rubric) |
| Preflight | `PREFLIGHT.md` / `PREFLIGHT.json` |

## Exact invocation / prompt

```text
/csdd init

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
| Reflog | only `clone` entry; no subject commits |
| Ahead/behind `origin/main` | `0 0` |
| Tests | `py -3.13 -m unittest discover -s tests -v` → `Ran 1 test` … `OK` (`test_list_names`) |

## Observed behavior

Factual subject final response (no chain-of-thought; not a full transcript):

> CSDD initialized at the worktree root. Structural adoption only — not complete project knowledge.
>
> **Root:** `C:/Users/Valen/Desktop/Vale/Proyectos/csdd skill/campaigns/t027-manual-campaign-rematerialized/t027-a-subject-cursor`
>
> **Created:** `.csdd/specs.md`, `.csdd/todo.md`, `.csdd/decisions.md`, `.csdd/handoff.md`
>
> **Evidence inspected:** `README.md`, `docs/architecture.md`, `src/catalog_cli.py`, `tests/test_catalog_cli.py`, `fixtures/catalog.json`, Git root/status (clean before init)
>
> **Persisted truth:** five accepted README requirements; offline/no-network constraints; `--path` / default path contract; DEC-001 whole-document load from `docs/architecture.md`
>
> **Left empty / not invented:** Invariants empty; todo operationally empty with `Retention: 5`; handoff with no active boundary; CSV export note left out (README marks it non-authoritative)
>
> **Gaps / uncertainty:** invalid-file / missing-field / exit-failure behavior not specified as durable intent; runtime validation of `id`/`name`/`category` not elevated beyond docs; DEC-001 date unknown; no packaging/CI/entry-point docs
>
> **Preserved:** only new untracked `.csdd/`; no product code edits, staging, commit, push, archive, or extra workflow

Observable durable state (evaluator inspection of subject files/Git):

1. Exactly four primary documents under `.csdd/`; archive absent.
2. Specs record the five README requirements and offline constraints; CSV not promoted.
3. Decisions record accepted DEC-001 (whole-document load) from architecture evidence; date marked unknown.
4. Todo has the six canonical H2 headings in order, `Retention: 5`, zero tasks.
5. Handoff has no active entry.
6. Product tree and Git refs unchanged vs BASE.

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
| Global install via Agent Skills CLI | not tested | This run used an existing development checkout; no installer mutation |
| Discovery in a new session | not tested | Session opened on frozen explicit `/csdd init`; no separate discovery probe |
| Explicit invocation | verified | Frozen Cursor `/csdd init` variant succeeded under recorded provenance |
| Implicit activation | not tested | Out of this campaign session |
| `/csdd init` | verified | Fixture A PASS with complete required provenance for this claim |
| Representative workflow in an existing CSDD-aware project | not tested | Fixture B not executed in this record |
| Relevant Git / branch / worktree visibility | verified | Subject observed Git root/status for Absent-only init; post-run `main`/`origin/main`/`HEAD` remain BASE |

## Limitations

- Skill source mode is `development checkout` on the live profile; this does **not** demonstrate CLI-managed copy → harness consumption.
- Model string was not user-visible / not recorded for the subject session.
- Discovery and implicit activation were not separately tested.
- Fixture B (existing-project workflow) is out of scope for this record.
- Global-install dimension remains unclaimed by this run.

## Modifications produced (paths only)

```text
.csdd/specs.md
.csdd/todo.md
.csdd/decisions.md
.csdd/handoff.md
```
