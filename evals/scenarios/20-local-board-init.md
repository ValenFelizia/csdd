# Scenario 20 — Opt-in local board at init

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate Absent-only `/csdd init` when the utterance contains the local fence
line, so the patch is the three required documents plus an empty six-heading
`.csdd/todo.md`.

Companion to scenario 08, whose default creates no `todo.md`. External opt-in
is scenario 16.

## Applicability

**Local opt-in at init.** The prompt must contain a whole-line local fence
phrase. A paraphrase such as "use a local board" is not this contract.

## Behaviors under test

- Absent-only initialization after confirming no `.csdd` path exists
- One coherent patch of four files
- `.csdd/todo.md` copied from the local template: six state H2 headings in
  order, `Retention: 5`, no tasks, no `Mode: external`
- No invented tasks, owners, or an initialization self-task
- Handoff with no active entry; no archive
- Product files and Git history unchanged

## Fixture contract

Reuse the scenario 08 fixture shape: a small existing Git project, Absent
`.csdd/`, a README with durable truth, and a vague non-authoritative future
idea. Clean committed baseline. One unambiguous root.

### Subject start state

- Checked out on the fixture default branch at the clean baseline
- Clean worktree
- Installed CSDD skill at the recorded skill commit
- Destination confirms Absent before any write

## Exact subject prompt

Give the subject only the prepared fixture, the installed skill, and:

```text
/csdd init
/csdd todo enable local board

Initialize CSDD for this existing repository. Use only evidence the project
supports for specs and decisions. Do not invent tasks. Do not modify product
code, commit, push, or create any additional workflow.
```

Do not provide this scenario file or the evaluator rubric.

## Expected observable behavior

Evaluator-only. The subject should:

1. Resolve the Git root and confirm `.csdd/` is Absent.
2. Inspect repository evidence progressively.
3. Revalidate root and destination immediately before writing.
4. Create exactly `.csdd/specs.md`, `.csdd/decisions.md`, `.csdd/handoff.md`,
   and `.csdd/todo.md` in one patch.
5. Make `.csdd/todo.md` the empty local board: six canonical state H2 headings
   in order and `Retention: 5`.
6. Invent no tasks, owners, agents, or scopes.
7. Leave handoff with no active entry and create no archive.
8. Leave product files and Git history unchanged.
9. Report `task surface: local`.
10. Avoid commit, push, a pull request, or a merge.

## Critical failure conditions

FAIL if the subject:

- omits `.csdd/todo.md`;
- writes an external stub, or omits the six headings or `Retention: 5`;
- invents tasks or imports issues;
- creates anything other than those four documents under `.csdd/`;
- edits existing project files, or commits or publishes;
- writes the trio first and the board in a later step that can crash between
  them.

## Evidence to collect

- final Git status and diff
- contents of `.csdd/todo.md`
- list of created paths under `.csdd/`
- confirmation that product files and Git history are unchanged
- fixture commit and skill commit
- concise factual subject report

Do not collect private chain-of-thought.

## Grading notes

- Structural success does not require complete specifications.
- Subject input is fixture + skill + exact subject prompt only.
- Scenario 08 is the board-off default. This prompt's fence line is the
  difference.

## Declared limitations

- Fixture materialization and execution are out of scope for this contract.
- Results do not belong in `evals/results.md` until a real run is recorded.
