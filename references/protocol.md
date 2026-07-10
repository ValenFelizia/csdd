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

- `todo.md`;
- `handoff.md`.

Hot context is the first candidate for project or collaborative work, but a
trivial isolated task may need neither file.

### Warm context

Durable and slower-changing:

- `specs.md`;
- `decisions.md`.

Agents load only the sections relevant to the task.

### Cold context

Historical material kept for occasional recovery or investigation:

- an optional `archive/`;
- relevant Git history.

Cold context is never part of default context hydration. It is consulted only
when current state points to it or the task requires historical explanation.

## Core project-state documents

CSDD v0 separates state across four primary documents:

| Document | Context layer | Primary responsibility |
| --- | --- | --- |
| `specs.md` | L1 | Durable requirements, constraints, invariants, and contracts |
| `decisions.md` | L1 | Consequential choices, rationale, consequences, and supersession |
| `todo.md` | L2 | Current work, ownership, scope, dependencies, and blockers |
| `handoff.md` | L2 | Minimum current transfer state for resuming incomplete work |

`todo.md` is the coordination authority for active work and overlap detection.
`handoff.md` is the transfer surface for the current or next session. A handoff
may refer to a task, but it must not become a parallel task tracker.

The detailed boundaries, read policies, update triggers, and aging rules are
defined in [document-contracts.md](document-contracts.md). The protocol defines
conceptual responsibilities, not a mandatory Markdown schema.

## Principles

### P1 - Agents are ephemeral; project state is durable

Critical project state must not exist exclusively in chat history. Durable does
not mean immutable: state must remain updateable as the project changes.

### P2 - Persist consequential knowledge, not activity

Persist what would hurt another agent to lose. Do not record every command,
edit, failed experiment, or trivial implementation choice.

Knowledge is consequential when its loss could cause duplicated work,
conflicting implementation, repeated investigation, architectural regression,
or an unsafe assumption.

### P3 - Minimum sufficient context

An agent should load the smallest amount of project state that allows it to act
correctly and safely. More available context is not automatically better
context.

### P4 - Separate state by purpose and lifetime

Requirements, work state, decisions, handoffs, operator preferences, and
session notes have different owners and aging rules. They must not be collapsed
into one accumulating document.

### P5 - Current state over accumulated history

The default operational view must describe the project now. Historical value
may be retained as cold context, but it must not burden routine agent startup.

### P6 - Explicit coordination over inferred coordination

Active work must expose enough ownership, scope, status, and dependency
information for another agent to detect likely overlap. Agents must not assume
that silence means a scope is free.

### P7 - No silent contradiction

When repository evidence, specifications, decisions, or active work conflict,
an agent must surface and reconcile the conflict rather than silently overwrite
one side.

### P8 - Documentation is project state, not unquestionable reality

CSDD documents are authoritative statements of project intent and coordination,
but they can become stale. Conflicting repository evidence must be investigated;
neither documentation nor code wins automatically.

### P9 - Durable knowledge should be promoted; transient knowledge should expire

Validated knowledge should move to the document whose lifetime matches it.
Temporary observations should be removed, replaced, or promoted when they stop
being current.

### P10 - Context loading must be proportional to task need

CSDD must not require unconditional project-state hydration. Agents should
escalate context only when scope, uncertainty, dependencies, behavioral impact,
or possible overlap demand it.

### P11 - Coordination overhead must not exceed task complexity

The protocol must not make a trivial change more expensive than the change
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
identified text replacement.

Flow: inspect target -> execute -> verify.

Do not read or update CSDD documents unless the target reveals broader impact.

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
the task.

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

Reconstruct minimum sufficient context. Inspect current handoff and work state
as needed, then load only relevant specifications and decisions.

### Claim/Plan

For concurrent or continuity-sensitive work, identify the task, owner, intended
scope, dependencies, and likely overlap before editing.

### Execute

Perform the work. Preserve consequential discoveries, but do not turn shared
documents into an activity log. Checkpoints are warranted when work becomes
partial, blocked, materially different in scope, or important to concurrent
agents.

