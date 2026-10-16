# Poteto composition

Follow this file only after
[When Poteto mode is active](../SKILL.md#when-poteto-mode-is-active) matches
the current session. If it does not match, stop. Do not apply the steps below.

Poteto mode owns orchestration, playbook selection, and per-role model choice.
CSDD owns durable project state. Do not add a scheduler or a required subagent
type. Do not override a Poteto role line, and do not record model slugs here.
When no orchestrator policy selected a model, follow
[Delegate with a fitting model](../SKILL.md#delegate-with-a-fitting-model).

## Keep playbook steps out of `todo.md`

Leave Poteto playbook steps in the session todolist. Do not copy them into
`.csdd/todo.md`. Task shape and retention stay in
[TODO structure and retention](protocol.md#todo-structure-and-retention).

## Hold one claim

The coordinating session holds one claim for the human-visible task. Set
`Agent` to that session.

Give a delegate its own claim only when the delegate takes a distinct write
scope that can collide with other work.

Do not change `Agent` when a delegate returns. Closure still must not rewrite
historical `Agent` metadata. See
[Scope and coordination claims](document-contracts.md#scope-and-coordination-claims)
and
[Historical Agent metadata](document-contracts.md#historical-agent-metadata).

## Do not write a handoff for a return

A delegate return is not a handoff. Update `handoff.md` only when the existing
trigger is met. See
[Boundary-driven handoffs](protocol.md#boundary-driven-handoffs) and
[Creation and update trigger](document-contracts.md#creation-and-update-trigger).

## Carry the constraint in the brief

A delegate may not load CSDD. Put these constraints in its brief:

- Stay inside the claimed scope.
- Do not initialize CSDD.
- Do not invent requirements, decisions, or tasks.
- Do not write `handoff.md` for the return.
- Do not copy or overwrite `.csdd/` across worktrees.

## Do not let autonomy invent durable state

Poteto autonomy covers reversible work inside the task. It does not authorize
`/csdd init` or invented durable truth. Initialization stays explicit and
Absent-only. See
[Initialization and adoption](protocol.md#initialization-and-adoption).

## Use the existing worktree rules

Follow
[Branch and worktree baseline reconciliation](protocol.md#branch-and-worktree-baseline-reconciliation).

## Leave CSDD prose in CSDD's voice

Poteto reply rules apply to the chat reply. Do not restyle `SKILL.md`,
`.csdd/` documents, or other CSDD prose to match them.

## Land with the existing shared-file rules

Shared `todo.md` integration stays on
[Write economy](document-contracts.md#write-economy) and
[Task-wise landing reconciliation](document-contracts.md#task-wise-landing-reconciliation).
That contention is
[issue 42](https://github.com/ValenFelizia/csdd/issues/42). Do not redesign it here.
