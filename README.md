# CSDD

**Collaborative Spec Driven Development: Durable project state for ephemeral coding agents.**

[![Latest release](https://img.shields.io/github/v/release/ValenFelizia/csdd?display_name=tag&sort=semver)](https://github.com/ValenFelizia/csdd/releases/latest)
[![CSDD validation](https://github.com/ValenFelizia/csdd/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/ValenFelizia/csdd/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: public beta](https://img.shields.io/badge/status-public%20beta-orange.svg)](#status-and-scope)

CSDD is a lightweight, Git-native protocol for preserving and coordinating
project state across AI coding sessions, agents, harnesses, branches, and
worktrees.

Coding agents are temporary. Their conversations end, context windows reset,
and parallel sessions do not share reliable state. CSDD keeps the minimum
sufficient context in four small, version-controlled documents and uses
[adaptive hydration](#adaptive-hydration) so agents load only what each task
needs. The next agent can determine what is true, what is active, what was
decided, and what remains unfinished.

It is designed for developers who use coding agents on work that must survive
session boundaries, resume safely, or stay coordinated across concurrent
branches and worktrees. Trivial work keeps a trivial fast path.

> CSDD provides durable and inspectable project state. It does not provide
> shared runtime memory, distributed locking, or automatic synchronization.

## Quick start

### 1. Install the skill

Pick the install path for your agent. Full commands, manual
copy/clone/symlink options, verification, and uninstall steps are in the
[installation guide](docs/installation.md). See
[Supported agents](#supported-agents) for the evidence-backed summary.

**Codex and Cursor** (global):

```bash
npx skills add ValenFelizia/csdd --skill csdd --agent codex cursor -g -y
```

**Claude Code** (personal / global):

```bash
npx skills add ValenFelizia/csdd --skill csdd --agent claude-code -g -y
```

**Google Antigravity** (project-local, from the workspace root):

```bash
npx skills add ValenFelizia/csdd --skill csdd --agent antigravity -y
```

Skill install does **not** create or modify `.csdd/` in any project. Do not
add `-g` to the Antigravity command until the Agent Skills CLI global target
agrees with Antigravity's current documented global path.

### 2. Initialize one repository

Open the repository you want to adopt and explicitly ask the agent to initialize
CSDD:

```text
/csdd init
```

`/csdd init` is the portable workflow name, not a guaranteed native slash
command. An equivalent explicit request also works:

```text
Initialize CSDD in this repository.
```

Installation and initialization are separate operations:

| Operation | Result |
| --- | --- |
| `npx skills add ... --agent codex cursor -g` | Makes CSDD globally available to Codex and Cursor |
| `npx skills add ... --agent claude-code -g` | Makes CSDD available to Claude Code under `~/.claude/skills/csdd` |
| `npx skills add ... --agent antigravity` | Makes CSDD available to Antigravity in the current workspace |
| `/csdd init` | Creates CSDD state in the current repository |

Initialization is Absent-only: it creates state only when the target repository
does not already contain `.csdd/`. A successful run with no fence line creates
exactly:

```text
your-project/
└── .csdd/
    ├── specs.md
    ├── decisions.md
    └── handoff.md
```

That tree is Current with `task surface: board-off`. `.csdd/todo.md` is not
created. A sentence about GitHub, Linear, or issues does not create it.

CSDD’s value is how agents decide and which documents they load, not an
in-repo board. In a project that already uses git with Issues and pull
requests, a checked-in `todo.md` is a second backlog that forces constant
rebases. Leave the surface board-off there. Opt in when a solo repo has no
issue tracker and you want in-repo claims (`Owner`, `Agent`, `Scope`), or
when you want a stub that points agents at an external tracker with
`Tracker:` and `Next:`.

Opt in during the same init, or later on a Current board-off tree, with one
whole line from this fence. The contract is
[Phrase fence](references/document-contracts.md#phrase-fence).

```text
/csdd todo enable local board
csdd todo enable local board
/csdd todo enable external stub
csdd todo enable external stub
```

The local phrase also writes `.csdd/todo.md` from
[`assets/templates/todo.md`](assets/templates/todo.md): six headings and
`Retention: 5`, no tasks. The external phrase also needs one whole-line
`Tracker:` and one whole-line `Next:`, and writes the
[external-tracker stub](references/document-contracts.md#external-tracker-stub).
A second init does not add the file. `/csdd todo enable` is the later writer,
and only while the surface is still board-off.

### 3. Start using durable project state

Invoke the installed skill using the syntax supported by your harness. For a
newly initialized repository, a safe first request is:

```text
/csdd

Inspect this repository and its CSDD state. Tell me which project facts or
active work should be recorded, without inventing missing information.
```

The initialized documents may stay sparse. Structural success does not require
the agent to guess requirements, decisions, tasks, or handoff state.

As a manual fallback, copy `specs.md`, `decisions.md`, and `handoff.md` from
[`assets/templates`](assets/templates) into a repository-level `.csdd/`
directory. Copy `todo.md`, or copy `todo.external.md` and rename it to
`todo.md` after replacing `Tracker:` and `Next:`, only when opting in.
Prefer `/csdd init` when an agent can run the adoption workflow.

### 4. Inspect existing state

When CSDD state may already exist, ask for a read-only diagnosis or a derived
snapshot:

```text
/csdd doctor
/csdd status
```

`/csdd doctor` reports classification, evidence-backed findings, and one next
step. `/csdd status` summarizes what is active and points back at the canonical
files. Neither initializes, repairs, migrates, or edits files. If status
cannot count the state reliably, it says so and recommends doctor. The
contracts are in [read-only-workflows.md](references/read-only-workflows.md).

## The documents

| Document | Canonical responsibility |
| --- | --- |
| [`specs.md`](assets/templates/specs.md) | Required. Durable behavioral truth: requirements, constraints, invariants, interfaces, and accepted behavior |
| [`decisions.md`](assets/templates/decisions.md) | Required. Accepted directions whose rationale, alternatives, or consequences should survive the session |
| [`handoff.md`](assets/templates/handoff.md) | Required. Only current resumable state that another agent could otherwise misunderstand, repeat, or lose. Not a backlog when `todo.md` is absent |
| [`todo.md`](assets/templates/todo.md) | Optional. Absent by default (board-off). Opt-in local board: tasks, owners, agents, write scopes, dependencies, blockers, and bounded completion history. Opt-in external stub ([`todo.external.md`](assets/templates/todo.external.md)): in-repo `Mode: external`, `Tracker:`, and `Next:` when an external tracker owns the backlog |

Projects may add an optional `.csdd/archive/` for cold semantic summaries of
completed phases or superseded context. It is not part of initialization or
default context loading.

## What CSDD does and what it does not do

CSDD helps agents:

- load only the context required for the current task;
- preserve requirements and decisions outside transient conversations;
- coordinate human ownership, operational executors, and write scopes;
- reconcile relevant branch and worktree state before overlapping work;
- close tasks, release claims, and remove obsolete handoffs truthfully.

CSDD does not provide:

- shared agent memory or authenticated agent identity;
- distributed locks, consensus, or automatic synchronization;
- a task scheduler or a replacement for Git;
- a guarantee that every agent observes every branch or worktree;
- a substitute for tests, code review, or human project ownership.

## Supported agents

CSDD ships as an [Agent Skills](https://agentskills.io/specification)-compatible
skill (`SKILL.md` with `name` / `description`, optional `license`). Compatibility
is dimensional (distribution ≠ discovery ≠ behavior). Do not treat this table as
proof that CSDD “works everywhere.”

| Agent | Recommended install | Skill location | Distribution | Discovery | Behavior |
| --- | --- | --- | --- | --- | --- |
| Codex | `npx skills add ValenFelizia/csdd --skill csdd --agent codex cursor -g -y` | `~/.agents/skills/csdd` | **partial** | **partial** | **verified** (explicit / init / workflow) |
| Cursor | same command as Codex | `~/.agents/skills/csdd` | **partial** | **partial** | **verified** (explicit / init / workflow) |
| Claude Code | `npx skills add ValenFelizia/csdd --skill csdd --agent claude-code -g -y` | `~/.claude/skills/csdd` (personal) or `.claude/skills/csdd` (project) | **partial** | **not tested** | **not tested** |
| Google Antigravity | `npx skills add ValenFelizia/csdd --skill csdd --agent antigravity -y` | `.agents/skills/csdd` (project) | **partial** | **not tested** | **not tested** |

### Claude Code notes

Claude Code discovers skills from personal `~/.claude/skills/<name>/` and
project `.claude/skills/<name>/` ([Claude Code skills docs](https://code.claude.com/docs/en/skills)).
CSDD’s frontmatter `name: csdd` matches the install directory name, so `/csdd`
is the expected command once a session loads the skill.

Manual install (copy, clone, or symlink) is also supported by Claude Code:

```bash
# Personal (all projects on this machine)
git clone https://github.com/ValenFelizia/csdd.git ~/.claude/skills/csdd
# or: cp -a /path/to/csdd ~/.claude/skills/csdd
# or: ln -s /path/to/csdd ~/.claude/skills/csdd

# Project (commit for the team)
git clone https://github.com/ValenFelizia/csdd.git .claude/skills/csdd
```

A project `CLAUDE.md` is not required for skill discovery. Prefer installing the
skill over pasting CSDD into `CLAUDE.md`.

### Agent Skills CLI (verified in this repo’s install evidence)

```bash
npx skills add ValenFelizia/csdd
```

With Agent Skills CLI `1.5.18`, this command succeeds and installs a project
copy (observed destination `./.agents/skills/csdd`, with copies linked toward
detected agents). Prefer the explicit `--agent ...` commands above so you
control which harnesses receive the skill. Details and transcripts:
[installation guide](docs/installation.md),
[Claude Code distribution evidence](evidence/t-033-claude-code.md).

Full dimensional matrix, provenance, and limitations:
[compatibility matrix](docs/compatibility.md).

## Compatibility and validation

Compatibility is still a work in progress. Codex and Cursor have behavioral
evidence; Claude Code and Antigravity have installation-path evidence but no
recorded discovery or behavioral run yet. Compatibility is dimensional rather
than a binary supported/unsupported label. See the
[compatibility matrix](docs/compatibility.md) for current evidence, limitations,
and validation status.

## Status and scope

CSDD is experimental public-beta software. The latest published version is
shown by the release badge above; release history is recorded in
[`changelog.md`](changelog.md).

The protocol includes a Git-aware task lifecycle, six TODO states on an
opted-in local board, boundary-driven replaceable handoffs, Absent-only
initialization, and templates for the required documents plus the opt-in
task surface. Fresh init leaves the task surface board-off.

Before `1.0`, document contracts and workflows may still evolve through
versioned releases. Current compatibility claims are intentionally narrow and
evidence-backed.

## Learn more

- [Contributing and change-impact guidance](CONTRIBUTING.md)
- [Architecture and product boundaries](docs/architecture.md)
- [Installation and lifecycle](docs/installation.md)
- [Agent compatibility matrix](docs/compatibility.md)
- [Example: session resume and adaptive hydration](docs/examples/session-resume.md)
- [Full protocol](references/protocol.md)
- [Document contracts](references/document-contracts.md)
- [Evaluation results](evals/results.md)

## Principles

1. Persist consequential knowledge, not activity.
2. Load only the minimum sufficient context.
3. Treat repository reality as evidence, not documentation as unquestionable truth.
4. Do not silently contradict code, specifications, decisions, or active claims.
5. Keep human ownership distinct from operational agent execution.
6. Make write scopes explicit before concurrent edits.
7. Release claims when work is completed.
8. Store each durable truth in one canonical document.
9. Reconcile branch and worktree divergence explicitly.
10. Coordination overhead should remain proportional to task complexity.

## Adaptive hydration

CSDD does not require every agent to read every project document.

| Level | Use case | Typical context |
|---|---|---|
| 0: Direct | Trivial isolated edits | Target file only |
| 1: Local | Small bounded changes | Local files and nearby contracts |
| 2: Operational | Multi-file, resumable, or coordinated work | Relevant TODO, handoff, specs, decisions |
| 3: Deep | Architecture, contradiction, migration, or phase closure | Broader project and protocol context |

The agent should classify the task before hydrating context.

A trivial label change should not require reading project history. A stale
claim, architectural migration, or phase closure should not proceed without
relevant project state.

### Before / after: session resume

Same task: a fresh agent must finish partially completed password-reset work
with no prior conversation.

| | Without durable state (problem CSDD targets) | With CSDD ([run 02](evals/runs/02-session-resume.md), PASS) |
| --- | --- | --- |
| Continuity | Generation-done / consumption-left lives only in a dead chat — easy to redo or miss | Handoff + TODO record the boundary; subject preserved generation work |
| Context loaded | Broad rediscovery, or loading “everything” hoping something sticks | Level 2 on that opted-in board: read `todo.md`, `handoff.md`, `specs.md`, and `decisions.md` only |
| Decisions | Accepted storage choice can be reinvented | Reused the accepted SHA-256 hashed-storage decision |
| Outcome | Repeat or contradict prior work | Consumption + rejection cases implemented; **five tests passed**; scope released; obsolete handoff removed |

Trivial work stays cheap: a button-label change stayed Level 0 and **did not
read any `.csdd/` document contents**
([run 01](evals/runs/01-trivial-edit.md)).

Sources: [`evals/runs/02-session-resume.md`](evals/runs/02-session-resume.md),
[`evals/runs/01-trivial-edit.md`](evals/runs/01-trivial-edit.md),
[`evals/results.md`](evals/results.md). Longer walkthrough:
[`docs/examples/session-resume.md`](docs/examples/session-resume.md).

## Task and claim semantics

CSDD distinguishes:

- **Owner:** the responsible human or team;
- **Agent:** the current operational executor;
- **Scope:** the active write boundary.

Reassigning stale agent execution does not transfer human accountability.

Overlapping scopes must be coordinated before editing. Claims are advisory
coordination artifacts rather than distributed locks, but they must not be
ignored silently.

Completed tasks release or remove their write scopes.

## Local task IDs and optional issue links

New tracked tasks use IDs such as `T-auth-reset-001`: explicitly agreed
namespaces separate independent lines of task creation without requiring an
issue tracker or network connection. Continuing a task preserves its ID.
Optional `Issue:` URLs relate a task to GitHub, Linear, or another tracker;
they do not become its identity or enable automatic synchronization.

Existing stable IDs remain valid and can coexist with new IDs. Adoption does
not renumber tasks or migrate project state. Retention does not release IDs;
missing counter history requires a fresh coordinated namespace rather than
guessing. See the [identity contract](references/document-contracts.md#local-task-identity)
for allocation and duplicate reconciliation. This addition is unreleased;
it does not change compatibility claims recorded for older skill commits.

## Branches and worktrees

Parallel PRs can contend on TODO text even when their task IDs and code scopes
are distinct. Avoid patches for reads/unchanged checks and keep necessary
claims and waiting states visible. Reconcile relevant task changes against the
current target; after landing, close compatible known outcomes coherently and
apply retention to combined state. See [write economy](references/document-contracts.md#write-economy)
and [task-wise landing reconciliation](references/document-contracts.md#task-wise-landing-reconciliation).
The layout and Git-aware lifecycle are unchanged. Git conflicts and preparation
still count as integration work; savings depend on the workload and evaluation.

CSDD documents are version-controlled and therefore branch-local.

The current worktree is the operational baseline, but it is not proof that no
relevant activity exists elsewhere.

When concurrency, stale claims, or durable truth may involve other branches or
worktrees, agents inspect relevant Git state before editing. Live conflicting
work blocks silent execution. Divergent specifications or decisions must be
reconciled explicitly.

CSDD does not provide global locking or distributed consensus.

## Lifecycle

Depending on task complexity, CSDD follows an adaptive lifecycle:

```text
Trivial:
execute → verify

Local:
inspect → execute → verify

Project:
bootstrap → orient → execute → reconcile

Collaborative:
bootstrap → orient → claim → execute → reconcile → handoff
```

In this lifecycle, **Bootstrap** means detecting CSDD state and project
instructions at session start. It is not synonymous with `/csdd init`.

Closure must be truthful:

- completed;
- partial;
- blocked;
- interrupted;
- trivial.

Obsolete claims and handoffs should not survive completed work.

## Example task

```markdown
- [ ] T-201 — Complete password-reset token consumption
  - Owner: valen
  - Agent: cursor/password-reset
  - Scope: `src/password-reset/consume-token.ts`, `tests/password-reset.test.ts`
  - Updated: 2026-07-12
  - Note: Generation and hashed persistence are complete. Consumption remains.
```

When completed:

```markdown
- [x] T-201 — Complete password-reset token consumption
  - Owner: valen
  - Agent: cursor/password-reset
  - Scope: released
  - Updated: 2026-07-12
```

## Repository structure

```text
.
├── SKILL.md
├── docs/
│   ├── installation.md
│   ├── compatibility.md
│   └── examples/
│       └── session-resume.md
├── assets/
│   └── templates/
├── references/
│   ├── protocol.md
│   └── document-contracts.md
├── evals/
│   ├── scenarios/
│   ├── runs/
│   └── results.md
└── dogfooding/
```

- [`SKILL.md`](SKILL.md) is the operational router.
- [`docs/installation.md`](docs/installation.md) is the global skill installation guide.
- [`docs/compatibility.md`](docs/compatibility.md) is the canonical dimensional compatibility matrix.
- [`docs/examples/session-resume.md`](docs/examples/session-resume.md) walks through adaptive hydration on a recorded resume eval.
- [`references/protocol.md`](references/protocol.md) defines the full protocol.
- [`references/document-contracts.md`](references/document-contracts.md) defines document semantics.
- [`assets/templates`](assets/templates) contains initialization templates.
- [`evals`](evals) contains reusable scenarios and recorded runs.

## Evaluation

The manual evaluation suite covers:

- scenarios 01–05 as historical evaluations: trivial fast path, session resume,
  overlapping write scopes, evidence-based stale-claim reconciliation, and
  phase closure with semantic archival;
- scenario 06: Git divergence and live collision;
- scenario 07: landing truthfulness, TODO retention, and handoff cleanup;
- scenario 08: existing-repository initialization.

Scenarios 01–05 found protocol defects involving human ownership, completed
scopes, historical agent metadata, and duplicated durable truth. The rules were
updated and the same fixtures were rerun successfully.

Scenarios 06–08 Run A passed with no critical failures. Run B was not warranted
under the campaign rule.

See [`evals/results.md`](evals/results.md) for the complete matrix and
limitations.

## Structural validation

Run the same offline checks locally that CI runs:

```bash
python -m unittest discover -s tests -v
python scripts/validate_repository.py
```

Structural validation verifies machine-checkable repository contracts such as
`SKILL.md` frontmatter, the T-025 runtime file boundary, the primary templates
plus `todo.external.md`, local-board `todo.md` headings and Retention, external
stub fields and mixed-shape rejection, and relative Markdown links. It is
deterministic and does not use the network or model output. Passing these
checks does not replace the qualitative evaluations in [`evals/`](evals).

## Versioning

CSDD follows semantic versioning. Before 1.0, a minor version may change
required init behavior.

- patch releases clarify wording or fix non-breaking protocol defects;
- minor releases add compatible rules, document fields, or workflows;
- major releases may change canonical document contracts or required behavior.

v0.3.0 changes the init patch and the Current class. Fresh init does not
write `.csdd/todo.md`. A valid trio with that path absent is Current
board-off. Existing valid local boards and valid stubs stay valid. Re-enable
with a fence line. Enable writes a blank template and does not restore deleted
task text. Restore that file from Git instead.

## License

[MIT License](LICENSE). Copyright (c) 2026 Valentín Felizia.