### Reconcile

Compare the resulting repository state, verification results, task state,
specifications, and decisions. Surface contradictions and update shared state
that the work made stale.

### Handoff/Close

Leave the project resumable. Update task status and ownership, preserve partial
state and unresolved risks, promote durable knowledge, and remove or replace
transient information.

A session may close as successful, partial, blocked, interrupted, or abandoned.
An incomplete session still requires a usable checkpoint when continuity would
otherwise be lost.

## Concurrency model

CSDD coordination is document-based and intentionally lightweight.

### C1 - Read active ownership before writing when overlap is plausible

Before non-trivial work, inspect relevant active entries in `todo.md` when the
target scope could overlap. A trivial, clearly unrelated edit does not require a
coordination scan.

### C2 - Claim explicit scope when collaborative work requires ownership

A claim should name concrete files, directories, modules, contracts, or another
boundary that lets an agent judge overlap. Prefer `src/auth/**` and
`tests/auth/**` over a vague label such as `backend`.

### C3 - Single writer per overlapping scope by default

One owner for overlapping write scope is the safe default. This is not an
absolute prohibition on shared work; it is a bias toward avoiding accidental
conflict.

### C4 - Overlap must be intentional, never silent

When overlapping work is necessary, the agents or operator must surface it,
agree on boundaries or sequencing, and reflect the coordination state where a
later agent can see it.

### C5 - Durable decisions cannot be silently reversed

An agent changing an accepted direction must acknowledge the active decision
and explicitly supersede it or surface the proposed change for resolution.

### C6 - Ownership claims can become stale

Claims can become stale after interruption or abandonment. Metadata such as
`owner`, `claimed_at`, and `last_checkpoint` may provide evidence, but CSDD v0
does not define a universal timeout or automated lease algorithm. Age is a
signal to investigate, not permission to silently seize scope.

## Contradiction and reconciliation

CSDD artifacts are authoritative statements of project state, but they are not
infallible. Repository reality is evidence, but implementation accidents are
not automatically project intent.

When an agent finds a material conflict, it should:

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
when the information changes active work, and `handoff.md` when it is needed to
resume the current partial state.

Transient state should expire when it is completed, disproven, superseded, or
no longer useful for resumption. Promotion must not mean copying the same fact
into every document; keep one canonical home and link when necessary.

## Optional archive and cold history

A project may preserve concise semantic history under a location such as
`.csdd/archive/` when removing it from hot or warm documents would otherwise
lose useful explanation. An archive is optional in v0, never a fifth primary
document, and never part of default hydration.

Git remains the source for exact file history. A CSDD archive, if adopted,
would instead preserve selected project meaning such as prior phases,
superseded directions, or abandoned work whose rationale remains useful.

The protocol deliberately leaves archive layout, retention rules, and promotion
thresholds open until real project use demonstrates that the added surface area
is worthwhile.

## Trade-offs and limitations

CSDD exchanges a small amount of document maintenance for faster, safer context
reconstruction. Its effectiveness depends on agents and operators keeping the
relevant state honest and scoped. Text files cannot provide atomic claims,
guarantee fresh ownership, prevent conflicting writes, or resolve ambiguous
project intent without judgment.

The protocol is harness-agnostic and requires no runtime service. That keeps it
portable and inspectable, but it also means v0 offers conventions rather than
enforcement. Git, tests, code review, and human escalation remain necessary.

## Open design questions

Phase 0 intentionally leaves these questions unresolved:

- Should v0 recommend `.csdd/` as the default location for the four primary
  documents, allow project-root files, or define only discovery rules?
- Is an optional archive useful enough to standardize, and if so, what minimum
  retention and indexing rules keep it cold and discoverable?
- Which ownership metadata is worth recommending without implying a reliable
  distributed lease?
- How should multiple agents reconcile a stale claim when its owner cannot be
  contacted?
- What is the smallest interoperable document structure that remains readable
  to humans and diverse agent harnesses?
- Which protocol statements should become normative requirements after the
  conceptual model has been exercised on real projects?
