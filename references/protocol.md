# Collaborative Spec-Driven Development Protocol

Status: Phase 0 conceptual draft

## Summary

Collaborative Spec-Driven Development (CSDD) is a lightweight protocol for
preserving project state and coordinating work across ephemeral AI coding
sessions. It externalizes the minimum sufficient state that a new or concurrent
agent needs to resume work safely without relying on shared chat history.

CSDD does not provide true shared agent memory or create a shared mind. It
provides durable, inspectable project artifacts from which each agent can
reconstruct a task-appropriate working context.

> Agents are ephemeral. Project state must be durable.

## Normative language

The terms MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY express v0 protocol
requirements, recommendations, and options. Lowercase terms are descriptive.
Normative language is used only where interoperability or safety requires a
clear rule.

## Problem

AI coding agents are context-isolated. When work spans sessions, agents, or
harnesses, useful knowledge can remain trapped in a chat, be reconstructed
manually, or be interpreted inconsistently. The human operator becomes the
message bus, memory layer, and conflict resolver.

This produces recurring failure modes:

- repeated onboarding and investigation;
- lost constraints and rationale;
- conflicting or silently reversed decisions;
- overlapping edits and unclear ownership;
- stale assumptions about code or active work;
- ever-growing context files that recreate the context-window problem.

## Goal

CSDD externalizes the minimum sufficient project state needed for agents to:

- orient themselves;
- continue existing work;
- respect requirements and prior decisions;
- detect overlap with concurrent work;
- preserve consequential discoveries;
- leave the project in a state another agent can resume.

## Non-goals

CSDD v0 does not attempt to:

- share full reasoning or chat history between agents;
- provide autonomous multi-agent orchestration;
- replace Git, tests, issue trackers, or project documentation;
- manage operator personality or communication preferences;
- prescribe code style, performance practices, or dependency policy;
- require runtime services, hooks, databases, or provider-specific APIs;
- eliminate human judgment when evidence or decisions conflict.

## Context layers

CSDD distinguishes context by owner, purpose, and lifetime.

| Layer | Name | Examples | CSDD v0 scope |
| --- | --- | --- | --- |
| L0 | Operator context | Communication style, personal defaults, preferred workflows | Recognized, not managed |
| L1 | Durable project context | Requirements, constraints, invariants, decisions | Managed |
| L2 | Coordination context | Tasks, ownership, scope, blockers, handoffs | Managed |
| L3 | Session working context | Current conversation, temporary hypotheses, debugging notes | Ephemeral, not managed by default |

Information may move between layers. A temporary observation in L3 becomes
shared state only when losing it would harm later work. Operator preferences in
L0 become L1 only when the project explicitly adopts them as project policy.

## Context temperature

Temperature describes how often information changes and how readily an agent
should load it. It does not make any document mandatory reading.

### Hot context

Current, operational, and frequently changing:

- `.csdd/todo.md`;
- `.csdd/handoff.md`.

Hot context is the first candidate for project or collaborative work, but a
trivial isolated task may need neither file.

### Warm context

Durable and slower-changing:

- `.csdd/specs.md`;
- `.csdd/decisions.md`.

Agents load only the sections relevant to the task.

### Cold context

Historical material kept for occasional recovery or investigation:

- the optional `.csdd/archive/`;
- relevant Git history.

Cold context is never part of default context hydration. It is consulted only
when current state points to it or the task requires historical explanation.

## Core project-state documents

CSDD v0 uses one canonical, deterministic project-state location:

