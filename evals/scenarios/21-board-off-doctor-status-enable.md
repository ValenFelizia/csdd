# Scenario 21 — Board-off doctor, status, and post-init enable

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate Current board-off doctor and status, then `/csdd todo enable` as the
only later writer of `.csdd/todo.md`.

The first observation must differ from scenario 14 variant A (empty board,
six counts of zero) and from scenario 17 variant A (`mode: external`).

## Applicability

**Current board-off, then enable.** The fixture starts with the three required
files and no `todo.md`. Variant A enables a local board. Variant B enables an
external stub. A later `/csdd init` writes nothing.

## Behaviors under test

- Doctor classification `current`, `task surface: board-off`, todo checks
  skipped because the surface is off, no `docs.missing` for `todo.md`
- Status `task surface: board-off`, handoff source, no `mode: external`, no
  six-state counts, no retention `used/N`
- Local enable writes only `.csdd/todo.md` from the local template
- External enable writes only the stub, with the utterance `Tracker:` and
  `Next:`
- `specs.md`, `decisions.md`, and `handoff.md` stay byte-identical
- A following `/csdd init` writes nothing
- No convert, no delete, no repair of an invalid path

## Fixture contract

Build two Git fixtures, A and B, from the same start. Each has one unambiguous
root and a clean committed baseline.

Start state for both:

- `.csdd/specs.md`, `.csdd/decisions.md`, and `.csdd/handoff.md` exist as files
- `.csdd/handoff.md` has no active entry
- `.csdd/todo.md` does not exist
- Record the bytes of the three files before any subject turn

Install the CSDD skill at the recorded skill commit. Do not give the subject
this contract.

## Exact subject prompts

Run the turns in order on each fixture. Give only the fixture, the skill, and
one prompt at a time.

Doctor:

```text
/csdd doctor

Diagnose this repository's CSDD state. Read only. Do not modify files or Git
state, and do not start initialization, repair, or migration.
```

Status:

```text
/csdd status

Give the current CSDD snapshot. Read only. Do not modify files or Git state.
```

Variant A enable:

```text
/csdd todo enable local board
```

Variant B enable:

```text
/csdd todo enable external stub
Tracker: https://github.com/example/fixture/issues
Next: open Issues labeled ready
```

After enable, on the same fixture:

```text
/csdd init

Initialize CSDD here if it is not already initialized.
```

## Expected observable behavior

| Turn | Required observations |
| --- | --- |
| Doctor, both variants | Classification `current`. `task surface: board-off`. No `docs.missing` for `todo.md`. Skip reason says the task surface is board-off. No `mode: external`. Ends with `Nothing was modified.` |
| Status, both variants | `task surface: board-off`. Sources include `.csdd/handoff.md` and do not require `.csdd/todo.md`. Handoff count 0. No six-state counts, no retention `used/N`, no `mode: external`. Ends with `Nothing was modified.` |
| Enable A | Creates only `.csdd/todo.md`. Six headings in order, `Retention: 5`, no tasks, no `Mode: external`. The other three files are byte-identical to the pre-turn bytes. |
| Enable B | Creates only `.csdd/todo.md` as a stub: `Mode: external`, the utterance `Tracker:`, the utterance `Next:`, no six headings. The other three files are byte-identical. |
| Later init | Writes nothing. Does not replace `todo.md`. Reports already initialized. |

## Critical failure conditions

FAIL if the subject:

- creates or edits a file during doctor or status;
- prints six zero counts on the board-off status (that is scenario 14 variant A);
- reports `mode: external` on the board-off turns (that is scenario 17 variant A);
- emits `docs.missing` for the absent `todo.md`;
- on enable, modifies `specs.md`, `decisions.md`, or `handoff.md`;
- on enable A, writes a stub, or omits the six headings or `Retention: 5`;
- on enable B, writes a local board;
- on the later init, creates or replaces any file;
- deletes a file.

## Evidence to collect

- doctor and status text for the board-off turns
- Git diff after enable, including a byte comparison of the three original files
- contents of `.csdd/todo.md` after enable
- Git status after the later init
- fixture commit and skill commit
- concise factual subject report

Do not collect private chain-of-thought.

## Grading notes

- Subject receives fixture + skill + one exact prompt at a time.
- Enable does not resurrect task text. This fixture never had a board, so the
  blank template is the expected file.

## Declared limitations

- Fixture materialization and execution are out of scope for this contract.
- Results do not belong in `evals/results.md` until a real run is recorded.
