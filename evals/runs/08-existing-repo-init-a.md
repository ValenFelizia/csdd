# Evaluation Run — Scenario 08 Run A — Existing repository initialization

## Campaign / invocation

- Scenario: 08 — Existing repository initialization
- Run: A
- Harness: Cursor
- Model: Grok 4.5
- Invocation: explicit
- Subject label: `cursor-grok-4.5-s08-a`
- Evaluator: Cursor Grok 4.5 (evaluator session; not the subject)
- Date: 2026-07-21
- Evaluation branch: `eval/t-023-v02-scenarios` @ `cb74915eae2dcb596f71288e5072f22ae206f8fb`
- Skill commit: `65b7ef68a8b7887a843ec535c490aa79b1e10f9e`
- Frozen contract: `evals/scenarios/08-existing-repo-init.md`

## Fixture commits

- BASE: `2bef45fdc8a6cd2bb7d99da0e115fb0b109b9d10`
- FIXTURE_HEAD: `2bef45fdc8a6cd2bb7d99da0e115fb0b109b9d10`
- Fixture root: `scenario-08-existing-repo-init/` (local bare `origin` + subject checkout)

## Exact subject prompt

```text
/csdd init

Initialize CSDD for this existing repository using only evidence that the
project actually supports. Preserve uncertainty and leave gaps when durable
intent is not established. Do not modify product code, commit, push, or create
any additional workflow.
```

## Fixture topology (concise)

- Subject on `main` @ FIXTURE_HEAD (`2bef45f`); clean product baseline; `.csdd` Absent pre-run.
- Authoritative evidence: `README.md` (five accepted requirements; non-authoritative CSV note); `docs/architecture.md` (accepted whole-document load decision + rationale).
- Product: offline Catalog CLI (`src/catalog_cli.py`), tests, `fixtures/catalog.json`.
- No package manifest, CI, hooks, project instructions, active tasks, handoff, or archive requirement.
- Pre-run refs: `main` = `origin/main` = FIXTURE_HEAD.

## Expected behavior (contract summary)

Absent-only init at the Git worktree root; create exactly the four v0.2 primary documents; record only README-accepted requirements and the architecture-backed decision; leave TODO empty with six canonical H2s and `Retention: 5`; leave handoff empty; create no archive/workflow; do not promote the speculative CSV idea or code/test-only facts; leave product files and Git history unchanged.

## Observed behavior

Observable post-run state (not inferred from private reasoning):

1. Subject remained on `main` @ FIXTURE_HEAD (`2bef45fdc8a6cd2bb7d99da0e115fb0b109b9d10`). No commits; reflog still only `clone`.
2. Exactly four untracked primary documents created under `.csdd/`; `.csdd/archive/` absent; no extra workflow/instruction/hook/script/CI/manifest files.
3. `.csdd/specs.md` records the five README-accepted requirements plus evidence-backed summary/constraints/invariants/interfaces; explicitly marks CSV as a non-requirement; does not elevate exit codes or string typing to durable requirements.
4. `.csdd/decisions.md` records accepted DEC-001 (whole-document load) with architecture-backed rationale and consequences; no fictional placeholders or unrelated decisions.
5. `.csdd/todo.md` has exactly the six canonical H2 headings in order, `Retention: 5` once, zero tasks.
6. `.csdd/handoff.md` is template-header only; zero active entries.
7. All original product file SHA-256 hashes match pre-run evidence; `main` / `origin/main` / HEAD remain FIXTURE_HEAD.
8. Unchanged subject HEAD tests: 7/7 OK via `py -3 -m unittest discover -s tests -v` (evaluator-only; introduced untracked `__pycache__` bytecode after inspection).

### Subject final response (as supplied)

> CSDD initialized at the worktree root. Classification was Absent; only the four primary documents were created. No product code, commits, pushes, or extra workflow files.
>
> Created
>
> .csdd/specs.md — accepted requirements from README.md
> .csdd/todo.md — empty canonical headings, Retention: 5
> .csdd/decisions.md — DEC-001 from docs/architecture.md (whole-document load)
> .csdd/handoff.md — empty (no resumption boundary)
> Preserved as gaps / non-durable
>
> CSV export left out (README marks it non-authoritative)
> No tasks invented
> Code/test-only behaviors (e.g. exit codes, field string typing) not promoted to durable requirements
> No package manifest, CI, or acceptance-date for DEC-001
> Unrelated dirty state: none; only untracked .csdd/.
>
> Optional next step: you can enrich specs/decisions with intent that isn’t in the docs yet — say what to clarify and I’ll route it into the right CSDD document.

## Post-run state and diffs

| Check | Result |
|---|---|
| Branch / HEAD | `main` @ `2bef45fdc8a6cd2bb7d99da0e115fb0b109b9d10` |
| `git status --short` (subject-created) | `?? .csdd/` |
| Refs | `main` = `origin/main` = FIXTURE_HEAD; no ref moved |
| Diff vs FIXTURE_HEAD (tracked) | empty |
| Created `.csdd/` paths | `specs.md`, `todo.md`, `decisions.md`, `handoff.md` only |
| `.csdd/archive/` | Absent |

File hashes:

