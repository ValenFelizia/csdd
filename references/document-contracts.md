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

### Shared coordination surfaces

`.csdd/todo.md` and `.csdd/handoff.md` are shared coordination surfaces, not a
task's principal write `Scope` by default.

When editing either document:

1. re-read the current file before changing it;
2. check for concurrent or intervening changes;
3. apply the smallest patch that updates the relevant entry or section;
4. preserve unrelated entries and sections;
5. surface conflicts instead of overwriting them; and
6. do not automatically add these files to a task's principal `Scope` unless the
   task explicitly claims them.

Git-aware field semantics (`Target`, `Base`, `Landed`), refresh checkpoints, the
minimal Git contract, and landing examples live in [Git-aware task
lifecycle](protocol.md#git-aware-task-lifecycle). This contract defines how those
rules appear in document fields and edit behavior.

## Document map

| Document | Primary question | Temperature | Expected lifetime |
| --- | --- | --- | --- |
| `.csdd/specs.md` | What must be true? | Warm | Durable, revised as project intent changes |
| `.csdd/todo.md` | What work exists now, and who is accountable and executing? | Hot | Current operational cycle |
| `.csdd/decisions.md` | What consequential choice was made, and why? | Warm | Durable until superseded |
| `.csdd/handoff.md` | What must a later agent or session know to cross this boundary safely? | Hot | Transient, replaced or removed when the handoff is consumed |

Projects MAY omit `.csdd/archive/`. When present, it is standardized cold
context, not a fifth primary document. Its read policy is defined in
[Optional archive and cold history](protocol.md#optional-archive-and-cold-history).

## Initialization

This section owns the exact `/csdd init` operational contract. Conceptual
lifecycle, root rules, discovery stopping criteria, and safety invariants live
in [Initialization and adoption](protocol.md#initialization-and-adoption).
Canonical initialization templates live in
[`../assets/templates/`](../assets/templates/). The operational
[v0.1 → v0.2 migration guide](migration-v0.1-to-v0.2.md) is non-normative.
This document contract remains authoritative.

### State classification

Before writing, resolve one unambiguous canonical root and confirm the
destination is usable for classification. Only then classify the destination.
Classes are mutually exclusive by first-match precedence in this order, after
root ambiguity and destination conflicts have been ruled out:

| Order | State discovered | Required behavior |
| --- | --- | --- |
| 1 | Ambiguous or conflicting — competing or unresolved roots, `.csdd` is not a usable directory, or another destination conflict prevents safe classification | Stop and request clarification; never overwrite conflicting content |
| 2 | Absent — the canonical `.csdd/` path does not exist | Proceed with initialization |
| 3 | Already initialized — all four primary documents exist and the minimum current canonical structure validates | Do not overwrite; report that CSDD is already initialized and surface any validation concerns |
| 4 | Recognizable older state — existing CSDD state can be identified as following an older contract | Do not migrate; direct the user to the migration workflow |
| 5 | Partial or malformed — `.csdd/` exists but the state is neither valid current state nor recognizable older state | Do not modify; report incomplete or malformed CSDD state and offer a separate repair path |

Only Absent may proceed through `init`. An ambiguous or unusable destination
MUST block before absence is evaluated. An unusable `.csdd` path (for example
a regular file) MUST NOT classify as Absent. The presence of all four primary
filenames alone MUST NOT classify malformed current state as already
initialized. Every other class remains non-destructive and routes to
already-initialized reporting, migration, repair, or clarification as
applicable.

`init` initializes previously absent CSDD state only. It MUST NOT repair,
normalize, upgrade, migrate, or complete existing CSDD state. Successful
initialization MUST NOT imply permission for later repair, enrichment,
migration, staging, commit, push, or other repository actions.

### Allowed evidence sources

Initialization MAY use:

- explicit human and project instructions;
- canonical project documentation;
- README files and maintained technical guides;
- manifests, schemas, configuration, CI, and tests;
- code as evidence of current repository reality.

Code and tests MAY support descriptive current truth. They MUST NOT
independently authorize promoting observed implementation into a durable
requirement, constraint, invariant, stable interface, rationale, priority,
task, or accepted decision. Tests are stronger evidence of expected behavior
when they clearly exercise an acceptance or contract boundary; incidental
implementation tests do not make internal details normative.

The agent MUST:

- persist only claims supported by identifiable evidence;
- omit or describe as a gap any claim whose durability cannot be established;
- surface material contradictions instead of silently choosing a source;
- never invent content to make a template look complete.

Evidence, non-invention, preservation, and Scope rules take precedence over
document completeness. Targeted code and test inspection validates candidate
claims; repository size alone MUST NOT require exhaustive scanning.

### Progressive discovery and stopping

Follow the progressive discovery sequence and material stopping criterion in
[Progressive evidence-guided discovery](protocol.md#progressive-evidence-guided-discovery).
Deepen only when a material contradiction, unclear boundary, safety
constraint, public interface, persistence contract, or referenced-but-unread
source could change the resulting CSDD state. Generated output, vendored
dependencies, build artifacts, coverage, irrelevant snapshots, repetitive
internals, source-code TODO comments, broad issue history, and Git history
without a concrete question are outside default discovery.

### Generated structure

A successful new initialization creates one coherent patch containing only
these four primary documents directly under the canonical root:

```text
.csdd/
|-- specs.md
|-- todo.md
|-- decisions.md
`-- handoff.md
```

Do not create `.csdd/archive/` by default. Do not create version files,
databases, extra canonical documents, or harness-specific metadata. Do not
modify `AGENTS.md`, `CLAUDE.md`, README files, source code, configuration, or
unrelated project files as part of initialization. Do not stage, commit, push,
or open a pull request without separate authority.

### Document-specific initialization behavior

#### `specs.md`

- Populate only consequential project truth supported by evidence.
- Descriptive current reality MAY be included when useful, but MUST NOT be
  phrased as durable intent without supporting authority.
- Empty or sparse sections are valid.
- Unknowns and contradictions belong in the initialization report until the
  human supplies authoritative clarification; they MUST NOT become invented
  pseudo-specifications.

#### `todo.md`

- Create the six canonical H2 state headings in order: In Progress, Ready to
  Land, Blocked, Pending, Deferred, Recently Completed.
- Declare `Retention: 5`.
- Start without invented tasks, ownership, executors, scopes, priorities,
  dependencies, completed work, or an initialization self-task.
- Do not import issues, roadmaps, source-code TODO comments, or documentation
  wish lists automatically.

#### `decisions.md`

- Start without a fictional template decision.
- Do not infer rationale or accepted direction from implementation alone.

#### `handoff.md`

- Start without an active handoff entry.
- Initialization alone does not establish a boundary with concrete resumption
  risk.

### Coherent patch and failure cleanup

Initialization MUST behave as one logical adoption transaction:

1. record which destination paths existed before the attempt;
2. complete discovery and prepare the intended content before writing;
3. immediately before creating `.csdd/`, revalidate the canonical root and
   destination usability against the recorded preflight state, then reclassify
   from the beginning—stop without writing unless the destination is still
   unambiguously Absent;
4. create the four primary documents as one coherent patch;
5. validate the resulting structure and content;
6. report completion only when the structural postconditions hold.

On failure:

- remove only files safely attributable to the current initialization attempt;
- remove `.csdd/` only when the current attempt created it and it is empty
  after safe cleanup;
- never delete, restore, reset, or overwrite pre-existing content;
- never discard unrelated working-tree changes;
- a failed initialization attempt remains failed even when cleanup succeeds;
- successful cleanup only restores the pre-attempt state and does not convert
  failure into successful initialization;
- completion requires a coherent subsequent attempt that satisfies all
  structural postconditions;
- if cleanup is unsafe or incomplete, report the exact partial state and do
  not claim initialization completed.

Unrelated dirty working-tree state MUST be preserved. Existing or conflicting
content in the target `.csdd/` paths blocks automatic initialization.

### Questions and post-initialization enrichment

Initialization MUST NOT require a pre-write interview merely to make generated
documents appear complete.

Ask before writing only when a real blocker exists, such as:

- ambiguous project root;
- partial, old, malformed, or conflicting CSDD state;
- destination conflicts;
- insufficient permissions;
- a contradiction that prevents even a minimal honest initialization.

Missing requirements, decisions, tasks, or detailed specifications are normally
non-blocking. Initialize the truthful minimum, report the gaps, and offer an
optional follow-up conversation in which the human can clarify intent and
authorize enrichment. That follow-up is not part of initialization success and
MUST route new truth to the correct canonical document.

### Completion semantics

Successful initialization certifies coherent structural adoption, not
completeness of project knowledge. A sparse `specs.md`, empty operational
documents, and explicitly documented gaps are valid outcomes. The agent MUST
NOT invent claims, broaden Scope, continue discovery without material
justification, or answer unresolved questions on the human's behalf merely to
satisfy postconditions.

Hard structural completion conditions are:

- one unambiguous canonical root;
- previously Absent CSDD state through the pre-write revalidation;
- all four primary documents created coherently;
- canonical document structure validates;
- generated content respects evidence and non-invention rules;
- no pre-existing or unrelated content was modified.

Safe failure cleanup is not a structural success condition. Cleanup that
succeeds after a failed attempt restores the pre-attempt state only; it does
not satisfy completion. Knowledge coverage is reported, not graded as a
completion gate.

### Required user-facing result

The final response SHOULD state:

- the initialized project root;
- files created;
- principal evidence sources inspected;
- project truth persisted;
- sections deliberately left empty and why;
- material contradictions, uncertainties, or inspection limits;
- whether unrelated dirty state was observed and preserved;
- that no staging, commit, push, PR, migration, or unrelated edit occurred;
- that initialization confirms valid structure rather than exhaustive project
  knowledge;
- an optional offer to review and fill the reported gaps with the human.

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

### Canonical behavioral truth

`specs.md` is the canonical location for durable observable behavior,
requirements, constraints, and invariants.

When implementation or tests reveal undocumented behavior that is intended to
remain valid, promote it to `specs.md`.

Do not create a parallel decision entry merely to repeat the same behavioral
rule. Reference a decision only when that decision contains independently
useful context, rationale, rejected alternatives, or consequences.

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
- a state represented by placement under exactly one canonical state H2.

```markdown
## In Progress

- [ ] T-004 — Define document templates
```

For active collaborative work, tasks SHOULD include these fields when relevant:

- `Owner`: the accountable human or team and preferred coordination point;
- `Agent`: the current operational executor or harness/task label;
- `Scope`: the concrete write or contract boundary;
- `Updated`: the date of the last meaningful task-state update;
- `Target`: the integration branch or ref for repository-modifying work;
- `Base`: the `Target` commit observed at claim or at the last explicit
  reconciliation that updated `Base`.

`Landed` is not an active-work field. It belongs on repository-modifying tasks
that are already completed. A Ready to Land task MUST describe the pending
landing path with `Landing:` and MUST NOT use `Landed` for that purpose.

```markdown
- [ ] T-021 — Implement password recovery
  - Owner: valen
  - Agent: codex/auth-reset
  - Scope: `src/auth/reset-password/**`
  - Target: `main`
  - Base: `a1b2c3d`
  - Updated: 2026-07-12
```

`Depends on`, `Blocked by`, `Workstream:`, and a short `Note` MAY be added.
Trivial tasks MAY omit all ownership metadata. CSDD does not require story
points, completion percentages, mandatory priorities, risk scores, complex
labels, redundant timestamps, or mandatory reviewer fields. V0 MUST NOT
require YAML front matter, JSON, a database, a machine schema, or
harness-specific metadata.

Changing `Agent` does not necessarily change `Owner`. Neither field provides
secure identity or authentication. CSDD v0 MUST NOT attempt automatic human
identity discovery and SHOULD use human-readable labels rather than
provider-specific identifiers.

Changing the operational executor SHOULD update `Agent`.

Changing `Owner` requires explicit evidence that human or team accountability
has been reassigned. A stale agent claim alone is not sufficient.

`Target` and `Base` follow [Git-aware task
lifecycle](protocol.md#git-aware-task-lifecycle). `Landed` follows the same
section once the repository-modifying task is completed. A task entry does not
grant permission to commit, push, or merge. Edits to `todo.md` follow [Shared
coordination surfaces](#shared-coordination-surfaces).

### Canonical structure and presentation

Every `todo.md` MUST contain these six H2 headings, including when empty, in
this exact order:

```markdown
## In Progress
## Ready to Land
## Blocked
## Pending
## Deferred
## Recently Completed
```

H2 headings under `# TODO` are reserved for canonical task state. Projects and
agents MUST NOT omit, rename, reorder, alias, or add state H2 headings. Every
task present in `todo.md` MUST appear under exactly one canonical state H2.
Active and lateral states use unchecked task items (`- [ ]`). Recently
Completed uses checked task items (`- [x]`).

State is always the primary grouping dimension. The default presentation is
flat: tasks appear directly under their state H2.

```markdown
## Pending

- [ ] T-020 — Make handoffs boundary-driven
  - Owner: valen
  - Note: Depends on T-018.
```

A task MAY use an optional `Workstream:` field when thematic context
materially improves coordination under flat presentation.

Projects MAY instead adopt H3 workstream grouping. H3 grouping is opt-in and
requires an existing project convention or explicit human direction; an agent
MUST NOT introduce or switch grouping modes autonomously.

When H3 grouping is used:

- H3 headings are thematic only and never express task state;
- tasks within a grouped state section MUST live under an H3 rather than
  mixing grouped and direct task entries;
- tasks without a specific workstream use `### General`;
- `Workstream:` MUST NOT duplicate the H3;
- deeper grouping is not allowed;
- empty H3 headings are removed;
- Recently Completed remains flat and does not use H3 grouping.

```markdown
## In Progress

### Auth

- [ ] T-030 — Reset password flow
  - Owner: valen
  - Agent: cursor/auth-reset
  - Scope: `src/auth/reset/**`
  - Updated: 2026-07-18

### General

- [ ] T-031 — Fix docs typo
  - Owner: valen
  - Agent: cursor/docs-typo
  - Scope: `README.md`
  - Updated: 2026-07-18
```

### Task lifecycle states

Task state is represented by section placement under the canonical H2
structure. Semantic states for repository-modifying work follow the protocol's
[Git-aware task lifecycle](protocol.md#git-aware-task-lifecycle) and [TODO
structure and retention](protocol.md#todo-structure-and-retention):

```text
Pending → In Progress → Ready to Land → Recently Completed
```

`Blocked` and `Deferred` are lateral states.

| State | Claim and presentation expectations |
| --- | --- |
| Pending | Accepted execution-queue work. No active `Agent` or write claim. MAY name dependencies. Not Blocked merely because an unstarted dependency remains. MUST NOT be created from speculative ideas without evidence the work was accepted. Age alone does not authorize removal or deferral. |
| In Progress | Active collaborative work SHOULD carry `Owner`, `Agent`, `Scope`, and `Updated` when coordination needs them, plus `Target` / `Base` when the protocol requires them. |
| Ready to Land | Active unchecked task state, not a completed outcome. Persist when verified work remains unlanded at a session, responsibility, or coordination boundary; omit persistence only when landing completes in the same uninterrupted operation. Retain honest `Agent`, protected `Scope`, `Target`, `Base`, and `Updated` when required. MUST include `Landing:`; SHOULD include concise `Verification:`; MUST NOT use `Landed:`. `Agent` MAY change when landing responsibility is genuinely transferred or reclaimed. |
| Blocked | Name the blocker. Retain `Scope` only when partial work or safe continuation needs protection; otherwise release `Scope` and explain why. |
| Deferred | Authoritative intent required. MUST include `Reason:` and `Resume when:`. MAY retain `Owner`. MUST NOT have an `Agent`. MUST omit active Scope or use `Scope: released`. MUST NOT conceal partial or unlanded repository changes. Vague resume conditions are invalid. |
| Recently Completed | Satisfies the protocol completion rules; active write scope is released; `Landed` recorded when required; checked item under the bounded retention window. |

#### Pending

Pending is the accepted execution queue: work that may be claimed without a new
product or prioritization decision once capacity and dependencies permit.

```markdown
## Pending

- [ ] T-022 — Update templates and write the migration guide
  - Owner: valen
  - Note: Depends on T-018 through T-021.
```

#### Ready to Land

```markdown
## Ready to Land

- [ ] T-050 — Harden session token rotation
  - Owner: valen
  - Agent: cursor/auth-token-rotation
  - Scope: `src/auth/tokens/**`, `tests/auth/tokens/**`
  - Target: `main`
  - Base: `a1b2c3d`
  - Updated: 2026-07-18
  - Landing: Branch pushed; open PR against `main` after review
  - Verification: `git diff --check` passed; token rotation tests green
```

#### Deferred

Deferral requires evidence from the user, Owner, accepted planning, or another
authoritative project source. An agent MUST NOT defer work autonomously merely
because it is difficult, old, blocked, unfinished, or inconvenient.

```markdown
## Deferred

- [ ] T-040 — Migrate legacy billing export
  - Owner: valen
  - Scope: released
  - Reason: Waiting for the billing schema freeze announced by the Owner
  - Resume when: Billing schema freeze is published in `specs.md`
  - Updated: 2026-07-18
```

Invalid deferral: inventing Deferred to park unfinished work, omitting
`Reason:` or `Resume when:`, using non-observable conditions such as “later”
or “when there is time”, keeping an `Agent`, retaining a concrete active
Scope, or using Deferred to hide unlanded repository changes. If partial work
needs protection, the honest state is normally Blocked. When a resume
condition is known to be satisfied, reconcile into Pending or directly into
In Progress when claimed in the same operation.

`Icebox` is not a valid state alias.

#### Recently Completed retention

Directly under `## Recently Completed`, the project declares:

```markdown
## Recently Completed

Retention: 5
```

The v0.2 default is `Retention: 5`. If the line is absent in an older project,
agents MUST use five as the fallback until migration. `N` is a positive
integer (`N >= 1`) and applies globally, not per workstream. `Retention: 0`
is invalid. A human or explicit project policy MAY change it. Agents MUST NOT
increase it autonomously to avoid compaction.

Recently Completed:

- remains flat;
- is ordered newest first;
- retains entries until they exceed the declared limit;
- does not permit subjective early removal;
- does not support pinned entries.

When a task completes, the closing agent MUST, in the same coherent TODO
patch:

1. insert it at the top;
2. update `Updated` to the completion transition date;
3. compact metadata that no longer serves operational coordination;
4. remove the oldest entries that exceed `Retention`.

An agent modifying Recently Completed MUST reconcile an existing overflow. An
agent editing an unrelated state section is not required to audit retention.

Completed entries MUST omit concrete active Scope and SHOULD remove
active-only metadata such as `Base` and usually `Target`. `Agent` and `Owner`
MAY be omitted during compaction without rewriting historical executor
identity. `Landed` remains when required by the Git-aware lifecycle. `Note`
remains only when it still helps interpret current operational work.

```markdown
## Recently Completed

Retention: 5

- [x] T-018 — Define the Git-aware task lifecycle
  - Owner: valen
  - Scope: released
  - Updated: 2026-07-18
  - Landed: PR #10 @ `00d06fb`
  - Note: Git-aware lifecycle contract merged to `main`.
```

Removing an entry because of retention is eviction from the operational view,
not a new lifecycle state. It MUST NOT create an `Archived` state, MUST NOT
mechanically copy the task into `.csdd/archive/`, and MUST NOT authorize reuse
of its stable task ID. Durable truth SHOULD be promoted during task closure.
If an old entry visibly contains unpromoted consequential truth, promote it
before removal, but routine compaction does not require historical
archaeology. Git, pull requests, and issues remain the sources for exact
implementation history. Optional archive entries preserve semantic cold
history only when a concrete historical question warrants them; they are not
a mechanical destination for retention overflow.

### Contains

- all six canonical state H2 headings, including when empty;
- pending, in-progress, ready-to-land, blocked, and deferred work when used;
- ownership, execution, and active scope when coordination requires them;
- `Target` and `Base` when active repository work needs them;
- `Landing` and optional `Verification` on persisted Ready to Land tasks;
- `Landed` on completed repository-modifying tasks when required;
- `Reason` and `Resume when` on every Deferred task;
- dependencies or blockers when relevant;
- a short note or completion condition when it materially helps execution;
- a visible `Retention: N` declaration and bounded Recently Completed window.

### Does not contain

- a full history of completed work;
- detailed implementation narration;
- architectural rationale;
- durable requirements;
- transient debugging notes unrelated to coordination;
- vague ownership scopes that prevent unrelated work;
- project-management metadata without a demonstrated coordination purpose;
- implied commit, push, or merge authority;
- agent-invented state H2 headings or `Icebox` aliases;
- YAML, JSON, front matter, a database, or another canonical task document.

### Update triggers

Update `todo.md` when:

- work is claimed or released;
- scope, `Owner`, `Agent`, state, dependency, or blocker changes;
- `Target`, `Base`, or landing evidence changes materially;
- work becomes ready to land, blocked, deferred, or resumes from those states;
- a meaningful checkpoint is needed to protect continuity;
- work completes or becomes abandoned;
- Recently Completed gains an entry or requires overflow compaction;
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
the preferred coordination point. When another baseline may hold live
overlapping work or divergent durable truth, follow [Branch and worktree
locality](#branch-and-worktree-locality) and the protocol reconciliation
procedure before reclaiming.

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

Keep active and near-term work hot. `todo.md` MUST retain Recently Completed
entries only within the declared `Retention: N` bound (fallback five when the
line is absent). Order newest first and compact overflow in the same coherent
patch that inserts a completed entry or otherwise modifies Recently Completed.
Do not perform subjective early removal or pin entries.

At the end of a meaningful phase or milestone, relevant history MAY be
distilled into an archive entry. Do not mechanically copy completed tasks.
Retention removal is not archival and does not authorize task-ID reuse.
Durable specifications MUST remain in `specs.md`, durable decisions MUST remain
in `decisions.md`, and current operational state MUST remain in `todo.md`.
Git, pull requests, and issues remain the sources for exact implementation
history.

### Update responsibility

The executing agent is responsible for keeping task state, `Agent`, scope, and
checkpoints honest. An agent that detects conflicting scope MUST surface the
conflict before changing the claim or overlapping code.

### Ownership, execution, and scope semantics

`Owner`, `Agent`, and `Scope` represent different forms of project state:

- `Owner` identifies the human or team accountable for the work.
- `Agent` identifies the current operational executor.
- `Scope` identifies the files, modules, or contracts currently claimed for
  modification.

A change of operational executor normally updates `Agent`, `Updated`, and any
reconciliation note. It does not transfer human accountability.

Changing `Owner` requires explicit evidence that responsibility was reassigned
by the user, responsible team, or authoritative project state. A stale `Agent`
claim, a new execution session, or a task-completion action is not sufficient
evidence to change `Owner`.

### Completed-task claims

When a task becomes completed, interrupted without continuation, cancelled, or
otherwise no longer active, its write claim must be released.

A completed task MUST either:

- use `Scope: released`; or
- omit `Scope` and other active-claim metadata when compacted.

Concrete file or glob scopes MUST NOT remain on completed tasks when they could
be interpreted as active claims.

For repository-modifying work, completion additionally requires the Git-aware
rules in [Git-aware task lifecycle](protocol.md#git-aware-task-lifecycle):
verification, reachability from the resolved `Target`, no unlanded task changes
and no unresolved unattributed changes remaining inside `Scope`, and `Landed`
recorded when required. Implementation finished but unlanded work belongs in
`Ready to Land` or another honest active state, not `Recently Completed`.

Completed entries under Recently Completed MUST omit concrete active Scope and
SHOULD remove active-only metadata such as `Base` and usually `Target`.
`Agent` and `Owner` MAY be omitted during compaction without rewriting
historical executor identity. `Landed` remains when required. `Note` remains
only when it still helps interpret current operational work. That compacted
metadata must not block or confuse future overlap detection.

`Blocked` tasks follow the same scope-retention rule as the protocol: keep
`Scope` only when partial work or safe continuation needs protection;
otherwise release it and explain why. `Deferred` tasks MUST release any active
claim and MUST NOT use deferral to conceal unfinished repository changes.

Handoff cleanup for completed work follows [Closure
behavior](#closure-behavior); stale-claim and cross-worktree checks remain in
[Stale claims](#stale-claims) and [Branch and worktree
locality](#branch-and-worktree-locality).

Stable task IDs remain reserved after retention removal. An evicted ID MUST NOT
be reused for a different task.

### Historical Agent metadata

The agent that reconciles, verifies, archives, or closes a task is not
automatically the agent that executed the task.

Closure MUST NOT overwrite historical `Agent` metadata solely to identify the
closing agent.

Valid approaches include:

1. preserve the agent that performed the substantive task;
2. omit `Agent` when compacting old completed entries;
3. record the closure agent only on a dedicated phase-closure task;
4. change `Agent` when the new agent genuinely reclaimed and executed the
   remaining task work.

If the project needs both executor and verifier provenance, it should define
separate fields rather than overloading `Agent`.

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

### Decision threshold and duplication

A decision entry should capture an accepted direction whose rationale or
tradeoffs are likely to matter after the immediate implementation context is
gone.

`decisions.md` should not restate requirements already canonical in
`specs.md`.

A behavioral rule may be supported by a decision when the decision contributes
distinct durable value, such as:

- meaningful alternatives that were rejected;
- architectural or product tradeoffs;
- migration or compatibility consequences;
- legal, security, or operational rationale;
- conditions under which the choice may be revisited.

When no such independent rationale exists, record the behavior only in
`specs.md`.

## `handoff.md`

### Contract

Transfer the minimum replaceable snapshot needed for a later agent or session to
cross a real execution boundary safely when concrete resumption risk exists.

V0 MUST use one canonical `.csdd/handoff.md`. It is a transient resume point, not
a progress log, duplicate task tracker, live collision board, or permanent
history. Multiple or scoped handoff files are outside v0.

Conceptual lifecycle rules—boundary and risk, consumption, outcome-specific
behavior, and relationship to session close—live in [Boundary-driven
handoffs](protocol.md#boundary-driven-handoffs). This section owns the
document-local contract.

### Read policy

Read the relevant task or workstream section when continuing prior work or when
an active task indicates that boundary transfer state with concrete resumption
risk may exist. Trivial or unrelated work MAY avoid reading `handoff.md`.

A handoff is a claim about recent transfer state, not proof that the repository
is unchanged. Confirm critical details against repository reality and current
task state before acting. Edits follow [Shared coordination
surfaces](#shared-coordination-surfaces).

Reading, claiming, reassigning, or beginning to resume does not consume the
entry.

### Creation and update trigger

Create or update a handoff only when both hold:

1. a real continuity, responsibility, impediment, landing, dependency, or
   collision boundary; and
2. concrete resumption risk that Git, `todo.md`, and other canonical project
   documents do not already make safe to ignore.

Neither condition alone is sufficient. Routine session closure, uninterrupted
work, ordinary checkpoints, state changes, and live collisions do not
independently require a handoff.

Relevant boundaries include:

- work pauses or a session closes with consequential partial state;
- operational responsibility genuinely transfers;
- work becomes blocked or is interrupted;
- verified work remains unlanded because landing is delayed or transferred;
- a collision forces a workstream to pause, sequence, or transfer;
- an active dependent workstream needs non-obvious transfer state.

A successful self-contained task does not create a handoff unless a separate
active dependent workstream independently satisfies both boundary and concrete
resumption risk. A live collision resolved during uninterrupted work is
coordinated in `todo.md` without creating a handoff.

### Concrete risk requirement

Every active handoff entry MUST identify a concrete resumption risk. Generic
statements such as “context may be lost” are insufficient.

If no concrete risk can be stated, the entry MUST NOT be created or MUST be
removed.

The entry MUST contain only the additional transient state needed to mitigate
that risk. A checkpoint and next safe action are recommended when they are not
already obvious from Git, `todo.md`, or another canonical source.

Exact labels such as `Checkpoint:`, `Resume risk:`, or `Next:` are not
mandatory. Projects MAY configure presentation while preserving the semantic
contract. Do not require empty subsections or invent mandatory handoff metadata
such as `From:`, `To:`, `Consumed:`, `Status:`, a second owner, or a
handoff-specific timestamp.

### Contains

- the concrete resumption risk that justifies the entry;
- the non-obvious checkpoint or partial state needed to mitigate that risk;
- the next safe action when it is not already obvious;
- costly verification results, exact errors, temporary hypotheses, unresolved
  questions, or canonical references only when needed to resume efficiently.

### Does not contain

- the canonical backlog, task ownership, `Owner`, `Agent`, `Scope`, overlap
  model, or other task metadata duplicated merely to complete a format;
- a permanent chronological project history or appended session narration;
- full chat transcripts or reasoning traces;
- durable requirements or accepted architectural rationale;
- routine details a later agent or session can cheaply rediscover;
- completed-session summaries with no continuing value;
- a live collision board or continuously synchronized activity log.

### Relationship to `todo.md`

`todo.md` remains canonical for task state, `Owner`, `Agent`, `Scope`,
dependencies, blockers, overlap, sequencing, and collision prevention.
`handoff.md` contains only additional non-obvious transient implementation or
verification state that must cross a boundary safely.

These responsibilities MUST remain distinct. `handoff.md` MUST NOT become a
duplicate task tracker or the primary collision-prevention mechanism.

Operational rule:

```text
coordination without boundary + risk -> todo.md
coordination with boundary + risk    -> todo.md and, when needed, handoff.md
```

When both refer to the same task, the handoff SHOULD link or refer to the
canonical task entry rather than duplicate ownership fields. If they disagree,
reconcile the task state before continuing.

Outcome-specific representation follows the table in [Boundary-driven
handoffs](protocol.md#boundary-driven-handoffs).

### Organization and presentation

Use one current entry per task or workstream.

Default to task-oriented entries and use the canonical task ID when one exists.
Use a workstream entry only when the transferred state genuinely spans multiple
tasks or no canonical task exists.

Do not organize entries by agent, harness, session, or date. Do not accumulate
multiple snapshots of the same work.

Presentation inside an entry is project-configurable. Recommended compact
content may include the non-obvious checkpoint, the concrete resumption risk,
and the next safe action. Do not require empty subsections or fixed mandatory
labels.

Conforming compact example:

```markdown
# Handoff

## T-021 — Implement password recovery

- Checkpoint: recovery token minting works; email delivery stub still returns 503
- Risk: resuming without the stub failure mode will re-run the full auth suite and miss the open delivery blocker
- Next: fix the mail stub, then re-run only the delivery integration test
```

Non-conforming patterns include progress narration during uninterrupted work,
entries without a concrete risk, mandatory empty checklist subsections, and
appending successive session histories for the same task.

### Responsibility and validation

The executor leaving consequential resumable state writes the handoff at the
boundary, after reconciling Git and `todo.md`. The resumer may be another agent
or the same agent in a later session.

The resumer MUST validate critical claims against repository reality and current
task state before relying on them.

The executor whose work resolves or transforms the risk is responsible for
removing or replacing the entry. Cleanup responsibility does not remain
permanently with the original author.

Do not invent or preassign a new `Agent` merely to complete a handoff. Update
`Agent` only when operational responsibility genuinely changes under the
Git-aware lifecycle contract.

### Consumption, replacement, and cleanup

A handoff is consumed only when the resumption risk that justified it has been
resolved, superseded, or made safely recoverable from canonical project and
repository state.

When consumed:

- remove the entry if no new boundary and risk exist;
- replace it if a new boundary and risk require a different current snapshot;
- never retain it as completed history or mark it with a consumed/completed
  status.

Cleanup occurs at the first coherent reconciliation after the risk disappears.
At the latest, before the next close, transfer, or landing, the entry must still
be correct and necessary, have been replaced, or have been removed.

A known materially false entry MUST be cleared or replaced at the next coherent
reconciliation; boundary-snapshot semantics do not authorize preserving
misleading state.

Promote validated durable truth to its canonical document before clearing
transient state.

### Stale entries

Age alone does not prove that a handoff is stale.

Before removing an apparently stale entry, compare it with `todo.md`, Git,
working-tree state when available, and active claims. If current responsibility
or repository reality is uncertain, reconcile or block rather than silently
inferring abandonment.

## Cross-document movement

Information SHOULD move when its purpose or lifetime changes, not be copied
indefinitely.

| From | Trigger | Canonical destination |
| --- | --- | --- |
| Session notes | A finding is validated and must remain true | `specs.md` |
| Session notes | A consequential choice is accepted | `decisions.md` |
| Session notes | Work, scope, status, or blocker changes | `todo.md` |
| Session notes | Boundary + concrete resumption risk requires transient transfer state | `handoff.md` |
| `handoff.md` | A temporary finding becomes durable | `specs.md` or `decisions.md` |
| `handoff.md` | Resumption risk is resolved, superseded, or recoverable from canonical state | Remove or replace the entry; never retain as completed history |
| `todo.md` | Rejected, cancelled, or obsolete work; or completed work exceeding `Retention` | Remove rejected/cancelled/obsolete entries after promoting consequential truth. Evict completed entries only under the Retention rule. Optional semantic archive remains independently justified; retention overflow is not mechanical archival and does not authorize task-ID reuse. |
| `decisions.md` | A decision changes | Add explicit supersession; optionally move old detail to cold context |

Links may appear across documents, but one document should remain canonical for
each fact. When moving information, update or remove the stale source so it does
not continue presenting an old truth.

Prefer links or identifiers such as `REQ-005` and `DEC-002` over copying the
same normative statement into multiple documents.

### Closure behavior

When the resumption risk that justified a handoff is resolved, superseded, or
safely recoverable from canonical project and repository state, remove the
entry—or replace it when a new boundary and risk require a different current
snapshot. Do not mark handoff entries completed or retain them as history.

Phase summaries, completed-task history, and durable behavior do not belong in
the active handoff. Promote them to their canonical durable document or a
semantic archive entry.

Completed tasks remove their obsolete handoff state unless a separate active
dependent workstream has its own concrete transfer risk. Ready to Land, blocked,
partial, interrupted, transfer, and collision closes follow the outcome table in
[Boundary-driven handoffs](protocol.md#boundary-driven-handoffs) and MUST NOT
create a handoff solely because the session ended or the task state changed.

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

Archive access follows [Optional archive and cold
history](protocol.md#optional-archive-and-cold-history). Entries SHOULD be
organized by meaningful phase, milestone, experiment, migration, or workstream
and MUST NOT be created for every agent session. A monolithic, indefinitely
growing `history.md` SHOULD NOT be used.

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

### Archived task metadata

Archive entries may reference completed task IDs and outcomes, but should not
preserve active claim semantics.

Do not archive concrete scopes as if they remained owned. If scope history is
material, describe it as historical context and state explicitly that the claim
was released.

Archive summaries should preserve phase meaning, not every operational field
from `todo.md`.

## Branch and worktree locality

CSDD documents are versioned project artifacts. Their visible state is local to
the checked-out Git branch and worktree. The current worktree is the operational
baseline for reading and writing these documents; it does not prove the absence
of activity, claims, or durable-truth changes elsewhere.

A claim in `.csdd/todo.md` coordinates agents that can observe that version of
the document. It is not a repository-global lock. Agents on another branch,
worktree, or unmerged commit MAY not see or honor the claim.

The absence of a claim in the current worktree does not prove the absence of
relevant claims or in-flight work elsewhere.

The authoritative procedural sequence—Trigger, Discover, Compare, Classify,
Reconcile or block, Execute, Close—and the divergence classes are defined in
[Branch and worktree baseline
reconciliation](protocol.md#branch-and-worktree-baseline-reconciliation). This
section states document-local evidence and update rules.

### When to inspect other worktrees

Cross-worktree inspection is required only when concurrency, stale claims,
scope overlap, or durable-truth divergence could change the claim, reclaim,
resume, or implementation decision. Do not scan every worktree for Level 0
work that is clearly local and unrelated.

### Cross-worktree evidence

When that trigger applies, inspect:

- active worktrees and their checked-out branches;
- clean or dirty working-tree state;
- uncommitted changes inside claimed or requested scopes;
- relevant commits affecting `.csdd/` or the requested implementation scope;
- divergent `todo.md`, `handoff.md`, `specs.md`, or `decisions.md`.

Dirty files inside a conflicting claimed scope are strong evidence of active
work. A worktree's mere existence is not sufficient evidence by itself.

Claim age remains only one signal. Branch age, worktree state, handoff state,
repository changes, and current user instruction must be considered together.
None of those signals alone proves abandonment or safety to ignore another
baseline.

### Divergence classes and document effects

Map observed differences to the protocol classes:

| Class | Typical document evidence | Required handling |
| --- | --- | --- |
| No material divergence | No relevant claim, handoff, or durable-doc difference that changes the decision | Continue on the current baseline |
| Coordination-only divergence | Differences limited to `todo.md` or `handoff.md` | Preserve live compatible claims; block on live conflict; explicitly reclaim or supersede stale operational state; import a valid handoff with source recorded when useful |
| Durable-truth divergence | Material differences in `specs.md` or `decisions.md` | Reconcile before implementing dependent behavior; do not concatenate or silently copy |
| Live conflicting work | Active overlapping claim plus dirty or recent overlapping commits in another worktree/branch | Surface overlap; coordinate, sequence, or block; do not silently reclaim or overwrite |

### Durable truth divergence

Material differences in `specs.md` or `decisions.md` must be reconciled before
implementing behavior that depends on the disputed truth.

Do not combine divergent durable documents by concatenation or silent copying.
Choose or construct the target truth explicitly through merge, rebase,
cherry-pick, or manual reconciliation, preserving rationale and provenance.
Record accepted directional changes in `decisions.md` when the reconciliation
supersedes a consequential choice.

### Coordination divergence

Differences limited to `todo.md` or `handoff.md` may be reconciled by:

- preserving a live compatible claim;
- blocking on a live conflicting claim;
- explicitly reclaiming stale operational execution while preserving `Owner`
  unless human accountability is explicitly reassigned;
- superseding obsolete coordination state;
- importing a valid handoff with its source branch or commit recorded.

Reconciliation in one branch does not silently modify or release claims stored
only in another branch. Closing or releasing scope on the current baseline
must not imply that another worktree's active claim was cleared.

Stale-claim reclamation across baselines still follows [Stale
claims](#stale-claims) and Owner/Agent semantics: age is evidence, not proof;
reclamation must be explicit; historical `Agent` metadata is not rewritten
merely by verification or closure on another baseline.

### Provenance

When CSDD state is imported, superseded, or reconciled across branches, record
the relevant source branch, worktree, or commit when that provenance is useful
for future recovery—for example in a task `Note`, handoff section, or decision
rationale.

## Contract-level open questions

- Which `Agent` label conventions remain portable across Codex, Cursor, Claude
  Code, and future harnesses?
- Which normative statements should be promoted from SHOULD to MUST after
  real-world testing?
- Will one `.csdd/handoff.md` remain practical under concurrent editing?
- Does the archive model remain useful without becoming redundant with Git and
  durable project documents?
