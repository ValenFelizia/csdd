# CSDD Document Contracts

Status: Phase 0 conceptual draft

## Purpose

The four CSDD documents separate project state by purpose and lifetime. Their
contracts define what belongs in each document, when an agent should read or
update it, and how its contents age.

These contracts prevent CSDD from becoming a single large context dump.

## Shared rules

1. Load documents according to task need, never as an unconditional startup
   ritual.
2. Prefer current, actionable state over chronological narration.
3. Persist consequential knowledge, not a transcript of activity.
4. Keep information in one canonical document and link to it when another
   document needs the context.
5. Update shared state when work makes it materially false, incomplete, or
   misleading.
6. Reconcile conflicts with repository evidence; do not silently overwrite
   either side.
7. Keep sections scannable so agents can retrieve a relevant subset without
   reading the entire file.

## Document map

| Document | Primary question | Temperature | Expected lifetime |
| --- | --- | --- | --- |
| `specs.md` | What must be true? | Warm | Durable, revised as project intent changes |
| `todo.md` | What work exists now, and who owns it? | Hot | Current operational cycle |
| `decisions.md` | What consequential choice was made, and why? | Warm | Durable until superseded |
| `handoff.md` | What must the next agent know right now? | Hot | Transient, replaced or cleared frequently |

An optional `archive/` is cold context. It is not a fifth required document and
must not be read during default hydration.

## `specs.md`

### Contract

Describe the intended truth of the project: behavior, requirements, constraints,
invariants, and stable contracts.

### Read policy

Read only relevant sections when a task changes behavior, interprets intent,
touches a contract or invariant, or needs to distinguish desired state from
current implementation.

Do not require `specs.md` for a clearly isolated, non-behavioral edit.

### Contains

- expected user-visible or system behavior;
- functional and non-functional requirements;
- invariants and safety constraints;
- stable domain terminology;
- architectural or integration contracts that must remain true;
- explicit project policies, when the project has adopted them.

### Does not contain

- chronological work logs;
- task status, ownership, or blockers;
- temporary debugging hypotheses;
- rationale that belongs in `decisions.md`;
- a copy of implementation details discoverable directly from the repository;
- personal operator preferences unless adopted as project policy.

### Update triggers

Update `specs.md` when:

- requirements or intended behavior change;
- a new invariant or consequential constraint is validated;
- implementation work reveals that the documented intent was stale or
  incomplete;
- an accepted decision changes what the system must guarantee.

Do not update it merely because files were edited.

### Aging and reconciliation

Specifications are durable but mutable. When code and a specification disagree,
record or surface the contradiction and determine whether the implementation is
wrong, the specification is stale, or a transition is in progress.

Replace obsolete statements instead of keeping multiple active truths. Preserve
historical rationale in `decisions.md` or optional cold context only when it
remains consequential.

### Update responsibility

The agent whose work changes intended behavior or validates a missing constraint
is responsible for proposing or making the corresponding update. It must not
silently rewrite intent merely to match its implementation.

## `todo.md`

### Contract

Describe the current operational state of work, including enough ownership and
scope information to coordinate agents.

`todo.md` is a live control surface, not a permanent project diary.

### Read policy

Read relevant active work before editing when a task is non-trivial, continues
existing work, or may overlap with another agent. A trivial local task need not
read `todo.md` when overlap is not plausible.

### Contains

For each relevant task, include only the fields needed to act and coordinate:

- a stable short identifier or unambiguous title;
- status such as pending, in progress, or blocked;
- owner when work is claimed;
- explicit scope, preferably files, directories, modules, or contracts;
- dependencies or blocker when relevant;
- last meaningful checkpoint for active work;
- a concise completion condition when it is not obvious.

A bounded `Recently Completed` section may help humans and agents bridge the
current work cycle.

### Does not contain

- a full history of completed work;
- detailed implementation narration;
- architectural rationale;
- durable requirements;
- transient debugging notes unrelated to coordination;
- ownership scopes so broad that they prevent unrelated work.

### Update triggers

Update `todo.md` when:

- work is claimed or released;
- scope, owner, status, dependency, or blocker changes;
- a meaningful checkpoint is needed to protect continuity;
- work completes or becomes abandoned;
- an active claim appears stale and is reconciled.

Do not add a task or claim for work whose coordination overhead would exceed its
complexity.

### Ownership and stale claims

Ownership is an explicit soft lease:

- a single writer owns overlapping scope by default;
- overlap must be intentional and surfaced before editing;
- an owner must keep scope narrow enough to permit independent work;
- a last checkpoint helps later agents judge whether a claim may be stale;
- age alone does not automatically prove that a claim is abandoned.

CSDD v0 does not define a universal expiry interval. A questionable claim must
be reconciled, not silently ignored or treated as eternally active.

### Aging and history

Keep active and near-term work hot. Periodically remove completed entries from
the default view. Git remains the exact technical history; optional `archive/`
may retain concise semantic history when it would help explain prior phases or
abandoned directions.

The archive must remain cold and must not become required startup reading.

### Update responsibility

The agent performing the work is responsible for keeping its task status, scope,
and checkpoint honest. An agent that detects conflicting ownership must surface
the conflict before changing either the claim or the overlapping code.

## `decisions.md`

### Contract

Preserve consequential choices and the rationale needed to prevent repeated
debate or silent reversal.

### Read policy

Read relevant decisions before making an architectural, contractual, dependency,
or cross-cutting choice. Do not read the entire decision history for an isolated
implementation task.

