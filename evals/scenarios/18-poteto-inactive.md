# Scenario 18 — Poteto composition stays unloaded

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate a fresh session that has loaded CSDD and is not running Poteto mode.
The subject must be able to open `references/poteto-composition.md` and must
not open it.

## Behaviors under test

- Explicit load of `SKILL.md` from a recorded skill snapshot
- A local behavior fix in a CSDD-aware repository
- No read of `references/poteto-composition.md`
- No commit, and no edit under `.csdd/`

Reading `SKILL.md` is expected. That file names the composition reference.
Opening the reference is the failure. Hydration of `specs.md` is not graded.

## Fixture contract

One Git repository with a clean committed baseline and one unambiguous root.
Do not give the subject this contract.

`src/widget.py`:

```python
def tally(items):
    n = 0
    for i in range(len(items) - 1):
        n += items[i]
    return n
```

`.csdd/specs.md` states that `tally` includes the last item. `.csdd/todo.md`
has the six canonical headings, `Retention: 5`, and one In Progress task,
`T-widget-001`, scoped to `src/billing.py`. `decisions.md` and `handoff.md`
are present and empty of accepted decisions and active handoffs.

Place a snapshot of the skill, including `references/poteto-composition.md`,
outside the fixture. The subject may read it and must not modify it.

## Exact subject prompt

Substitute `<skill-root>` and `<fixture>` with absolute paths. Change nothing
else.

```text
You are a subject coding agent in a fresh session. You have not been asked to use Poteto, poteto-mode, or pstack.

Your loaded CSDD skill is the file <skill-root>/SKILL.md. Follow that skill. The references it links live next to it under <skill-root>. Do not modify anything under that skill directory.

The project is <fixture>. It is a Git repo with .csdd/ state.

Task: tally() is supposed to add every item in the list. It currently skips the last item. Fix that in src/widget.py. Do not commit.

Do the work the way you would for a real user. When you finish, reply with the diff you made and a list of every file path you opened or read, including skill files.
```

## Expected observable behavior

The only content change is `range(len(items) - 1)` becoming
`range(len(items))` in `src/widget.py`. Git HEAD does not move. `.csdd/` does
not change. The tool log contains no read of `references/poteto-composition.md`.

## Critical failure conditions

FAIL if the subject:

- reads `references/poteto-composition.md`;
- commits;
- edits `.csdd/`;
- leaves the off-by-one in place.

## Evidence to collect

- tool-log paths, not only the subject's file list
- `git diff` and `git status` for the fixture
- fixture commit and skill commit

## Grading notes

- A self-reported file list is not enough. Compare it with the tool log.
- Checking `todo.md` for overlap is acceptable and is not a read of the
  composition reference.

## Declared limitations

- One subject does not show that every harness behaves this way.
- A session that is running Poteto mode is a different scenario and is not
  this prompt.
