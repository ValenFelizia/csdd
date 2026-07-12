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
| 2 — Operational | A non-trivial bug, feature, integration, multi-file change, or continuation task. | Relevant `todo.md`; relevant `handoff.md` when partial state matters; applicable specifications and decisions. |
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
- Read the relevant `.csdd/handoff.md` section for consequential resumable partial
  state; validate it against the repository before relying on it.
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

When reclaiming stale work, preserve the existing human `Owner` unless the
user or an authoritative project instruction explicitly reassigns human
accountability. Reclaiming normally changes `Agent`, `Updated`, and relevant
coordination notes—not `Owner`.

Treat `Owner` and `Agent` as distinct:

- `Owner` is the responsible human or team.
- `Agent` is the current operational executor.

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
- Update `handoff.md` when another agent could otherwise resume incorrectly,
  repeat meaningful work, miss a current risk, or overlook a blocking question.
  Do not update it after every trivial session.
- Update `specs.md` when intended behavior, a requirement, constraint,
  invariant, stable contract, or other durable project truth changes or is found
  incomplete or incorrect.
- Update `decisions.md` when a consequential direction is accepted, a rejected
  alternative has reusable rationale, or an existing decision is superseded.
  Do not manufacture rationale or turn implementation accidents into intent.

## Reconcile conflicts

Reconcile conflicts among documentation, repository reality, current task
state, existing decisions, and active ownership. Neither Markdown nor code is
automatically correct. Inspect enough evidence to identify stale state,
incorrect implementation, or an incomplete transition.

If intent cannot be resolved safely, avoid expanding the conflict, mark the work
blocked when appropriate, and state the decision or clarification required. See
[Contradiction and reconciliation](references/protocol.md#contradiction-and-reconciliation)
for the full procedure.

## Close truthfully

- **Completed:** Verify the result, reconcile documentation and repository
  state, mark the task completed, release active scope, and remove obsolete
  handoff state. Create a handoff only when another active workstream needs
  non-obvious transfer state.
- **Partial:** Keep the task honestly active, update its scope and checkpoint,
  and update the handoff when resumption risk exists.
- **Blocked:** Mark the task blocked, name the blocker or decision needed,
  preserve consequential partial state, and narrow or release unnecessary
  scope.
- **Interrupted:** Leave an honest active checkpoint. Create a handoff only when
  meaningful partial state or risk must survive. Do not imply completion.
- **Trivial:** Verify the change and do not create CSDD state unless durable
  truth or a material conflict changed.

Keep implemented work awaiting required human review active with a concise
review note when completion has not yet been earned.

## Load detailed references progressively

Load only the section relevant to the current question:

- Use [the protocol](references/protocol.md) for principles, hydration semantics,
  lifecycle, concurrency, stale claims, contradiction handling, archive policy,
  and validation scenarios.
- Use [the document contracts](references/document-contracts.md) for exact
  document boundaries, read and update triggers, aging and cleanup,
  cross-document movement, task and handoff structure, and archive-entry
  guidance.

Do not load both references in full by default and do not reproduce their
detailed procedures in working notes.