### Contains

- a concise decision statement;
- status, including whether it has been superseded;
- rationale;
- rejected alternatives when remembering them prevents repeated work;
- important consequences or constraints;
- affected scope;
- date or sequence information sufficient to order superseding decisions.

### Does not contain

- every implementation choice;
- personal preference without project consequence;
- work status or task ownership;
- a meeting or chat transcript;
- speculative options with no decision;
- requirements better stated canonically in `specs.md`.

### Update triggers

Create or update an entry when:

- a consequential architectural or technical direction is accepted;
- an alternative is rejected for a reason future agents are likely to revisit;
- a prior decision is changed or superseded;
- new evidence materially changes the original rationale or consequences.

### Supersession and contradiction

Never erase a consequential accepted decision merely because a new agent prefers
another approach. Add a superseding decision, link the previous entry, and state
why the trade-off changed.

If repository reality contradicts an active decision, surface whether the code
is non-conforming, the decision is stale, or a migration is incomplete.

### Aging

Accepted decisions remain warm while active. Superseded decisions may move to
cold context when they no longer help current work, provided the active entry
retains enough lineage to prevent confusion.

### Update responsibility

The agent introducing or discovering a consequential change must record or
surface it. It must not manufacture rationale after the fact or silently convert
an implementation accident into project policy.

## `handoff.md`

### Contract

Transfer the minimum current state needed for another agent to resume
incomplete, blocked, or interrupted work safely.

`handoff.md` is a transient resume point. It complements `todo.md`; it does not
replace the task list, ownership record, or durable project documentation.

### Read policy

Read the relevant handoff when continuing prior work or when an active task
indicates that partial session state matters. Do not require it for unrelated
or clearly self-contained work.

A handoff is a claim about recent state, not proof that the repository is
unchanged. Confirm critical details before acting.

### Contains

- the task or scope being transferred;
- what materially changed or was attempted;
- the current partial state and last verified point;
- what remains to be done;
- blockers, risks, and unresolved questions;
- verification performed and important results;
- the recommended next action;
- references to canonical tasks, specifications, or decisions when needed.

Include exact commands, error text, or temporary hypotheses only when they are
necessary to resume efficiently and are not better captured elsewhere.

### Does not contain

- the canonical backlog, task ownership, or overlap model;
- a permanent chronological project history;
- full chat transcripts or reasoning traces;
- durable requirements or accepted architectural rationale;
- routine details another agent can cheaply rediscover;
- completed-session summaries with no continuing value.

### Update triggers

Create, replace, or update a handoff when:

- unfinished work will continue in another session or agent;
- work becomes blocked or is interrupted with consequential partial state;
- the current resume point, risk, or recommended next action changes;
- a previous handoff is consumed and no longer describes current reality.

A successful self-contained task needs no handoff unless another active agent
depends on its result.

### Relationship to `todo.md`

`todo.md` answers who owns current work, its explicit scope, status,
dependencies, and blockers. `handoff.md` answers what a resuming agent needs to
know about the latest partial execution state.

When both refer to the same task, the handoff should link to the canonical task
entry rather than duplicate ownership fields. If they disagree, reconcile the
task state before continuing.

### Aging and replacement

Treat a handoff as replaceable current state. Remove or replace it after the
work is resumed, completed, abandoned, or made obsolete. Promote any validated
durable knowledge before removing the handoff.

Do not append every session forever. If a project needs historical transfer
records, it may preserve selected summaries as optional cold context, but those
records are outside default hydration.

### Update responsibility

The agent leaving resumable partial work is responsible for recording an honest
checkpoint. The agent consuming the handoff is responsible for validating
critical claims and replacing or clearing stale transfer state.

## Cross-document movement

Information should move when its purpose or lifetime changes, not be copied
indefinitely.

| From | Trigger | Canonical destination |
| --- | --- | --- |
| Session notes | A finding is validated and must remain true | `specs.md` |
| Session notes | A consequential choice is accepted | `decisions.md` |
| Session notes | Work, scope, status, or blocker changes | `todo.md` |
| Session notes | Partial state must survive a session boundary | `handoff.md` |
| `handoff.md` | A temporary finding becomes durable | `specs.md` or `decisions.md` |
| `todo.md` | Work is no longer operationally relevant | Remove; optionally archive concise semantic history |
| `decisions.md` | A decision changes | Add explicit supersession; optionally move old detail to cold context |

Links may appear across documents, but one document should remain canonical for
each fact. When moving information, update or remove the stale source so it does
not continue presenting an old truth.

## Optional archive contract

An archive is an open design option, not a required CSDD v0 artifact. If a
project uses one, it should:

- contain selected semantic history whose future value justifies retention;
- remain outside default hydration;
- distinguish archived state from current authoritative state;
- point back to current specifications or decisions when lineage matters;
- avoid duplicating exact technical history already available in Git.

The path `.csdd/archive/` is illustrative, not yet normative. Archive structure,
retention thresholds, and indexing remain unresolved.

## Contract-level open questions

- Which fields, headings, or stable identifiers should v0 require versus merely
  recommend?
- Should document discovery assume a `.csdd/` directory, allow root-level files,
  or support both through project instructions?
- How much recent completion state belongs in hot `todo.md` before removal?
- Which evidence is sufficient to release or replace an apparently stale
  ownership claim?
- Should `handoff.md` represent one project-wide transfer point or support
  multiple scoped handoffs?
- When does superseded decision detail remain warm, and when should it move to
  optional cold context?
