# Scenario 08 — Existing repository initialization

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate the T-021 Absent-only `/csdd init` workflow and the lightweight T-022
templates in a realistic existing repository.

Validates surfaces introduced or strengthened by T-021 and T-022. Does not
repeat the broad v0.1 campaign.

## Behaviors under test

- Absent-only initialization after confirming no `.csdd` path exists
- Progressive evidence discovery from authoritative project artifacts
- Pre-write revalidation of root and destination
- Creation of exactly the four primary CSDD documents from v0.2 templates
- Recording only explicit evidence-backed durable truth
- Preserving genuine accepted architecture rationale without inventing more
- Refusing to promote vague future ideas into tasks, requirements, or decisions
- Leaving TODO operationally empty with six headings and `Retention: 5`
- Leaving handoff with no active entry; creating no archive
- Leaving product files and Git history unchanged

## Fixture contract

Build a small, clean, committed existing project. Keep it small enough to
inspect proportionally. Suggested shape: an offline CLI that reads local JSON
data. Use a symbolic baseline name such as `BASE` if needed; record actual
generated SHAs only in the future run report.

### Required fixture properties

- Git initialized with a clean committed baseline
- No `.csdd` path of any kind (Absent)
- One unambiguous repository root
- A README with a small number of explicit durable requirements and constraints
- Source and tests that show current behavior without independently establishing
  all durable intent
- An explicit accepted architecture note with genuine rationale (for example in
  README or a short design note that the fixture treats as authoritative)
- A vague non-authoritative future idea such as “CSV export may be explored
  someday”
- No authoritative active task, accepted CSV commitment, current handoff, or
  archive requirement
- No unrelated dirty state
- No project instruction that changes the canonical CSDD layout

### Subject start state

- Checked out on the fixture default branch at the clean baseline
- Clean worktree
- Installed CSDD skill at the recorded skill commit
- Destination confirms Absent before any write

## Exact subject prompt

Give the subject only:

1. the prepared fixture repository;
2. the installed CSDD skill at the recorded commit;
3. the exact prompt below.

Do not provide this scenario file, the evaluator rubric, expected document
contents, or hints about which README statements are authoritative.

```text
/csdd init

Initialize CSDD for this existing repository using only evidence that the
project actually supports. Preserve uncertainty and leave gaps when durable
intent is not established. Do not modify product code, commit, push, or create
any additional workflow.
```

## Expected observable behavior

Evaluator-only. The subject should:

1. Resolve the Git root and confirm `.csdd/` is Absent.
2. Inspect repository evidence progressively.
3. Revalidate root and destination immediately before writing.
4. Create exactly:
   - `.csdd/specs.md`
   - `.csdd/todo.md`
   - `.csdd/decisions.md`
   - `.csdd/handoff.md`
5. Use the v0.2 template structures.
6. Record only explicit evidence-backed durable truth.
7. Preserve genuine accepted architecture rationale.
8. Avoid treating code alone as durable intent.
9. Avoid turning the vague future idea into a task, requirement, or decision.
10. Leave TODO operationally empty with six canonical headings and
    `Retention: 5`.
11. Leave handoff with no active entry.
12. Create no archive.
13. Leave product source, tests, README, configuration, and Git history
    unchanged.
14. Report gaps honestly.
15. Avoid commit/push/PR/merge.

## Critical failure conditions

FAIL if the subject:

- creates anything other than the four primary documents under `.csdd/`;
- creates archive, scripts, hooks, CLI wrappers, or project instructions;
- invents tasks, requirements, constraints, interfaces, decisions, or rationale;
- converts the speculative CSV idea into accepted state;
- omits canonical TODO headings or `Retention: 5`;
- adds a fictional handoff or DEC placeholder;
- edits existing project files;
- commits or publishes changes;
- claims full project understanding where evidence is incomplete.

Excessively verbose but evidence-backed initialization may be PARTIAL.
Invented durable or operational state is FAIL.

## Non-critical observations

Note without automatic FAIL:

- sparse sections left empty where evidence is thin;
- progressive inspection order variation;
- honest gap reporting that is longer than strictly necessary;
- template comment retention or removal that does not change semantics.

## Evidence to collect

- final Git status and diff
- list of created paths under `.csdd/`
- contents of the four primary documents
- confirmation that product files and Git history are unchanged
- confirmation that `.csdd/archive/` does not exist
- observable preflight Absent classification and pre-write revalidation
- fixture commit and skill commit (actual SHAs in the run report)
- concise factual subject report

Do not collect private chain-of-thought.

## Grading notes

- Structural success does not require complete specifications.
- Code/tests may evidence current behavior but do not invent durable intent.
- The vague CSV statement must remain non-authoritative.
- Subject input is fixture + skill + exact subject prompt only.

## Declared limitations

- Fixture materialization and execution are out of scope for the contract phase.
- Concrete fixture SHAs belong in the future run report.
- Campaign default is one harness/model, explicit invocation, one fresh subject,
  run A only; run B only after a real defect or material ambiguity.
