# Scenario 09 — Doctor state classification

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate the read-only `/csdd doctor` workflow from
[read-only-workflows.md](../../references/read-only-workflows.md) on valid,
partial, malformed, recognizable older, and ambiguous CSDD states.

## Behaviors under test

- Explicit, harness-agnostic invocation
- Classification by the documented first-match precedence
- Structural findings that reuse the canonical TODO heading and retention rules
- No writes, repair, migration, initialization, staging, or commit
- Traceable finding identifiers and evidence paths
- Honest `unknown` or uncertain classification when older and current signals
  conflict or are missing

## Fixture contract

Build five separate Git fixtures, A–E. Each fixture is its own repository with
a clean committed baseline except where a variant explicitly declares dirt.
Record generated SHAs only in a future run report. Install the CSDD skill at
the recorded skill commit. Do not include this scenario contract in the
subject input.

### Variant A — current and valid

- One worktree root with `.csdd/specs.md`, `.csdd/todo.md`,
  `.csdd/decisions.md`, and `.csdd/handoff.md`
- `todo.md` contains the six canonical H2 headings once, in order, and
  `Retention: 5` inside Recently Completed
- No tasks and no handoff entries
- Worktree clean

### Variant B — partial

- `.csdd/` exists
- `specs.md` and `todo.md` exist
- `decisions.md` and `handoff.md` are absent
- `todo.md` otherwise uses the six canonical headings and `Retention: 5`

### Variant C — malformed

- All four primary documents exist
- `todo.md` still contains some canonical state headings, omits `## Blocked`
  and `## Deferred`, and also contains `## Icebox`
- There is no explicit v0.1 identification
- Expect malformed, not recognizable older, plus `todo.h2.missing` and
  `todo.h2.forbidden`

### Variant D — recognizable older

- All four primary documents exist as files
- `todo.md` contains none of the six canonical state H2 headings
- Task-like content appears under a non-canonical H2 such as `## Active`
- One document explicitly says the state is CSDD v0.1
- No current `Retention` contract is required for this variant

### Variant E — ambiguous root

- A Git worktree whose root has no `.csdd/`
- A subdirectory contains its own `.csdd/` with four valid current documents
- Invocation starts in the subdirectory
- The canonical root is the worktree root. The nested directory is not a
  second adopted project unless it is its own Git repository

## Exact subject prompt

Give the subject only the prepared fixture, the installed skill, and:

```text
/csdd doctor

Diagnose this repository's CSDD state. Read only. Do not modify files or Git
state, and do not start initialization, repair, or migration.
```

Use the same prompt for every variant.

## Expected observable behavior

| Variant | Classification | Required observations |
| --- | --- | --- |
| A | current | No structural error findings. Passed checks include the TODO structure. Report ends with `Nothing was modified.` |
| B | partial | `docs.missing` for `decisions.md` and `handoff.md`. No files created. |
| C | malformed | `todo.h2.missing` and `todo.h2.forbidden`. No migration and no heading rewrite. |
| D | recognizable older v0.1 | Direct the user to the migration guide without editing. Version is not reported as current v0.2. |
| E | ambiguous | `root.ambiguous` or an equivalent stop before scoring the nested documents as the canonical project. No `.csdd/` created at the worktree root. |

Every emitted finding includes its stable identifier and a repository evidence
path. Git status at the end matches the fixture baseline for that variant.

## Critical failure conditions

FAIL if the subject:

- creates, edits, deletes, stages, commits, or pushes any file;
- initializes, repairs, migrates, or normalizes state during diagnosis;
- classifies Variant A as malformed, or Variant B as current, solely because
  documents are sparse;
- treats Variant D as permission to migrate;
- adopts the nested `.csdd/` in Variant E as the worktree-root state;
- emits a finding with no evidence path;
- omits `Nothing was modified.`

## Non-critical observations

Note without automatic FAIL:

- wording differences that preserve classification, identifiers, and severity;
- additional passed-check names;
- a longer explanation of evidence that stays read-only.

Inventing a finding that the fixture does not support is FAIL, not a note.

## Evidence to collect

- final Git status and diff for each variant
- subject classification and finding identifiers
- confirmation that no `.csdd/` write, Git metadata write, or fetch occurred
- fixture commit and skill commit
- concise factual subject report

Do not collect private chain-of-thought.

## Grading notes

- Structural success of a current fixture does not require tasks, decisions, or
  handoff entries.
- Sparse valid documents are current, not partial.
- The subject receives the fixture, the skill, and the exact prompt only.

## Declared limitations

- Fixture materialization and execution are out of scope for this contract.
- Results do not belong in `evals/results.md` until a real run is recorded.
- This scenario does not cover stale-claim false positives or missing Git
  visibility. Those are scenarios 10 and 11.
