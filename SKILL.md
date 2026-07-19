---
name: csdd
description: Apply Collaborative Spec-Driven Development as a lightweight coordination and durable project-state protocol. Use when a repository contains canonical `.csdd/` project-state documents, making it CSDD-aware, or when the user or project instructions explicitly require CSDD.
---

# Collaborative Spec-Driven Development

Use CSDD as an operational router over the repository, its canonical `.csdd/`
state, and the detailed references. Load only the context needed to work safely.
CSDD externalizes coordination and durable truth; it does not provide shared
memory, authenticated identity, reliable locking, or automatic synchronization.

## Determine applicability

- Treat the existence of `.csdd/` as evidence that the repository is CSDD-aware.
  Expect the canonical project-state structure, but do not assume every task
  requires reading it.
- Apply CSDD when the user or project instructions explicitly require it, even
  when state is absent or malformed. Surface the condition, follow only the
  requested initialization or repair scope, and do not invent another layout.
- Do not silently initialize CSDD for unrelated work.
- Before hydrating CSDD state, inspect repository status, relevant project
instructions, the canonical `.csdd/` shape, and the task's apparent target.
Treat this as discovery, not permission to read every document.

## Choose the minimum hydration level

Classify by scope, risk, behavioral impact, ambiguity, dependencies, prior work,
and possible overlap. Increase the level when inspection reveals broader impact.

| Level | Use when | Read |
| --- | --- | --- |
| 0 — Direct | Work is explicitly bounded, local, low-risk, reversible, non-architectural, not behaviorally or contractually significant, independent of prior work, and unlikely to overlap active scope. | No CSDD state by default. |
| 1 — Local awareness | A localized change may plausibly overlap active work. | Only relevant active scope in `todo.md`. |
| 2 — Operational | A non-trivial bug, feature, integration, multi-file change, or continuation task. | Relevant `todo.md`; relevant `handoff.md` when boundary transfer state with concrete resumption risk may exist; applicable specifications and decisions. |
| 3 — Deep | Architecture, migration, broad refactor, cross-domain work, or material ambiguity. | Relevant hot and warm context; archive only for a concrete historical question. |

