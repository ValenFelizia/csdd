# CSDD Document Contracts

Status: Phase 0 conceptual draft

## Purpose

The four CSDD documents separate project state by purpose and lifetime. Their
contracts define what belongs in each document, when an agent should read or
update it, and how its contents age.

These contracts prevent CSDD from becoming a single large context dump.
Normative terms have the meanings defined in [protocol.md](protocol.md).

## Canonical layout

The four primary documents MUST be human-readable Markdown files at these exact
v0 paths:

```text
.csdd/
|-- specs.md
|-- todo.md
|-- decisions.md
|-- handoff.md
`-- archive/        # optional
```

Project-root alternatives and configurable locations are outside v0. In the
rest of this document, short names such as `todo.md` refer to these canonical
paths.

## Shared rules

1. Context hydration MUST NOT be unconditional. Load documents according to
   task need.
2. Prefer current, actionable state over chronological narration.
3. Persist consequential knowledge, not a transcript of activity.
4. Keep information in one canonical document and link to it when another
   document needs the context.
5. Update shared state when work makes it materially false, incomplete, or
   misleading.
6. Conflicts with repository evidence MUST be surfaced and reconciled; agents
   MUST NOT silently overwrite either side.
7. Keep sections scannable so agents can retrieve a relevant subset without
   reading the entire file.

## Document map

| Document | Primary question | Temperature | Expected lifetime |
| --- | --- | --- | --- |
| `.csdd/specs.md` | What must be true? | Warm | Durable, revised as project intent changes |
| `.csdd/todo.md` | What work exists now, and who is accountable and executing? | Hot | Current operational cycle |
| `.csdd/decisions.md` | What consequential choice was made, and why? | Warm | Durable until superseded |
| `.csdd/handoff.md` | What must a resuming agent know right now? | Hot | Transient, replaced or cleared frequently |

Projects MAY omit `.csdd/archive/`. When present, it is standardized cold
context, not a fifth primary document, and MUST NOT be read during default
hydration.

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

Describe the current operational state of work, including enough accountability,
execution, and scope information to coordinate agents.

`todo.md` is a live control surface, not a permanent project diary.

### Read policy

Agents MUST NOT knowingly ignore active scope overlap. Read relevant active work
before editing when a task is non-trivial, continues existing work, or may
overlap. A trivial or isolated task MAY avoid reading `todo.md` when overlap is
not plausible.

### Minimum task structure

CSDD tasks MUST use plain, human-readable Markdown. Each task requires:

- a stable task ID;
- a concise title;
- a state represented by its section or another obvious Markdown mechanism.

```markdown
## In Progress

- [ ] T-004 — Define document templates
```

For active collaborative work, tasks SHOULD include these fields when relevant:

- `Owner`: the accountable human or team and preferred coordination point;
- `Agent`: the current operational executor or harness/task label;
- `Scope`: the concrete write or contract boundary;
- `Updated`: the date of the last meaningful task-state update.

```markdown
- [ ] T-021 — Implement password recovery
  - Owner: valen
  - Agent: codex/auth-reset
  - Scope: `src/auth/reset-password/**`
  - Updated: 2026-07-12
