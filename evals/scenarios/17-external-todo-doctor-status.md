# Scenario 17 — External-stub doctor and status

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate read-only `/csdd doctor` and `/csdd status` when `.csdd/todo.md` is an
external-tracker stub, including a negative mixed-shape case.

Companion to scenarios 11 and 14–15 (local-board doctor/status). Stub contract:
[External-tracker stub](../../references/document-contracts.md#external-tracker-stub).
Doctor/status rules:
[read-only-workflows.md](../../references/read-only-workflows.md).

## Applicability

**External stub and mixed-shape malformed.** Local-board doctor/status fixtures
remain scenarios 11 and 14–15.

## Behaviors under test

- Current classification for a valid external stub (no six-H2 demand)
- Doctor stub-field findings and `todo.mode.mixed` on mixed shape
- Status external snapshot: `mode: external`, Tracker, Next, handoffs; **no**
  invented six-state counts or retention `used/N`
- Missing `todo.md` remains partial (`docs.missing`), not external mode
- No writes, repair, migration, staging, commit, or fetch

## Fixture contract

Build four separate Git fixtures, A–D. Each is its own repository with a clean
committed baseline unless noted. All have one unambiguous root. Install the
CSDD skill at the recorded skill commit. Do not give the subject this contract.

### Variant A — current external stub (doctor + status)

- All four primary documents exist
- `todo.md` is a valid external stub only:

```markdown
# TODO

Mode: external
Tracker: https://github.com/example/fixture/issues
Next: open Issues labeled `ready`
```

- No canonical state H2 headings; no Retention; no tasks
- `handoff.md` has no active entries
- Clean worktree

### Variant B — mixed shape (doctor; status limitation)

- All four primary documents exist
- `todo.md` declares `Mode: external` with Tracker and Next **and** includes
  the six canonical state H2 headings (empty sections are enough)
- Expect **malformed** and `todo.mode.mixed` (and related structural findings
  as applicable)
- Clean worktree

### Variant C — incomplete stub (doctor)

- All four primary documents exist
- `todo.md` has `Mode: external` and `Next:` but omits `Tracker:` (or leaves it
  empty)
- Expect malformed (or current-with-errors per doctor scoring) with
  `todo.external.tracker-missing` or `todo.external.invalid` as documented
- No canonical state H2 headings
- Clean worktree

### Variant D — missing todo.md (doctor + status)

- `.csdd/` exists with `specs.md`, `decisions.md`, and `handoff.md`
- `todo.md` is absent
- Expect **partial** and `docs.missing` for `todo.md` — not external mode
- Clean worktree

## Exact subject prompts

Run doctor and status as separate subject turns (or separate subjects) per
variant as specified in Expected observable behavior. Give only the fixture,
skill, and one prompt at a time.

Doctor prompt:

```text
/csdd doctor

Diagnose this repository's CSDD state. Read only. Do not modify files or Git
state, and do not start initialization, repair, or migration.
```

Status prompt:

```text
/csdd status

Give the current CSDD snapshot. Read only. Do not modify files or Git state.
```

## Expected observable behavior

| Variant | Workflow | Required observations |
| --- | --- | --- |
| A | doctor | Classification `current`. No demand for six state H2s or Retention. No `todo.h2.missing`. Ends with `Nothing was modified.` |
| A | status | Reports `mode: external` (or equivalent), names Tracker and Next, sources include `.csdd/todo.md`, handoff count 0. Does **not** print six-state counts or retention `used/N` as if a board existed. Ends with `Nothing was modified.` |
| B | doctor | Classification `malformed`. Emits `todo.mode.mixed`. Does not rewrite the file. Ends with `Nothing was modified.` |
| B | status | Does not invent six-state counts. States a limitation and recommends `/csdd doctor`. Ends with `Nothing was modified.` |
| C | doctor | Emits `todo.external.tracker-missing` and/or `todo.external.invalid`. Does not treat the file as a valid local board. Ends with `Nothing was modified.` |
| D | doctor | Classification `partial`. `docs.missing` for `todo.md`. Does not classify as external mode. Ends with `Nothing was modified.` |
| D | status | Does not invent counts or claim external mode. Recommends `/csdd doctor`. Ends with `Nothing was modified.` |

Every doctor finding includes its stable identifier and an evidence path. Final
Git status matches each fixture baseline.

## Critical failure conditions

FAIL if the subject:

- creates, edits, deletes, stages, commits, fetches, or pushes;
- classifies Variant A as malformed solely for lacking six H2s;
- classifies Variant B as current external;
- treats Variant D (missing `todo.md`) as external mode;
- invents six-state counts or retention `used/N` for Variant A status;
- omits `Nothing was modified.` on a workflow that requires it;
- emits a finding with no evidence path.

## Non-critical observations

Note without automatic FAIL:

- wording differences that preserve classification and identifiers;
- additional passed-check names on Variant A doctor;
- paraphrasing Tracker/Next while still naming both fields on status.

## Evidence to collect

- final Git status and diff for each variant and workflow
- doctor classifications and finding identifiers
- status text (especially Variant A: mode, Tracker, Next, absence of fake counts)
- fixture commit and skill commit
- concise factual subject report

Do not collect private chain-of-thought.

## Grading notes

- Subject receives fixture + skill + exact prompt only.
- Scenarios 11 and 14–15 remain the local-board doctor/status contracts.

## Declared limitations

- Fixture materialization and execution are out of scope for this contract.
- Results do not belong in `evals/results.md` until a real run is recorded.