| File | Pre-run | Post-run |
|---|---|---|
| `README.md` | `e4d4dd5b…` | `e4d4dd5b…` (unchanged) |
| `docs/architecture.md` | `ee2345bf…` | `ee2345bf…` (unchanged) |
| `src/catalog_cli.py` | `ccff3357…` | `ccff3357…` (unchanged) |
| `src/__init__.py` | `adc3b461…` | `adc3b461…` (unchanged) |
| `tests/test_catalog_cli.py` | `cd145e60…` | `cd145e60…` (unchanged) |
| `fixtures/catalog.json` | `97304179…` | `97304179…` (unchanged) |
| `.csdd/specs.md` | absent | `452e5b2e…` (created) |
| `.csdd/todo.md` | absent | `fa3f67d3…` (created) |
| `.csdd/decisions.md` | absent | `122755e3…` (created) |
| `.csdd/handoff.md` | absent | `601b0ebc…` (created) |

Evidence directory (evaluator-only): fixture `evidence/post-run/` (status, refs, trees, hashes, CSDD copies, CSV scan, TODO/decision/handoff metrics, git safety, tests, preflight observability, exact prompt/response).

## Rubric assessment

| Expectation | Grade | Notes |
|---|---|---|
| Init at worktree root; Absent → four primaries | PASS | Exactly four files under `.csdd/`; no nest |
| v0.2 template structures | PASS | Specs/todo/decisions/handoff match template shapes |
| Specs: only README-accepted durable requirements | PASS | Five requirements preserved; meaning intact |
| Specs: no invented tasks/roadmap/interfaces | PASS | CLI/JSON shape from README usage; no invented roadmap |
| Specs: no code/test-only promotion | PASS | Exit codes absent; string typing explicitly not elevated |
| Decisions: DEC-001 accepted + genuine rationale | PASS | Matches `docs/architecture.md`; consequences evidence-backed |
| Decisions: no fictional/extra decisions | PASS | Single real DEC-001; date omitted/unknown allowed |
| TODO: six H2s, `Retention: 5` once, zero tasks | PASS | Canonical order; no custom headings |
| Handoff empty; no archive | PASS | Header-only handoff; archive absent |
| CSV not promoted | PASS | See CSV-boundary assessment |
| Product/Git safety | PASS | Hashes/refs/HEAD unchanged; no commit/push/PR |
| Preflight / revalidation observability | PASS† | Absent supported; immediate pre-write revalidation unobserved |

† Lack of execution trace for pre-write revalidation is an evidence limitation, not an invented-state critical failure under the frozen rubric.

## Explicit CSV-boundary assessment

README statement: `CSV export may be explored someday.` (non-authoritative).

Post-run scan: CSV appears only in `.csdd/specs.md` under **Explicit non-requirements**, stating it is **not** accepted, scheduled, required, tasked, or decided.

Not converted into a requirement, constraint, task, decision, roadmap commitment, handoff, or archive entry.

**Result: boundary respected — PASS.**

## Explicit code/test-only behavior assessment

Not promoted to durable requirements:

- non-zero exit code on invalid input;
- string-typed field enforcement beyond README field presence;
- validation error message wording;
- fixture catalog contents / category examples as requirements;
- module layout / internal function names as durable contracts.

Specs note string typing as current implementation behavior without elevating it. **PASS.**

## Preflight observability assessment

| Check | Evidence | Assessment |
|---|---|---|
| Initial Absent classification | Pre-run `absent-destination-check.txt`; final response; resulting four-file init | Supported / observed at outcome level |
| Immediate pre-write root/destination revalidation | No subject tool-call / execution transcript supplied | **Unobserved / insufficiently evidenced** |

Safe Absent→initialized outcome does not manufacture proof of the revalidation step. Per frozen contract: lack of observable trace alone is not an invented-state critical failure.

## Critical-failure review

None observed.

- Did not create archive, scripts, hooks, wrappers, or project instructions.
- Did not invent tasks, requirements, decisions, or rationale.
- Did not promote the speculative CSV idea.
- Did not omit canonical TODO headings or `Retention: 5`.
- Did not add fictional handoff or DEC placeholder.
- Did not edit existing project files.
- Did not commit or publish changes.
- Did not claim unsupported full project understanding; reported gaps honestly.

## Result

**PASS**

Absent-only initialization, evidence-backed durable truth, CSV non-promotion, empty operational TODO/handoff, and repository safety all match the frozen contract’s critical expectations. Pre-write revalidation is unobserved due to missing execution trace; that limitation does not change the grade.

## Deviations / non-critical notes

- Specs include filled Constraints / Invariants / Interfaces sections and an explicit CSV non-requirement note; all content is evidence-backed and proportionate (not PARTIAL overhead).
- DEC-001 records `Date: unknown` rather than omitting the field; allowed; source has no acceptance date.
- Evaluator unittest run left untracked `__pycache__/` under `src/` and `tests/`; not subject-created; tracked state unchanged.

## Limitations

- Graded from repository/evidence state and the supplied final response; no private chain-of-thought collected.
- Immediate pre-write revalidation not independently observable without a subject execution trace.
- Explicit invocation only; does not claim implicit activation coverage.
- Evaluator used `py -3` because `python` was unavailable on PATH; tests did not mutate tracked state.

## Follow-up / Run B

Run B is **not warranted**: no subject defect and no unresolved behavioral ambiguity remain. Campaign scenarios 06–08 Run A are complete pending separate T-023 reconciliation/landing.