```text
.csdd/
|-- specs.md
|-- todo.md
|-- decisions.md
|-- handoff.md
`-- archive/        # optional
```

The four primary documents MUST live directly under `.csdd/`, and CSDD state
MUST remain human-readable Markdown. V0 does not support project-root
alternatives, arbitrary paths, or configurable discovery. A fixed location
reduces discovery ambiguity, context cost, harness-specific behavior, and
adapter complexity. Configurable locations remain a possible post-v0 feature.

CSDD separates the four documents by responsibility:

| Document | Context layer | Primary responsibility |
| --- | --- | --- |
| `.csdd/specs.md` | L1 | Durable requirements, constraints, invariants, and contracts |
| `.csdd/decisions.md` | L1 | Consequential choices, rationale, consequences, and supersession |
| `.csdd/todo.md` | L2 | Current work, accountability, executor, scope, dependencies, and blockers |
| `.csdd/handoff.md` | L2 | Minimum replaceable transfer state at a boundary with concrete resumption risk |

`todo.md` and `handoff.md` MUST preserve distinct responsibilities. `todo.md` is
the primary coordination surface for active work and overlap detection.
`handoff.md` holds only additional non-obvious transient state needed to cross a
boundary safely; it is not the primary collision-prevention mechanism, a
parallel task tracker, or chronological history. See [Boundary-driven
handoffs](#boundary-driven-handoffs).

The detailed boundaries, read policies, update triggers, and aging rules are
defined in [document-contracts.md](document-contracts.md). The protocol defines
conceptual responsibilities and minimal Markdown conventions, not a machine
schema.

## Principles

### P1 - Agents are ephemeral; project state is durable

Critical project state MUST NOT exist exclusively in chat history. Durable does
not mean immutable: state must remain updateable as the project changes.

### P2 - Persist consequential knowledge, not activity

Persist what would hurt another agent to lose. Do not record every command,
edit, failed experiment, or trivial implementation choice.

Knowledge is consequential when its loss could cause duplicated work,
conflicting implementation, repeated investigation, architectural regression,
or an unsafe assumption.

### P3 - Minimum sufficient context

An agent SHOULD load the smallest amount of project state that allows it to act
correctly and safely. More available context is not automatically better
context.

### P4 - Separate state by purpose and lifetime

Requirements, work state, decisions, handoffs, operator preferences, and
session notes have different owners and aging rules. They MUST NOT be collapsed
into one accumulating document.

### P5 - Current state over accumulated history

The default operational view SHOULD describe the project now. Historical value
MAY be retained as cold context, but it MUST NOT burden routine agent startup.

### P6 - Explicit coordination over inferred coordination

Active collaborative work SHOULD expose enough ownership, scope, state, and
dependency information for another agent to detect likely overlap. Agents MUST
NOT knowingly ignore active scope overlap or assume that silence means a scope
is free.

### P7 - No silent contradiction

When repository evidence, specifications, decisions, or active work conflict,
an agent MUST surface and reconcile the conflict rather than silently overwrite
one side.

### P8 - Documentation is project state, not unquestionable reality

CSDD documents are authoritative statements of project intent and coordination,
but they can become stale. Conflicting repository evidence MUST be investigated
and reconciled; neither documentation nor code wins automatically.

### P9 - Durable knowledge should be promoted; transient knowledge should expire

Validated knowledge should move to the document whose lifetime matches it.
Temporary observations should be removed, replaced, or promoted when they stop
being current.

### P10 - Context loading must be proportional to task need

CSDD context hydration MUST NOT be unconditional. Agents SHOULD
escalate context only when scope, uncertainty, dependencies, behavioral impact,
or possible overlap demand it.

### P11 - Coordination overhead must not exceed task complexity

The protocol MUST NOT make a trivial change more expensive than the change
itself. Claiming work, writing handoffs, and updating shared state are required
only when they reduce meaningful coordination or continuity risk.

## Adaptive context hydration

Before reading CSDD state, estimate the minimum context required to perform the
task safely. Classify by risk and scope, not merely by apparent effort.

Relevant signals include:

- whether the target is explicit and local;
- whether the change is reversible;
- whether behavior or a public contract changes;
- whether the work crosses modules or files;
- whether interpretation or architectural judgment is required;
- whether active work may overlap;
- whether the task continues or depends on prior work.

### Hydration level 0 - Direct execution

Use for clearly bounded, local, low-risk work such as a typo or an explicitly
identified text replacement. The target should be explicit, reversible,
non-behavioral, independent of prior work, and have no plausible active-scope
overlap.

Flow: inspect target -> execute -> verify.

Trivial or isolated tasks MAY avoid reading CSDD documents entirely. If the
target reveals broader impact, increase hydration.

### Hydration level 1 - Local awareness

Use for a localized change with plausible but limited interaction with active
work.

Flow: inspect target -> check relevant active scope if needed -> execute ->
verify.

Read only the coordination state needed to rule out overlap.

### Hydration level 2 - Operational context

Use for non-trivial bugs, features, integrations, multi-file changes, or
continuation of existing work.

Read relevant hot context, then only the applicable sections of warm context.

### Hydration level 3 - Deep project context

Use for architecture, migrations, broad refactors, ambiguous features, or work
that crosses domains.

Read hot context and relevant warm context. Consult cold context only on demand.

If new evidence increases scope or uncertainty, increase hydration. Do not keep
a task at a lower level merely because its original wording looked simple.

## Adaptive session lifecycle

The full lifecycle is a toolbox, not a ritual. Use only the phases justified by
the task. Session phases below describe how an agent works; the
[Git-aware task lifecycle](#git-aware-task-lifecycle) describes how task state
moves relative to repository evidence.

| Task class | Expected lifecycle |
| --- | --- |
| Trivial | Execute -> Verify |
| Local | Inspect -> Execute -> Verify |
| Project | Bootstrap -> Orient -> Execute -> Reconcile |
| Collaborative | Bootstrap -> Orient -> Claim/Plan -> Execute -> Reconcile -> Handoff/Close |

### Bootstrap

Detect whether the project uses CSDD and locate its state, project-level
instructions, and available documentation.

### Orient

Reconstruct minimum sufficient context. Inspect relevant handoff and work state
when resumable risk may exist, validate critical handoff claims against
repository reality before relying on them, then load only relevant
specifications and decisions.

### Claim/Plan

For concurrent or continuity-sensitive work, identify the task, human `Owner`,
executing `Agent`, intended scope, dependencies, and likely overlap before
editing when those fields are relevant. For repository-modifying work, resolve
`Target` and apply the `Base` rules in [Git-aware task
lifecycle](#git-aware-task-lifecycle). Run the refresh checkpoint before writing
when that section requires it.

A task claim coordinates scope and continuity. It does not grant automatic
permission to commit, push, or merge.

### Execute

Perform the work. Preserve consequential discoveries, but do not turn shared
documents into an activity log. Checkpoints are warranted when work becomes
partial, blocked, materially different in scope, or important to concurrent
agents.

### Reconcile

Compare the resulting repository state, verification results, task state,
specifications, and decisions. For repository-modifying work, reconcile
implementation completion against landing evidence: verified changes must be
committed and reachable from the resolved `Target` before the task may be
treated as completed. Surface contradictions and update shared state that the
work made stale.

### Handoff/Close

Leave the project resumable. Update task state, accountability, and executor as
needed; promote durable knowledge; and remove or replace obsolete transient
information under [Boundary-driven handoffs](#boundary-driven-handoffs).

`Ready to Land` is a task state and a valid session-close condition when
verified work remains unlanded at a session, responsibility, or coordination
boundary. It is not a completed outcome. Persistence MAY be omitted when
landing completes immediately in the same uninterrupted operation, regardless
of who holds landing authority. Lack of authority alone does not require
persisting `Ready to Land` unless it delays or transfers landing. See
[Ready to Land](#ready-to-land).

A session may close as successful, partial, blocked, interrupted, abandoned, or
ready to land. Session closure alone does not require a handoff. An incomplete
session requires handoff state only when both a real boundary and concrete
resumption risk exist.

### Boundary-driven handoffs

A handoff entry is created or updated only when both conditions hold:

1. **Boundary:** execution reaches a real continuity, responsibility,
   impediment, landing, dependency, or collision boundary.
2. **Resumption risk:** without additional transient state, a later agent or
   session would likely repeat meaningful work, proceed incorrectly, miss a
   material risk, overlook a blocking question, or reconstruct costly
   verification.

Neither condition alone is sufficient. Routine session closure, uninterrupted
work, ordinary checkpoints, state changes, and live collisions do not
independently require a handoff when Git, `todo.md`, and canonical project
documents already make continuation safe.

`handoff.md` is a minimum replaceable boundary snapshot of unresolved
resumption risk. It is not continuously synchronized live state and not
chronological history. During uninterrupted execution, agents MUST NOT append
progress narration or rewrite the handoff for routine intermediate changes.
When a new boundary and risk exist, replace the prior snapshot coherently
rather than appending session history.

Reading, claiming, reassigning, or beginning to resume does not consume a
handoff. A handoff is consumed only when its resumption risk is resolved,
superseded, or safely recoverable from canonical repository and project state.
Consumed or obsolete entries are removed, or replaced when a new boundary and
risk require a new snapshot. They MUST NOT be marked completed or retained as
history.

The executor leaving consequential resumable state writes the snapshot after
reconciling Git and `todo.md`. The resumer may be another agent or the same
agent in a later session, and MUST validate critical claims against repository
reality before relying on them. The executor whose work resolves or transforms
the risk removes or replaces the entry; cleanup ownership does not permanently
remain with the author. Age alone never proves staleness.

Outcome-specific behavior:

| Situation | Primary representation | Handoff behavior |
| --- | --- | --- |
| Transfer | `todo.md` reflects the real executor and claim | Create only when non-obvious state or concrete risk must transfer |
| Ready to Land | `todo.md` records `Landing:` and useful `Verification:` | Create only when those fields are insufficient for safe continuation |
| Blocked | `todo.md` records the state and named blocker | Create only when consequential partial state, risk, or an unresolved question must survive |
| Partial / interrupted | `todo.md` preserves honest task state and scope | Create when a later resumer would otherwise proceed incorrectly or repeat meaningful work |
| Collision | `todo.md` coordinates scope, overlap, and sequencing | Create only when the collision forces a boundary and leaves non-obvious partial state |
| Completed | Git and `todo.md` record truthful closure | Remove obsolete task handoff state; create separate transfer state only for an active dependent workstream with concrete risk |

Operational rule:

```text
coordination without boundary + risk -> todo.md
coordination with boundary + risk    -> todo.md and, when needed, handoff.md
```

Document-local creation, content, organization, consumption, and cleanup rules
are in the [`handoff.md` contract](document-contracts.md#handoffmd).

## Git-aware task lifecycle

CSDD declares coordination intent; Git exposes observed execution state. Agents
MUST reconcile both before editing, landing, or closing collaborative
repository work.

### Conceptual states

The canonical progression for repository-modifying work is:

```text
Pending → In Progress → Ready to Land → Recently Completed
```

`Blocked` and `Deferred` are lateral states, not steps that every task must
visit. Canonical `todo.md` heading names, order, secondary grouping, and
retention bounds are normative under [TODO structure and
retention](#todo-structure-and-retention). Document-local field and example
rules live in the [`todo.md` contract](document-contracts.md#todomd).

| State | Meaning |
| --- | --- |
| Pending | Accepted execution-queue work that may be claimed without a new product or prioritization decision once capacity and dependencies permit. No active `Agent` or write claim. |
| In Progress | An agent is executing within an active claim. |
| Ready to Land | Implementation and verification are done; landing has not yet made the work reachable from `Target`. Task state and valid session-close condition; not a completed outcome. |
| Recently Completed | Work is completed under the Git-aware completion rules below. Bounded operational window, not permanent history. |
| Blocked | Progress cannot continue until a named blocker or decision is resolved. |
| Deferred | Accepted, still-relevant work intentionally removed from the execution queue until an observable resume condition is met. No `Agent` and no active claim. |

### Target, Base, and Landed

Work that modifies the repository MUST resolve an integration `Target`.

- `Target` is the integration branch or ref the work is intended to reach.
- `Base` is the commit of that `Target` observed when the task is claimed or
  at the last explicit reconciliation that updated `Base`.
- `Landed` is final landing evidence: a commit, merged pull request, or
  equivalent that makes the verified changes reachable from the resolved
  `Target`.

`Target` MAY be inherited from an unambiguous project policy. It MUST be
written explicitly on the task when the policy is ambiguous, non-standard, or
relevant for coordination.

`Base` MUST be recorded for collaborative Level 2/3 work, when branches or
worktrees are in play, or when concurrency is plausible. `Base` MAY be omitted
for Level 0 work and for Level 1 work with no coordination value. Agents MUST
NOT silently advance `Base` to hide divergence from `Target`. When `Base`
changes, record the reconciliation (for example in `Note` or handoff).

For repository-modifying work, *landed* means the verified changes are
committed and reachable from the resolved integration `Target`. Completed
repository tasks SHOULD record `Landed`. They MUST record `Landed` when
attribution is not obvious from the current tip of `Target` alone.

Editing rules for `todo.md` and `handoff.md` as shared coordination surfaces
are in [document-contracts.md](document-contracts.md#shared-coordination-surfaces).
Those documents are not automatically part of a task's principal write `Scope`.

### Ready to Land

`Ready to Land` is a canonical task state. It may also describe how a session
closes when verified work remains unlanded. It is never a completed outcome.

Persistence MAY be omitted when implementation, verification, and landing
complete immediately in the same uninterrupted operation, regardless of who
holds landing authority.

Persistence MUST occur when verified work remains unlanded at a session,
responsibility, or coordination boundary—including interruption, transfer, or
delayed landing. Lack of landing authority obligates persistence only when that
lack delays or transfers landing; authority alone does not.

A persisted Ready to Land task remains active and unchecked. It MUST retain
honest coordination metadata required by this lifecycle, including `Agent`,
protected `Scope`, `Target`, `Base`, and `Updated` when those fields apply.
`Agent` identifies the current operational executor responsible for the task
and MAY change when landing responsibility is genuinely transferred or
reclaimed; a separate landing-owner field is not introduced.

A persisted Ready to Land task:

- MUST include `Landing:` with the pending PR, commit, action, or landing path;
- SHOULD include concise `Verification:` evidence;
- MUST preserve enough verification state in the task so landing does not
  require unnecessary repeated work; create or update `handoff.md` only when
  `Landing:` and `Verification:` are insufficient for safe continuation under
  [Boundary-driven handoffs](#boundary-driven-handoffs);
- MUST NOT use `Landed:`, because the changes are not yet reachable from
  `Target`.

After landing satisfies the completion rules, the task moves to Recently
Completed, becomes checked, records `Landed:` when required, releases active
Scope, and compacts completed metadata.

### Refresh checkpoint

Before writing to a claimed repository `Scope` when Level 2/3 collaboration,
branch/worktree use, or plausible concurrency applies, and again before
landing or closure, after a material HEAD or `Target` change, when resuming a
material interruption, or when unexpected changes appear in `Scope`, agents
MUST:

1. re-read the relevant task entry;
2. run `git status --short`;
3. compare recorded `Base` with the current tip of `Target`;
4. inspect diff or log for `Scope` only when that comparison shows divergence
   or status shows unexpected changes; and
5. reconcile or block before proceeding with the pending write, landing, or
   closure.

Do not expand the checkpoint into a full repository survey when status is clean
and `Base` still matches the `Target` tip.

### Minimal Git contract

Agents MUST NOT stage or commit files outside the claimed `Scope`, except for
minimal coherent patches to `.csdd/todo.md` and `.csdd/handoff.md` made under
the [shared coordination-surface
contract](document-contracts.md#shared-coordination-surfaces). Any other file
outside `Scope` requires explicit reconciliation that expands or coordinates
that scope. Commits primarily associated with one task SHOULD include the task
ID in the subject or a trailer (for example `T-018` or `Task: T-018`).

### Illustrative landing shapes

These examples show evidence shapes; they do not invent alternate lifecycles.

- **Direct commit to `Target`:** claim with `Target`/`Base`; after verify and
  commit on `Target`, the task may move to Recently Completed without a
  persisted Ready to Land; record `Landed` according to the rules above.
- **Feature branch:** implement on a branch; when verified but unmerged at a
  session boundary, persist Ready to Land; land by merging so changes are
  reachable from `Target`.
- **Open PR / merged PR:** an open PR can evidence Ready to Land; a merged PR
  (or equivalent) can evidence `Landed` once the merge is reachable from
  `Target`.
- **Worktree with dirty overlap:** refresh shows foreign dirty files in
  `Scope` or another worktree claim; surface overlap and reconcile or block
  before writing. Do not silently reclaim or overwrite.

Cross-worktree discovery and divergence classes remain in [Branch and worktree
baseline
reconciliation](#branch-and-worktree-baseline-reconciliation).

### Authority and permission

Claiming or progressing a task does not imply permission to commit, push, or
merge. Landing authority remains a separate human, project, or harness policy.

### Blocked and Deferred

`Blocked` retains `Scope` only when partial work or safe continuation needs
protection. Otherwise it MUST release `Scope` and explain why retention is
unnecessary. Named blockers stay in `todo.md`. Create or update `handoff.md`
only when consequential partial state or concrete resumption risk must survive
under [Boundary-driven handoffs](#boundary-driven-handoffs); do not invent a
second scope-release rule beyond [Completed-task
claims](document-contracts.md#completed-task-claims) and the closing behavior
below.

`Deferred` contains accepted and still-relevant work intentionally removed
from the execution queue until an observable resume condition is met.
Deferral requires evidence from the user, Owner, accepted planning, or another
authoritative project source. An agent MUST NOT defer work autonomously merely
because it is difficult, old, blocked, unfinished, or inconvenient.

Every Deferred task MUST include:

- `Reason:` explaining why execution is postponed now;
- `Resume when:` naming an observable event, dependency state, decision, or
  planning boundary that makes the task eligible again.

Conditions such as “later”, “when appropriate”, or “when there is time” are
not sufficient.

Deferred tasks MAY retain `Owner`. They MUST NOT have an `Agent`, MUST omit
active Scope or use `Scope: released`, and MUST NOT conceal partial or
unlanded repository changes. If partial work needs protection, the honest
state is normally Blocked rather than Deferred. When a resume condition is
known to be satisfied, reconcile the task into Pending or directly into In
Progress when claimed in the same operation.

`Icebox` is not a canonical state alias. Rejected, cancelled, obsolete,
speculative, or irrelevant work is removed from `todo.md` after promoting any
consequential truth. A rejected alternative belongs in `decisions.md` only
when its rationale is durable and likely to prevent repeated debate.

### TODO structure and retention

Every `todo.md` MUST contain these six H2 headings, including when empty, in
this exact order:

1. `## In Progress`
2. `## Ready to Land`
3. `## Blocked`
4. `## Pending`
5. `## Deferred`
6. `## Recently Completed`