```

`Depends on`, `Blocked by`, and a short `Note` MAY be added. Trivial tasks MAY
omit all ownership metadata. CSDD does not require story points, completion
percentages, mandatory priorities, risk scores, complex labels, redundant
timestamps, or mandatory reviewer fields. V0 MUST NOT require YAML front matter,
JSON, a database, a machine schema, or harness-specific metadata.

Changing `Agent` does not necessarily change `Owner`. Neither field provides
secure identity or authentication. CSDD v0 MUST NOT attempt automatic human
identity discovery and SHOULD use human-readable labels rather than
provider-specific identifiers.

### Contains

- pending, in-progress, and blocked work;
- ownership, execution, and active scope when coordination requires them;
- dependencies or blockers when relevant;
- a short note or completion condition when it materially helps execution;
- a small `Recently Completed` window when it helps interpret current state.

### Does not contain

- a full history of completed work;
- detailed implementation narration;
- architectural rationale;
- durable requirements;
- transient debugging notes unrelated to coordination;
- vague ownership scopes that prevent unrelated work;
- project-management metadata without a demonstrated coordination purpose.

### Update triggers

Update `todo.md` when:

- work is claimed or released;
- scope, `Owner`, `Agent`, state, dependency, or blocker changes;
- a meaningful checkpoint is needed to protect continuity;
- work completes or becomes abandoned;
- an active claim appears stale and is reconciled.

Do not add a task or claim for work whose coordination overhead would exceed its
complexity.

### Scope and coordination claims

`Scope` SHOULD name concrete files, directories, modules, or contracts. Prefer
paths such as `src/auth/**` and `tests/auth/**` over a vague label such as
`backend`. Scope is usually more important for collision detection than agent
identity.

Claims are advisory coordination metadata, not reliable distributed locks.
CSDD does not guarantee exclusive access, agent liveness, atomic claims,
automatic synchronization, or lease expiration. A single operational executor
per overlapping scope is the safe default, but intentional overlap is allowed
when it is surfaced and coordinated.

### Stale claims

A claim may be stale because execution ended, a human abandoned the task, work
completed without a CSDD update, the task moved environments, or repository
state changed independently. `Updated` is a reconciliation signal, not proof of
liveness or abandonment. V0 defines no strict time-based lease algorithm.

Before reclaiming scope, an agent SHOULD inspect relevant `todo.md` and
`handoff.md` entries, repository state, Git status and recent history, files in
scope, visible branches or worktrees, and current user instructions. When an
`Owner` exists and can reasonably be consulted, that human or team SHOULD be
the preferred coordination point.

A stale claim MAY be reclaimed after explicit reconciliation, but MUST NOT be
reclaimed silently. Update the task to record reassignment or the other
resolution.

```markdown
- [ ] T-042 — Migrate billing client
  - Owner: martina
  - Agent: codex/billing-migration
  - Scope: `src/billing/**`
  - Updated: 2026-07-12
  - Note: Agent execution reassigned after stale-state reconciliation.
```

### Aging and history

Keep active and near-term work hot. `todo.md` SHOULD retain only a small,
relevant window of completed work and remove older entries from the default
view. The exact bound remains a dogfooding question.

At the end of a meaningful phase or milestone, relevant history MAY be
distilled into an archive entry. Do not mechanically copy completed tasks.
Durable specifications MUST remain in `specs.md`, durable decisions MUST remain
in `decisions.md`, and current operational state MUST remain in `todo.md`.

### Update responsibility

The executing agent is responsible for keeping task state, `Agent`, scope, and
checkpoints honest. An agent that detects conflicting scope MUST surface the
conflict before changing the claim or overlapping code.

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

Agents MUST NOT silently reverse or erase a consequential accepted decision.
Add a superseding decision, link the previous entry, and state why the trade-off
changed.

If repository reality contradicts an active decision, the conflict MUST be
surfaced and reconciled as non-conforming code, a stale decision, an incomplete
migration, or another explicitly resolved state.

### Aging

Accepted decisions remain warm while active. Superseded decisions may move to
cold context when they no longer help current work, provided the active entry
retains enough lineage to prevent confusion.

### Update responsibility

The agent introducing or discovering a consequential change MUST record or
surface it. It MUST NOT manufacture rationale after the fact or silently
convert an implementation accident into project policy.

## `handoff.md`

### Contract

Transfer the minimum current state needed for another agent to resume
incomplete, blocked, or interrupted work safely.

V0 MUST use one canonical `.csdd/handoff.md`. It SHOULD be organized by task or
workstream rather than by agent or harness. It is a transient resume point, not
a collection of per-agent diaries. Multiple or scoped handoff files are outside
v0.

```markdown
# Handoff

## T-021 — Implement password recovery

### Current state

...

### Risks

...

### Recommended next step

...
```

### Read policy

Read the relevant task or workstream section when continuing prior work or when
an active task indicates that partial session state matters. Trivial or
unrelated work MAY avoid reading `handoff.md`.

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

At minimum, create or update a handoff when consequential incomplete state must
survive a session close, transfer, block, or interruption. Clear or replace a
section when it no longer describes current reality. Whether routine meaningful
checkpoints should also trigger updates remains open for dogfooding.

Relevant triggers include:

- unfinished work will continue in another session or agent;
- work becomes blocked or is interrupted with consequential partial state;
- a previous handoff is consumed and no longer describes current reality.

A successful self-contained task MAY omit a handoff unless another active agent
depends on its result.

### Relationship to `todo.md`

`todo.md` is the primary coordination and collision-prevention surface. It
answers what work is active, its state, `Owner`, `Agent`, explicit scope,
dependencies, and blockers. `handoff.md` transfers the partial implementation
state, current risks, unresolved questions, and recommended next action.

These responsibilities MUST remain distinct. `handoff.md` MUST NOT become a
duplicate task tracker or the primary collision-prevention mechanism.

When both refer to the same task, the handoff SHOULD link to the canonical task
entry rather than duplicate ownership fields. If they disagree, reconcile the
task state before continuing.

### Aging and replacement

Treat a handoff as replaceable current state. Remove or replace its task section
after the work is resumed, completed, abandoned, or made obsolete. Promote any
validated durable knowledge before removing the handoff.

Do not append every session forever. Selected semantic history MAY move to cold
context, but per-session handoffs MUST NOT accumulate as permanent history.

### Update responsibility

The agent leaving resumable partial work is responsible for recording an honest
checkpoint. The agent consuming the handoff is responsible for validating
critical claims and replacing or clearing stale transfer state.

## Cross-document movement

Information SHOULD move when its purpose or lifetime changes, not be copied
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

Projects MAY omit `.csdd/archive/`. When the archive exists, it is standardized
cold context and SHOULD contain `index.md`:

```text
.csdd/archive/
|-- index.md
|-- 2026-07-phase-0-protocol-design.md
`-- 2026-08-initial-skill-validation.md
```

The index SHOULD provide a concise inventory that helps agents select a relevant
entry without loading the archive broadly.

Agents MUST NOT load archive contents during default hydration. Entries SHOULD
be organized by meaningful phase, milestone, experiment, migration, or
workstream and MUST NOT be created for every agent session. A monolithic,
indefinitely growing `history.md` SHOULD NOT be used.

> Preserve semantic project history, not chronological activity exhaust.

An archive entry SHOULD summarize:

- its objective and relevant outcome;
- consequential discoveries;
- important rejected or deferred approaches;
- unresolved concerns;
- related decisions;
- useful task or Git references.

It SHOULD NOT preserve:

- complete transcripts or full agent reasoning;
- every command, failed attempt, or transient hypothesis;
- mechanical copies of `todo.md`;
- exact technical history already available in Git.

Archived state MUST be distinguishable from current authoritative state. When
lineage matters, entries SHOULD point to current specifications or decisions.
At phase or milestone boundaries, history MAY be distilled into an entry, but
durable and operational facts MUST remain in their canonical primary documents.

## Contract-level open questions

- Should `handoff.md` be updated only at session close or interruption, or also
  at meaningful checkpoints?
- Should the `Recently Completed` window in `todo.md` be bounded by relevance,
  phase, or a loose numeric guideline?
- Which `Agent` label conventions remain portable across Codex, Cursor, Claude
  Code, and future harnesses?
- Which normative statements should be promoted from SHOULD to MUST after
  real-world testing?
- Will one `.csdd/handoff.md` remain practical under concurrent editing?
- Does the archive model remain useful without becoming redundant with Git and
  durable project documents?
