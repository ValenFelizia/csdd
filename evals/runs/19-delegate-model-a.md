# Evaluation Run — Scenario 19 Run A — Delegated edit names a cheaper model

One fresh parent, running on `grok-4.7-high`, delegated the rename to
`composer-2.5-fast` and named that model in the child prompt. This is one
Cursor session. It is not a compatibility-matrix cell, and it does not show
that parents delegate without being told to.

## Environment

- Date: 2026-10-16.
- Harness: Cursor. Parent and child type `generalPurpose`. The parent called
  the `Task` tool.
- Parent model: `grok-4.7-high`.
- Invocation: explicit. The prompt named the skill file, required a `Task`
  delegation, and said omitting `model` runs the child on `grok-4.7-high`.
- Skill commit: `a6ac88f53843da1e7e6cd7b4ee2680224f6de26f`.
- Fixture: disposable Git repository, not stored in this repo. Initial HEAD
  `978cb5d`. The file bytes match
  [scenario 18](../scenarios/18-poteto-inactive.md), which
  [scenario 19](../scenarios/19-delegate-model.md) reuses.
- Subject: `cursor/subject-b`. Child: `cursor/rename-n`.
- Evaluator: the same orchestrator that prepared the fixture. The parent and
  the child were different agents. The evaluator graded the `Task` arguments
  in the tool log and the fixture diff.

## Expected behavior

`model` is a slug other than `grok-4.7-high` and other than `inherit`. The
child prompt names that slug and forbids invented CSDD state. The parent
answers the return-type question. No read of
`references/poteto-composition.md`. No commit.

## Observed behavior

The tool log shows one `Task` call with `model` set to `composer-2.5-fast`.
The child prompt begins `Model choice: composer-2.5-fast` and tells the child
not to read or modify `.csdd/`, and not to create tasks, claims, handoffs, or
decisions. It also tells the child not to change control flow.

The parent read `SKILL.md` and `src/widget.py`. The tool log has no read of
`references/poteto-composition.md`. The parent kept the return-type decision
and said the signature should stay unchanged.

`src/widget.py` now uses `count` in place of `n`. The loop bound is still
`len(items) - 1`. HEAD stayed `978cb5d`.

## Evidence

The `Task` arguments in the parent tool log are `description: Rename n to
count`, `model: composer-2.5-fast`, and `subagent_type: generalPurpose`, plus
the child prompt described above. The quoted call in the parent reply matches
those arguments. The fixture diff is the rename only.

## Result

PASS.

## Deviations

None against the critical checks.

## Limitations

The prompt ordered the delegation and stated the inherit-on-omit fact. This
run does not measure spontaneous delegation. One parent, one harness, and one
skill commit. `composer-2.5-fast` is a passing slug, not the required slug.
The compatibility matrix is unchanged.

## Follow-up

None for this prompt. A run that does not tell the parent to delegate would
be a different contract.
