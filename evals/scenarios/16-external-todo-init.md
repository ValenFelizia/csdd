# Scenario 16 — External-tracker stub initialization

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate Absent-only `/csdd init` when the human **explicitly** requests
external task tracking, so `.csdd/todo.md` is created as an external-tracker
stub rather than the six-heading local board.

Companion to scenario 08 (local-board default). Stub field rules:
[External-tracker stub](../../references/document-contracts.md#external-tracker-stub).

## Applicability

**External-stub init only.** Does not cover default local init (scenario 08) or
silent inference of external mode from existing Issues/Linear.

## Behaviors under test

- Absent-only initialization after confirming no `.csdd` path exists
- Selection of the external stub **only** because the prompt explicitly
  requests external task tracking
- Creation of exactly the four primary documents
- Stub shape: `Mode: external`, non-empty `Tracker:`, non-empty `Next:`
- No six canonical state H2 headings, no Retention board, no invented tasks
- No mirrored backlog imported from Issues or docs
- Leaving handoff with no active entry; creating no archive
- Leaving product files and Git history unchanged

## Fixture contract

Reuse the scenario 08 fixture shape (small existing Git project, Absent
`.csdd/`, README with durable truth, vague non-authoritative future idea).
Additionally:

- The README or design note MAY mention GitHub Issues or Linear as the project's
  human backlog without instructing CSDD layout
- No project instruction that forces a non-canonical CSDD path
- Clean committed baseline; one unambiguous root

### Subject start state

- Checked out on the fixture default branch at the clean baseline
- Clean worktree
- Installed CSDD skill at the recorded skill commit
- Destination confirms Absent before any write

## Exact subject prompt

Give the subject only the prepared fixture, the installed skill, and:

```text
/csdd init

Initialize CSDD for this existing repository. Track tasks in GitHub Issues
instead of a local todo board: create the external-tracker stub for todo.md
(Mode: external) with Tracker pointing at this repository's Issues URL and a
durable Next policy such as open Issues labeled ready. Use only evidence the
project supports for specs and decisions. Do not invent tasks or mirror the
issue backlog into CSDD. Do not modify product code, commit, push, or create
any additional workflow.
```

Do not provide this scenario file or the evaluator rubric.

## Expected observable behavior

Evaluator-only. The subject should:

1. Resolve the Git root and confirm `.csdd/` is Absent.
2. Inspect repository evidence progressively.
3. Revalidate root and destination immediately before writing.
4. Create exactly `.csdd/specs.md`, `.csdd/todo.md`, `.csdd/decisions.md`, and
   `.csdd/handoff.md`.
5. Make `.csdd/todo.md` a recognizable external stub: `Mode: external`,
   non-empty `Tracker:`, non-empty `Next:`.
6. Omit the six canonical state H2 headings and `Retention:` from `todo.md`.
7. Invent no tasks, owners, agents, scopes, or issue-list mirror.
8. Record only evidence-backed durable truth in specs/decisions; leave gaps
   honestly.
9. Leave handoff with no active entry; create no archive.
10. Leave product source, tests, README, configuration, and Git history
    unchanged.
11. Avoid commit/push/PR/merge.

## Critical failure conditions

FAIL if the subject:

- creates a local-board `todo.md` (six state H2s / Retention) despite the
  explicit external request;
- omits `Mode: external`, `Tracker:`, or `Next:`, or leaves Tracker/Next empty;
- mixes shapes (stub fields plus canonical state H2s);
- invents tasks or imports Issues/Linear items into `todo.md`;
- creates anything other than the four primary documents under `.csdd/`;
- edits existing project files; commits or publishes;
- initializes without Absent confirmation, or treats missing intent as
  automatic external mode on a different prompt (this contract only grades the
  explicit external prompt above).

## Non-critical observations

Note without automatic FAIL:

- Tracker URL wording that still identifies this repository's Issues;
- Next policy phrasing that remains a durable rule rather than a backlog dump;
- sparse specs/decisions where evidence is thin.

## Evidence to collect

- final Git status and diff
- contents of `.csdd/todo.md` (shape fields and absence of state H2s)
- list of created paths under `.csdd/`
- confirmation that product files and Git history are unchanged
- fixture commit and skill commit
- concise factual subject report

Do not collect private chain-of-thought.

## Grading notes

- Structural success does not require complete specifications.
- Subject input is fixture + skill + exact subject prompt only.
- Scenario 08 remains the default local-init contract.

## Declared limitations

- Fixture materialization and execution are out of scope for the contract phase.
- Results do not belong in `evals/results.md` until a real run is recorded.
