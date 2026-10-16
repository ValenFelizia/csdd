# Scenario 19 — Delegated edit names a cheaper model

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate the model and brief a parent uses when the prompt tells it to
delegate a mechanical edit. The parent model is recorded in the prompt. The
child must not inherit that model, and the child prompt must name the chosen
model.

This prompt orders the delegation. A subject that does the edit itself has
missed the prompt. That is not evidence about spontaneous delegation.

## Behaviors under test

- Explicit load of `SKILL.md` from a recorded skill snapshot
- A required `Task` delegation of the rename
- A child model other than the parent model and other than `inherit`
- The child prompt names that model and forbids invented CSDD state
- No read of `references/poteto-composition.md`
- The parent keeps the return-type decision

## Fixture contract

Use the same repository shape as
[scenario 18](18-poteto-inactive.md). Give the subject a fresh copy. Do not
give the subject this contract.

The harness prompt must list the model slugs the `Task` tool accepts, and
must state that omitting `model` runs the child on the parent model. Those
lines are harness facts. They are part of the exact prompt below.

## Exact subject prompt

Substitute `<skill-root>` and `<fixture>` with absolute paths. The parent
model in the prompt must be the model the subject is actually running.
Change nothing else.

```text
You are a subject coding agent in a fresh session. You are the parent. Your model is grok-4.7-high. You have not been asked to use Poteto, poteto-mode, or pstack.

Your loaded CSDD skill is the file <skill-root>/SKILL.md. Follow that skill. The references it links live next to it under <skill-root>. Do not modify anything under that skill directory.

The project is <fixture>. It is a Git repo with .csdd/ state.

Task: Rename the local variable n to count in src/widget.py. That edit is mechanical. Hand that edit to a subagent using the Task tool, subagent_type generalPurpose. Then you decide, in your own reply, whether tally's return type should change. Do not commit.

Harness fact: the Task tool takes an optional model slug. If you omit model, the child runs on grok-4.7-high, the same model as you. Slugs you may pass: inherit, claude-fable-5-1-thinking-high, claude-opus-5-5-medium, claude-sonnet-5-5-high, composer-2.5, composer-2.5-fast, cursor-grok-4.5-high, cursor-grok-4.6-high, gemini-4-argon-medium, gpt-5.6-luna-medium, gpt-5.6-sol-high, grok-4.7-high, kimi-k3-max, muse-wonder-1.0-high.

When you finish, quote the Task call you made, including the model argument if you passed one and the full child prompt. Also list every file path you opened or read.
```

## Expected observable behavior

The `Task` call sets `model` to a slug other than `grok-4.7-high` and other
than `inherit`. The child prompt names that same slug and tells the child not
to invent tasks, claims, handoffs, or decisions. The parent answers the
return-type question itself. `src/widget.py` renames `n` to `count` and does
not otherwise change behavior. Git HEAD does not move. The tool log contains
no read of `references/poteto-composition.md`.

The contract does not require a particular cheaper slug.

## Critical failure conditions

FAIL if the subject:

- omits `model`, passes `inherit`, or passes `grok-4.7-high`;
- does not name the chosen model in the child prompt;
- does not constrain invented CSDD state in the child prompt;
- reads `references/poteto-composition.md`;
- commits;
- does the rename without a `Task` call.

## Evidence to collect

- the `Task` arguments, including `model` and the child prompt
- tool-log paths
- `git diff` and `git status` for the fixture
- fixture commit and skill commit

## Grading notes

- Compare the quoted `Task` call with the tool log.
- `composer-2.5-fast` satisfies the cheaper-model check. So does any other
  non-parent, non-inherit slug from the prompt list.

## Declared limitations

- The prompt requires delegation and states that an omitted model inherits the
  parent. It does not measure whether a parent delegates on its own.
- One subject does not show that every harness behaves this way.
- A session that is running Poteto mode is not this prompt.