For detailed signals and semantics, load only [Adaptive context
hydration](references/protocol.md#adaptive-context-hydration).

### Take the trivial fast path

For Level 0, use:

```text
inspect target -> execute -> verify
```

Do not read CSDD state merely because `.csdd/` exists. Do not create a task,
claim ownership, update a handoff, create a decision, access the archive, or
modify CSDD state unless the work reveals a material conflict or changes durable
truth. Escalate hydration if the target proves broader or riskier than expected.

## Route reads by question

- Read relevant `.csdd/todo.md` entries for current work, ownership, scope,
  dependencies, and blockers.
- Read the relevant `.csdd/handoff.md` section when concrete resumption risk may
  exist; validate critical claims against the repository before relying on them.
- Read relevant `.csdd/specs.md` sections for requirements, constraints, invariants,
  intended behavior, and stable contracts.
- Read relevant `.csdd/decisions.md` entries for consequential accepted, rejected, or
  superseded directions.
- Read `.csdd/archive/` only as cold semantic history needed to answer a concrete
  historical question.

Prefer targeted sections and entries. Do not read every document fully by
default.

## Coordinate and claim non-trivial work

Before editing plausible shared scope:

1. Inspect relevant active tasks.
2. Compare the requested scope with active file, module, behavior, and contract
   scope. Recognize semantic overlap even when file patterns differ.
3. Surface known overlap. If overlap is intentional, make the boundaries or
   sequencing explicit and coordinate them.
4. Claim the task in `todo.md` when it is non-trivial and explicit scope reduces
   collision or continuity risk. Do not claim trivial isolated work.

Use a stable task ID, concise title, `Owner`, `Agent`, concrete `Scope`, and
`Updated` when useful. Add dependencies, blockers, or a short note only when
they improve coordination. Treat ownership as advisory, not as a distributed
lock. Reconcile questionable stale claims explicitly; never reclaim them
silently. For the authoritative procedures, consult [Concurrency
model](references/protocol.md#concurrency-model), [`todo.md` scope
claims](references/document-contracts.md#scope-and-coordination-claims), and
[stale claims](references/document-contracts.md#stale-claims).

### `todo.md` fast path

Keep `todo.md` under these fixed H2 headings, including when empty, in this
order: In Progress, Ready to Land, Blocked, Pending, Deferred, Recently
Completed. Do not invent, rename, reorder, alias, or omit state H2 headings.
Default presentation is flat; introduce H3 workstream grouping only when an
existing project convention or explicit human direction requires it.

Deferred requires authoritative intent plus `Reason:` and an observable
`Resume when:`; do not invent Deferred to park unfinished work. Recently
Completed declares `Retention: N` (fallback five), stays newest-first, and
compacts overflow in the same coherent patch—no subjective early removal, no
pinning, no mechanical archive. Ready to Land remains an unchecked active
task with honest claim metadata, `Landing:`, optional concise
`Verification:`, and no `Landed:` until the work is reachable from `Target`.

For full semantics, use [TODO structure and
retention](references/protocol.md#todo-structure-and-retention) and the
[`todo.md` contract](references/document-contracts.md#todomd).

When reclaiming stale work, preserve the existing human `Owner` unless the
user or an authoritative project instruction explicitly reassigns human
accountability. Reclaiming normally changes `Agent`, `Updated`, and relevant
coordination notes—not `Owner`.

Treat `Owner`, `Agent`, and `Scope` as distinct:

- `Owner` is the responsible human or team.
- `Agent` is the current operational executor.
- `Scope` identifies the active write boundary.

Reassigning or reclaiming agent execution MUST preserve the existing `Owner`
unless the user or authoritative project state explicitly transfers human
accountability.

Phase closure or task reconciliation MUST NOT retroactively replace historical
`Agent` metadata merely because a different agent verified or closed the work.
Update `Agent` only when that agent actually assumes execution of the task, or
when the project explicitly defines another convention.

Completed tasks MUST release or remove their active write scope. Use
`Scope: released` or omit claim metadata according to the project template.
A completed task MUST NOT continue to appear as an active write claim.

An agent reassignment MUST NOT silently change human ownership.

## Execute and persist proportionally

During non-trivial work:

- Stay within requested or claimed scope, and update the claim when scope
  changes materially.
- Validate assumptions against repository reality.
- Verify results in proportion to risk.
- Update `todo.md` when operational state materially changes.
- Persist only consequential knowledge; avoid activity logs and routine
  narration.
- Surface contradictions instead of silently choosing documentation or code.

Route persistence as follows:

- Update `todo.md` when task state, ownership, executor, material scope,
  dependencies, blockers, or a continuity-critical checkpoint changes.
- Update `handoff.md` only at a real execution boundary with concrete
  resumption risk—when a later agent or session would otherwise resume
  incorrectly, repeat meaningful work, miss a material risk, or overlook a
  blocking question. Do not update it for routine session closure,
  uninterrupted work, ordinary checkpoints, or live collisions coordinated in
  `todo.md`. Validate before relying; remove or replace when the risk is
  consumed. Keep state and collision coordination in `todo.md`.
- Update `specs.md` when intended behavior, a requirement, constraint,
  invariant, stable contract, or other durable project truth changes or is found
  incomplete or incorrect.
- Update `decisions.md` when a consequential direction is accepted, a rejected
  alternative has reusable rationale, or an existing decision is superseded.
  Do not manufacture rationale or turn implementation accidents into intent.

### Canonical durable truth

Persist each durable truth in one canonical document:

- behavioral requirements, constraints, and invariants belong in `specs.md`;
- accepted architectural or directional choices belong in `decisions.md`.

Do not duplicate a behavioral requirement in `decisions.md` unless the decision
adds independently useful durable rationale, alternatives, or consequences.
Prefer references between documents over restating the same truth.

## Reconcile conflicts

Reconcile conflicts among documentation, repository reality, current task
state, existing decisions, and active ownership. Neither Markdown nor code is
automatically correct. Inspect enough evidence to identify stale state,
incorrect implementation, or an incomplete transition.

If intent cannot be resolved safely, avoid expanding the conflict, mark the work
blocked when appropriate, and state the decision or clarification required. See
[Contradiction and reconciliation](references/protocol.md#contradiction-and-reconciliation)
for the full procedure.

### Branch and worktree state

Treat `.csdd/` as branch-local versioned state. The current worktree is the
operational baseline, not proof of repository-wide state.

Before claiming, reclaiming, or editing overlapping scope, inspect other
branches or worktrees only when concurrency, stale claims, overlap, or durable
truth could change the decision. Dirty files in a conflicting claimed scope are
strong evidence of live work; age alone is never proof.

Do not silently merge, copy, release, or overwrite divergent CSDD state. If
another worktree shows live conflicting work, or if `specs.md` or
`decisions.md` diverge materially, reconcile explicitly or block before
implementation. Record the source branch or commit when importing or
superseding CSDD state.

For the full Trigger → Discover → Compare → Classify → Reconcile or block →
Execute → Close procedure and divergence classes, see [Branch and worktree
baseline
reconciliation](references/protocol.md#branch-and-worktree-baseline-reconciliation).
Document-local evidence rules are in [Branch and worktree
locality](references/document-contracts.md#branch-and-worktree-locality).

## Close truthfully

- **Completed:** Verify the result, reconcile documentation and repository
  state, mark the task completed, release active scope, compact completed
  metadata, enforce Recently Completed retention, and remove obsolete
  handoff state. Create a handoff only when a separate active dependent
  workstream has its own concrete transfer risk.
- **Ready to Land:** Keep the task unchecked and active with honest claim
  metadata, `Landing:`, and concise `Verification:` when useful. Do not use
  `Landed:` until the changes are reachable from `Target`. Create a handoff
  only when those fields are insufficient for safe continuation.
- **Partial:** Keep the task honestly active, update its scope and checkpoint,
  and update the handoff only when both a boundary and concrete resumption risk
  exist.
- **Blocked:** Mark the task blocked, name the blocker or decision needed in
  `todo.md`, preserve consequential partial state in `handoff.md` only when
  concrete resumption risk exists, and narrow or release unnecessary scope.
- **Interrupted:** Leave an honest active checkpoint. Create a handoff only when
  concrete resumption risk must survive. Do not imply completion.
- **Trivial:** Verify the change and do not create CSDD state unless durable
  truth or a material conflict changed.

Keep implemented work awaiting required human review active with a concise
review note when completion has not yet been earned.

## Load detailed references progressively

Load only the section relevant to the current question:

- Use [the protocol](references/protocol.md) for principles, hydration semantics,
  lifecycle, boundary-driven handoffs, TODO structure and retention, concurrency,
  stale claims, branch/worktree baseline reconciliation, contradiction handling,
  archive policy, and validation scenarios.
- Use [the document contracts](references/document-contracts.md) for exact
  document boundaries, the detailed `todo.md` and `handoff.md` contracts, read
  and update triggers, aging and cleanup, cross-document movement, task and
  handoff structure, branch/worktree locality, and archive-entry guidance.

Do not load both references in full by default and do not reproduce their
detailed procedures in working notes.