H2 headings under `# TODO` are reserved for canonical task state. Projects and
agents MUST NOT omit, rename, reorder, alias, or add state H2 headings. Every
task present in `todo.md` MUST appear under exactly one canonical state H2.
Active and lateral states use unchecked task items; Recently Completed uses
checked task items.

State is always the primary grouping dimension. The default presentation is
flat. A task MAY use an optional `Workstream:` field when thematic context
materially improves coordination. Projects MAY instead adopt H3 workstream
grouping as an explicit opt-in; an agent MUST NOT introduce or switch grouping
modes autonomously. When H3 grouping is used, H3 headings are thematic only
and never express task state; Recently Completed remains flat. Exact H3
interoperability rules are in the [`todo.md`
contract](document-contracts.md#todomd).

Pending is the accepted execution queue. Pending tasks have no active `Agent`
or write claim, MAY name dependencies, are not Blocked merely because an
unstarted dependency remains, and MUST NOT be created from speculative ideas
without evidence that the work was accepted. Age alone does not authorize an
agent to remove or defer Pending work.

Recently Completed is a bounded operational window, not permanent history.
Directly under `## Recently Completed`, the project declares `Retention: N`.
The v0.2 default is `Retention: 5`. If the line is absent in an older project,
agents MUST use five as the fallback until migration. `N` is a positive
integer (`N >= 1`) and applies globally. `Retention: 0` is invalid. A human
or explicit project policy MAY change it; agents MUST NOT increase it
autonomously to avoid compaction.

Recently Completed remains flat, is ordered newest first, retains entries
until they exceed the declared limit, does not permit subjective early
removal, and does not support pinned entries. When a task completes, the
closing agent MUST, in the same coherent TODO patch: insert it at the top;
update `Updated` to the completion transition date; compact metadata that no
longer serves operational coordination; and remove the oldest entries that
exceed `Retention`. An agent modifying Recently Completed MUST reconcile an
existing overflow. An agent editing an unrelated state section is not
required to audit retention.

Retention removal is eviction from the operational view, not a new lifecycle
state. It MUST NOT create an `Archived` state, MUST NOT mechanically copy the
task into `.csdd/archive/`, and MUST NOT authorize reuse of its stable task
ID. Durable truth SHOULD be promoted during task closure. Routine compaction
does not require historical archaeology; Git, pull requests, and issues remain
the sources for exact implementation history.

### Completion

A repository-modifying task MAY move to `Recently Completed` only when all of
the following hold:

1. the result has been verified in proportion to risk;
2. the verified changes are reachable from the resolved `Target`;
3. no unlanded task changes and no unresolved unattributed changes remain
   inside `Scope`;
4. active write `Scope` is released (`Scope: released` or omitted when
   compacted);
5. obsolete handoff state for the task is removed or replaced; and
6. `Landed` is recorded when required by the Landed rules above.

Work that awaits required review or landing remains active—typically
`Ready to Land` or `In Progress`—even when implementation appears finished.
Non-repository work may complete without Git landing evidence when no
repository change was in scope.

## Initial skill operational contract

The initial CSDD skill is a concise operational router over this protocol and
the document contracts. It tells an agent how to recognize a CSDD project,
select the minimum useful context, coordinate work, persist consequential
state, and close honestly. It does not duplicate the detailed protocol in
`SKILL.md`.

### Applicability and bootstrap

The skill is applicable when either:

- the repository contains the canonical `.csdd/` project-state documents; or
- the user or project instructions explicitly require CSDD.

An existing `.csdd/` is sufficient evidence that work in that repository is
CSDD-aware, but not that every task requires reading CSDD documents. If CSDD is
explicitly requested but the canonical state is missing or malformed, the
agent MUST surface that condition and follow the requested initialization or
repair scope; it MUST NOT silently invent an alternative layout. Without
either signal, the skill need not enter the CSDD lifecycle.

Bootstrap SHOULD inspect repository status, project instructions, the `.csdd/`
shape, and the task's apparent target before hydrating project state. This is
discovery, not permission to read every available document.

### Context classification and read routing

Classify the task using [Adaptive context hydration](#adaptive-context-hydration)
before reading CSDD state, and increase the level when new evidence raises
scope, ambiguity, continuity, or collision risk. Use this initial routing:

| Level | Initial CSDD route |
| --- | --- |
| 0 - direct | No CSDD document is required. |
| 1 - local awareness | Inspect relevant active scope in `todo.md` when overlap is plausible. |
| 2 - operational | Inspect relevant hot context, then applicable warm context. |
| 3 - deep | Inspect relevant hot and warm context; use cold context only on demand. |

The authoritative document-specific read policies are in
[document-contracts.md](document-contracts.md). In particular, `handoff.md` is
read when relevant boundary transfer state with concrete resumption risk may
exist, while `specs.md` and `decisions.md` are loaded only when their
documented behavioral, contractual, or decision triggers apply. Follow
[Optional archive and cold history](#optional-archive-and-cold-history) for any
historical access.

### Ownership, overlap, and claiming

Apply the [Concurrency model](#concurrency-model) before writing in plausible
shared scope: inspect active work, compare intended path and contract scope,
claim coordination-sensitive work, and do not edit an apparent overlap until
it is surfaced and coordinated. When another branch or worktree may hold
relevant claims or durable truth, apply [Branch and worktree baseline
reconciliation](#branch-and-worktree-baseline-reconciliation). Use the
`todo.md` contract for task structure and claim triggers. Questionable
ownership follows C6 and the document contract's stale-claim procedure; the
operational contract does not define a second reclamation rule.

### Execution, persistence, and reconciliation

The skill fast path should require the agent to:

1. stay within the claimed or requested scope, updating it when material scope
   changes;
2. validate assumptions against repository reality and verify the result in
   proportion to risk;
3. update `todo.md` when state, scope, executor, dependency, blocker, or a
   continuity-critical checkpoint materially changes;
4. preserve validated consequential knowledge in its canonical document, not
   as an activity log; and
5. surface and reconcile material contradictions instead of choosing code or
   documentation automatically.

The authoritative persistence triggers and document boundaries are in
[document-contracts.md](document-contracts.md). Apply [Knowledge promotion and
expiration](#knowledge-promotion-and-expiration) to validated findings,
[Contradiction and reconciliation](#contradiction-and-reconciliation) to
conflicting evidence, and [Boundary-driven
handoffs](#boundary-driven-handoffs) with the `handoff.md` contract when both a
real boundary and concrete resumption risk exist. These references define the
detailed rules; the list above is the operational sequence.

Promote consequential knowledge to one canonical durable document. Cross-link
related requirements and decisions instead of duplicating normative truth.

### Closing behavior

Every close verifies what actually happened and leaves operational state
truthful. Treat work awaiting required review, acceptance, or landing as
active rather than completed, even when implementation is finished. Apply the
outcome-specific minimum and the [Git-aware task
lifecycle](#git-aware-task-lifecycle) completion rules.

`Ready to Land` in the table below is a session-close condition that leaves the
task in the Ready to Land state. It is not a completed outcome.

| Close condition | Required close |
| --- | --- |
| Completed | Verify the result; for repository-modifying work, confirm the changes are landed and reachable from `Target`, with no unlanded task changes and no unresolved unattributed changes remaining inside `Scope`; record `Landed` when required; reconcile repository and durable docs; move or mark the task completed and release active scope; remove obsolete handoff state. Create a handoff only when a separate active dependent workstream has its own concrete transfer risk. |
| Ready to Land | Persist the Ready to Land task state when verified work remains unlanded at a session, responsibility, or coordination boundary; keep the claim honest; update `handoff.md` only when `Landing:` and `Verification:` are insufficient for safe continuation. Omit task persistence only when landing completes in the same uninterrupted operation. |
| Partial | Keep the task honestly active with current scope and a useful checkpoint; update `handoff.md` only when both a boundary and concrete resumption risk exist. |
| Blocked | Move or mark the task blocked and name the blocker or decision needed in `todo.md`; update `handoff.md` only for consequential partial state or concrete resumption risk; retain `Scope` only when partial work or safe continuation needs protection, otherwise release it and explain why. |
| Interrupted | Record an honest active checkpoint in `todo.md`; create or update `handoff.md` only when concrete resumption risk must survive; if implementation is finished but unlanded, close as Ready to Land rather than implying completion; do not retain a misleading claim. |
| Trivial | Verify the change. Do not create a task, handoff, decision, archive entry, or other CSDD update unless the work discovered a material conflict or changed durable truth. |

For all close conditions, promote consequential knowledge before removing
transient state. Do not leave completed ownership claims active, duplicate
facts across documents, or preserve routine session narration.

At closure, release active claims when the Git-aware rules require it, preserve
human accountability, and compact operational metadata without rewriting
execution history. Stale-claim and cross-worktree procedures remain those in
the [Concurrency model](#concurrency-model) and [Branch and worktree baseline
reconciliation](#branch-and-worktree-baseline-reconciliation); this section
does not redefine them.

### `SKILL.md` and progressive references

`SKILL.md` SHOULD contain only the operational fast path:

- applicability signals and canonical `.csdd/` discovery;
- the context-level classifier and minimal read-routing table;
- the essential orient, overlap-check, claim, execute, reconcile, and close
  sequence;
- concise persistence routing for task, handoff, specification, and decision
  state;
- non-negotiable guards against unconditional hydration, silent overlap,
  silent contradiction, stale claims, and unnecessary archive access; and
- links that identify which reference section to load when more detail is
  required.

Detailed protocol knowledge remains in `references/` and is loaded
progressively. This document owns principles, full lifecycle semantics
including the Git-aware task lifecycle, hydration rationale, concurrency and
stale-claim handling, branch and worktree baseline reconciliation,
contradiction resolution, knowledge promotion, archive policy, limitations, and
validation scenarios.
[document-contracts.md](document-contracts.md) owns exact document boundaries,
read and update triggers, aging, cross-document movement, examples,
branch/worktree locality evidence, and archive-entry structure. Templates
remain in `assets/templates/`.

An agent SHOULD load only the referenced section needed for the current
decision. It SHOULD consult document contracts before making a non-obvious
document update or resolving a boundary or aging question, and consult the
deeper protocol sections for collaborative, conflicting, stale, branch/worktree,
or historical cases. The skill MUST remain usable for levels 0 and 1 without
forcing either reference to be read in full.

## Concurrency model

CSDD coordination is document-based and intentionally lightweight.

### Minimum interoperable task structure

Tasks MUST use plain, human-readable Markdown. Each task requires a stable task
ID, a concise title, and a state represented by placement under exactly one
canonical state H2. See [TODO structure and
retention](#todo-structure-and-retention).

```markdown
## In Progress

- [ ] T-004 — Define document templates
```

Active collaborative tasks SHOULD identify `Owner`, `Agent`, `Scope`, and
`Updated` when those fields help coordination. Repository-modifying tasks
follow the `Target`, `Base`, and `Landed` rules in [Git-aware task
lifecycle](#git-aware-task-lifecycle). `Depends on`, `Blocked by`, and a short
`Note` MAY be added when relevant. Trivial tasks MAY omit all ownership
metadata.

```markdown
- [ ] T-021 — Implement password recovery
  - Owner: valen
  - Agent: codex/auth-reset
  - Scope: `src/auth/reset-password/**`
  - Target: `main`
  - Base: `a1b2c3d`
  - Updated: 2026-07-12
```

`Owner` identifies the accountable human or team and preferred coordination
point. `Agent` identifies the current operational executor or harness/task
label. Reassigning execution does not necessarily change human accountability.
Both fields are advisory labels, not authenticated identities. CSDD v0 MUST NOT
attempt automatic human identity discovery and SHOULD prefer human-readable
labels over provider-specific identifiers.

A claim still does not authorize commit, push, or merge.

CSDD does not require story points, completion percentages, mandatory
priorities, risk scores, complex labels, redundant timestamps, or mandatory
reviewer fields. V0 MUST NOT require YAML front matter, JSON, a database, a
machine schema, or harness-specific metadata.

### C1 - Read active ownership before writing when overlap is plausible

Before non-trivial work, inspect relevant active entries in `.csdd/todo.md` when
the target scope could overlap. A trivial, clearly unrelated edit does not
require a coordination scan. Compare both path scope and affected contracts;
semantically overlapping contracts may conflict even when file globs differ.
When another worktree or branch may hold relevant claims or overlapping dirty
state, extend the scan per [Branch and worktree baseline
reconciliation](#branch-and-worktree-baseline-reconciliation).

### C2 - Claim explicit scope when collaborative work requires ownership

A task SHOULD be claimed before editing when it is non-trivial and explicit
scope would reduce collision or continuity risk. Do not claim trivial isolated
work when coordination overhead would exceed that risk.

A claim SHOULD name concrete files, directories, modules, contracts, or another
boundary that lets an agent judge overlap. Scope is usually more useful for
collision detection than agent identity. Prefer `src/auth/**` and
`tests/auth/**` over a vague label such as `backend`.

### C3 - Single writer per overlapping scope by default

One operational executor for overlapping write scope is the safe default. This
is not an absolute prohibition on shared work; it is a bias toward avoiding
accidental conflict.

### C4 - Overlap must be intentional, never silent

When overlapping work is necessary, the agents or operator MUST surface it,
agree on boundaries or sequencing, and reflect the coordination state where a
later agent can see it.

### C5 - Durable decisions cannot be silently reversed

Agents MUST NOT silently reverse durable decisions. An agent changing an
accepted direction MUST acknowledge the active decision and explicitly
supersede it or surface the proposed change for resolution.

### C6 - Ownership claims can become stale

Claims can become stale when execution ends, work is abandoned or completed
without reconciliation, a task moves environments, or repository state changes
independently. Claims are soft coordination state, not distributed locks. CSDD
does not guarantee exclusive access, liveness, atomic claims, synchronization,
or reliable lease expiration.

The authoritative evidence and reclamation procedure is the `todo.md`
[stale-claims contract](document-contracts.md#stale-claims). It defines how to
assess `Updated`, consult ownership, inspect repository evidence, and record any
reassignment or release; this conceptual rule does not create a second lease or
reclamation mechanism.

Claims in `.csdd/todo.md` are not repository-global locks. Agents that do not
observe the same version of the document—because they work on another branch,
worktree, or unmerged commit—cannot be assumed to see or honor that claim.
Cross-worktree evidence is therefore part of stale-claim and overlap assessment
when concurrency outside the current baseline is plausible. See [Branch and
worktree baseline reconciliation](#branch-and-worktree-baseline-reconciliation).

## Branch and worktree baseline reconciliation

`.csdd/` is versioned, branch-local state. The current worktree is the
operational baseline for reading and writing CSDD documents, but it is not proof
that other worktrees or branches lack relevant claims, handoffs, or durable
truth.

CSDD does not introduce a global lock service, shared configuration file, or
out-of-band synchronization channel. Coordination remains artifact-based. When
branches or worktrees diverge, agents MUST reconcile explicitly rather than
silently copy, concatenate, merge, release, or overwrite CSDD state.

### When cross-worktree inspection is required

Cross-worktree or cross-branch inspection is mandatory only when concurrency,
stale claims, scope overlap, or durable-truth divergence could change the
decision to claim, reclaim, resume, or implement. Routine Level 0 work that is
explicitly local and unrelated does not require a worktree scan merely because
`.csdd/` exists.

Age of a branch, worktree, or claim is a signal, never sufficient proof that
work is abandoned or that another baseline is safe to ignore.

### Procedure

Use this sequence when the trigger applies:

```text
Trigger -> Discover -> Compare -> Classify -> Reconcile or block -> Execute -> Close
```

1. **Trigger.** Enter this procedure before claiming, reclaiming, or editing
   overlapping scope when another branch or worktree may hold relevant CSDD
   state or conflicting implementation; when resuming work that may have moved
   baselines; or when `specs.md` / `decisions.md` may diverge from the intended
   coordination baseline.
2. **Discover.** Inspect the current worktree baseline, then relevant other
   worktrees and branches: checked-out refs, clean or dirty status, uncommitted
   changes inside the requested or claimed scope, recent commits touching
   `.csdd/` or the implementation scope, and any visible handoff or ownership
   evidence. Prefer targeted inspection over exhaustive repository enumeration.
3. **Compare.** Diff the current `.csdd/` documents and relevant code against
   the candidate baseline. Note whether divergence is limited to operational
   coordination (`todo.md`, `handoff.md`), durable truth (`specs.md`,
   `decisions.md`), implementation artifacts, or a combination.
4. **Classify.** Assign one primary class (combine only when needed for
   clarity):

   | Class | Meaning | Default action |
   | --- | --- | --- |
   | No material divergence | Other baselines do not change claim, resume, or implementation decisions | Proceed on the current worktree baseline |
   | Coordination-only divergence | Claims or handoffs differ; durable truth agrees | Preserve live compatible claims, block on live conflict, or explicitly reclaim/supersede stale operational state |
   | Durable-truth divergence | Material differences in `specs.md` or `decisions.md` | Reconcile or block before implementing dependent behavior |
   | Live conflicting work | Another worktree or branch shows active overlapping execution | Surface overlap; coordinate, sequence, or block; do not silently reclaim or overwrite |

   Uncommitted changes inside a conflicting claimed scope are strong evidence of
   live conflicting work. A worktree's mere existence, or an old claim timestamp
   alone, is not.
5. **Reconcile or block.** Choose an explicit path: merge, rebase, cherry-pick,
   or manual reconciliation of the intended CSDD and code baseline; or mark the
   task blocked with the decision needed. Do not silently import or overwrite
   divergent state. Reconciling the current branch MUST NOT silently modify or
   release claims that exist only in another branch or worktree. Preserve
   `Owner` unless human accountability is explicitly reassigned; update `Agent`
   only when this agent assumes execution. When importing or superseding CSDD
   state from another branch, record the source branch or commit when that
   provenance aids recovery.
6. **Execute.** After the baseline is coherent—or after intentional overlap is
   recorded—claim or resume only on the reconciled current-worktree state,
   stay within scope, and apply ordinary concurrency and contradiction rules.
7. **Close.** Leave truthful task state on the current baseline. Release active
   write scope when complete. Do not imply that another worktree's claims were
   cleared unless that worktree's documents were explicitly updated. Clear or
   update handoff only when both a real boundary and concrete resumption risk
   require it on this baseline.

Document-contract detail for locality, evidence, and provenance lives in
[Branch and worktree locality](document-contracts.md#branch-and-worktree-locality).

### Examples

- **No material divergence:** Only this worktree exists; `.csdd/` and the
  implementation scope match the intended baseline. Proceed without ceremony.
- **Coordination-only divergence:** Another branch has an older completed claim
  for the same files, while `specs.md` agrees. Reconcile operational state
  explicitly if needed, then claim on the current baseline without rewriting
  the other branch's history.
- **Durable-truth divergence:** `decisions.md` on `feature/auth` accepts a
  different session model than `main`. Block or reconcile the decision before
  implementing auth behavior that depends on it.
- **Live conflicting work:** A second worktree is checked out on an active task
  branch with dirty files under the same `Scope`. Surface the overlap to the
  `Owner` or coordinate sequencing; do not reclaim silently because the claim
  looks old on this baseline.

## Contradiction and reconciliation

CSDD artifacts are authoritative statements of project state, but they are not
infallible. Repository reality is evidence, but implementation accidents are
not automatically project intent.

When an agent finds a material conflict, it MUST surface it and SHOULD:

1. identify the conflicting claims and the affected scope;
2. inspect enough evidence to determine whether one side is stale, incorrect,
   or part of an incomplete transition;
3. avoid expanding or overwriting the conflict while it is unresolved;
4. reconcile the appropriate document and repository state, or record a
   blocker and the decision required;
5. preserve rationale in `decisions.md` when resolution changes a
   consequential direction.

This process is proportional to impact. A harmless wording mismatch does not
require the ceremony of an architectural conflict.

## Knowledge promotion and expiration

Session observations begin in L3 and are not durable by default. Promote one
only after it is sufficiently validated and its loss could harm later work:

`temporary observation -> validated finding -> specification or decision`

Use `specs.md` when the finding describes what must remain true. Use
`decisions.md` when it records a consequential choice and why. Use `todo.md`
when the information changes active work, and `handoff.md` only when both a
real boundary and concrete resumption risk require transient transfer state.

Transient state should expire when it is completed, disproven, superseded, or
no longer useful for resumption. Promotion must not mean copying the same fact
into every document; keep one canonical home and link when necessary.

## Optional archive and cold history

A project MAY omit `.csdd/archive/`. When present, the directory is standardized
cold context and SHOULD contain `index.md`. Agents MUST NOT load archive
contents during default hydration.

Archive access is justified only when current state or a concrete question
requires a historical outcome, rationale, prior experiment, or milestone
context that Git and current documents do not answer efficiently. Inspect the
archive index first when available, then open only the relevant entry. Routine
orientation, task completion, and curiosity are not sufficient reasons to read
or create archive content.

Archive entries SHOULD be separate, meaningfully named Markdown files organized
around a phase, milestone, experiment, migration, or workstream. They MUST NOT
be created for every agent session. A monolithic, indefinitely growing
`history.md` SHOULD NOT be used because it recreates the accumulation problem
CSDD is intended to prevent.

> Preserve semantic project history, not chronological activity exhaust.

An entry SHOULD summarize the objective, relevant outcome, consequential
discoveries, important rejected or deferred approaches, unresolved concerns,
related decisions, and useful task or Git references. It SHOULD NOT preserve
complete transcripts, full reasoning, every command or failed attempt, every
transient hypothesis, or a mechanical copy of `todo.md`.

At the end of a meaningful phase or milestone, historical context MAY be
distilled into an archive entry. Durable requirements MUST remain in `specs.md`,
durable decisions MUST remain in `decisions.md`, and current work MUST remain in
`todo.md`. Git remains the source for exact file history; the archive preserves
selected project meaning.

## Planned validation scenarios

Phase 0 defines five scenarios for dogfooding and later conformance tests:

1. a trivial isolated rename proceeds without CSDD hydration;
2. one agent starts a feature and a fresh agent resumes it later;
3. two agents attempt to work in overlapping scopes;
4. a new agent identifies and reconciles a stale claim;
5. a completed phase is distilled from live state into cold archive context.

Together these scenarios exercise adaptive hydration, continuity, document
boundaries, overlap handling, advisory ownership, stale-claim reconciliation,
branch and worktree baseline awareness, semantic archival, and proportional
overhead.

Future evaluations may separate a fixture author, isolated subject agent,
evaluator agent, and human reviewer. Evaluation SHOULD compare actual repository
state and diffs rather than trust only the subject agent's self-report.
Structured run reports are preferred, and full transcripts SHOULD NOT be
preserved by default. Phase 0 defines no evaluation infrastructure.

## Trade-offs and limitations

CSDD exchanges a small amount of document maintenance for faster, safer context
reconstruction. Its effectiveness depends on agents and operators keeping the
relevant state honest and scoped. Text files cannot provide atomic claims,
guarantee fresh ownership, prevent conflicting writes, synchronize every
worktree automatically, or resolve ambiguous project intent without judgment.
Because `.csdd/` is branch-local, claims are advisory only for observers of that
document version; cross-worktree reconciliation remains an explicit agent
responsibility when concurrency is material.

The protocol is harness-agnostic and requires no runtime service, global lock
file, or shared configuration channel. That keeps it portable and inspectable,
but it also means v0 offers conventions rather than enforcement. Git, tests,
code review, and human escalation remain necessary.

## Open design questions

The following questions remain for dogfooding or later tasks:

- Which `Agent` label conventions remain portable across Codex, Cursor, Claude
  Code, and future harnesses?
- Which normative statements should be promoted from SHOULD to MUST after
  real-world testing?
- Will one `.csdd/handoff.md` remain practical under concurrent editing?
- Does the archive model remain useful without becoming redundant with Git and
  durable project documents?
