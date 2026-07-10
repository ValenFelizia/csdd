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
| `.csdd/handoff.md` | L2 | Minimum current transfer state for resuming incomplete work |

`todo.md` and `handoff.md` MUST preserve distinct responsibilities. `todo.md` is
the primary coordination surface for active work and overlap detection.
`handoff.md` transfers current resumable working state; it is not the primary
collision-prevention mechanism or a parallel task tracker.

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

For concurrent or continuity-sensitive work, identify the task, human `Owner`,
executing `Agent`, intended scope, dependencies, and likely overlap before
editing when those fields are relevant.

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

Leave the project resumable. Update task state, accountability, and executor as
needed; preserve partial state and unresolved risks; promote durable knowledge;
and remove or replace transient information.

A session may close as successful, partial, blocked, interrupted, or abandoned.
An incomplete session still requires a usable checkpoint when continuity would
otherwise be lost.

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
for continuation or consequential partial state, while `specs.md` and
`decisions.md` are loaded only when their documented behavioral, contractual,
or decision triggers apply. Follow [Optional archive and cold
history](#optional-archive-and-cold-history) for any historical access.

### Ownership, overlap, and claiming

Apply the [Concurrency model](#concurrency-model) before writing in plausible
shared scope: inspect active work, compare intended path and contract scope,
claim coordination-sensitive work, and do not edit an apparent overlap until
it is surfaced and coordinated. Use the `todo.md` contract for task structure
and claim triggers. Questionable ownership follows C6 and the document
contract's stale-claim procedure; the operational contract does not define a
second reclamation rule.

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
conflicting evidence, and the `handoff.md` contract when consequential
resumable state may otherwise be lost. These references define the detailed
rules; the list above is the operational sequence.

### Closing behavior

Every close verifies what actually happened and leaves operational state
truthful. Treat work awaiting required review or acceptance as active rather
than completed, even when implementation is finished. Apply the
outcome-specific minimum:

| Outcome | Required close |
| --- | --- |
| Completed | Verify the result; reconcile repository and durable docs; move or mark the task completed and release active scope; clear obsolete handoff state. Add a handoff only when another active workstream needs non-obvious transfer state. |
| Partial | Keep the task honestly active with current scope and a useful checkpoint; update `handoff.md` when resumption would otherwise repeat meaningful work or proceed incorrectly. |
| Blocked | Move or mark the task blocked, name the blocker or decision needed, and preserve consequential partial state in `handoff.md`; narrow or release scope that no longer needs protection. |
| Interrupted | Record an honest active checkpoint and handoff when meaningful partial state or risk must survive; do not imply completion or retain a misleading claim. |
| Trivial | Verify the change. Do not create a task, handoff, decision, archive entry, or other CSDD update unless the work discovered a material conflict or changed durable truth. |

For all outcomes, promote consequential knowledge before removing transient
state. Do not leave completed ownership claims active, duplicate facts across
documents, or preserve routine session narration.

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
progressively. This document owns principles, full lifecycle semantics,
hydration rationale, concurrency and stale-claim handling, contradiction
resolution, knowledge promotion, archive policy, limitations, and validation
scenarios. [document-contracts.md](document-contracts.md) owns exact document
boundaries, read and update triggers, aging, cross-document movement, examples,
and archive-entry structure. Templates remain in `assets/templates/`.

An agent SHOULD load only the referenced section needed for the current
decision. It SHOULD consult document contracts before making a non-obvious
document update or resolving a boundary or aging question, and consult the
deeper protocol sections for collaborative, conflicting, stale, or historical
cases. The skill MUST remain usable for levels 0 and 1 without forcing either
reference to be read in full.

## Concurrency model

CSDD coordination is document-based and intentionally lightweight.

### Minimum interoperable task structure

Tasks MUST use plain, human-readable Markdown. Each task requires a stable task
ID, a concise title, and an obvious state expressed by its section or another
clear Markdown mechanism:

```markdown
## In Progress

- [ ] T-004 — Define document templates
```

Active collaborative tasks SHOULD identify `Owner`, `Agent`, `Scope`, and
`Updated` when those fields help coordination. `Depends on`, `Blocked by`, and
a short `Note` MAY be added when relevant. Trivial tasks MAY omit all ownership
metadata.

```markdown
- [ ] T-021 — Implement password recovery
  - Owner: valen
  - Agent: codex/auth-reset
  - Scope: `src/auth/reset-password/**`
  - Updated: 2026-07-12
```

`Owner` identifies the accountable human or team and preferred coordination
point. `Agent` identifies the current operational executor or harness/task
label. Reassigning execution does not necessarily change human accountability.
Both fields are advisory labels, not authenticated identities. CSDD v0 MUST NOT
attempt automatic human identity discovery and SHOULD prefer human-readable
labels over provider-specific identifiers.

CSDD does not require story points, completion percentages, mandatory
priorities, risk scores, complex labels, redundant timestamps, or mandatory
reviewer fields. V0 MUST NOT require YAML front matter, JSON, a database, a
machine schema, or harness-specific metadata.

### C1 - Read active ownership before writing when overlap is plausible

Before non-trivial work, inspect relevant active entries in `.csdd/todo.md` when
the target scope could overlap. A trivial, clearly unrelated edit does not
require a coordination scan. Compare both path scope and affected contracts;
semantically overlapping contracts may conflict even when file globs differ.

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
when the information changes active work, and `handoff.md` when it is needed to
resume the current partial state.

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
semantic archival, and proportional overhead.

Future evaluations may separate a fixture author, isolated subject agent,
evaluator agent, and human reviewer. Evaluation SHOULD compare actual repository
state and diffs rather than trust only the subject agent's self-report.
Structured run reports are preferred, and full transcripts SHOULD NOT be
preserved by default. Phase 0 defines no evaluation infrastructure.

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

The following questions remain for dogfooding:

- Should the `Recently Completed` window in `todo.md` be bounded by relevance,
  phase, or a loose numeric guideline?
- Which `Agent` label conventions remain portable across Codex, Cursor, Claude
  Code, and future harnesses?
- Which normative statements should be promoted from SHOULD to MUST after
  real-world testing?
- Will one `.csdd/handoff.md` remain practical under concurrent editing?
- Does the archive model remain useful without becoming redundant with Git and
  durable project documents?
