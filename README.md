# CSDD

**Durable project state for ephemeral coding agents.**

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

Install CSDD globally for Codex and Cursor with the Agent Skills CLI:

```bash
npx skills add ValenFelizia/csdd --skill csdd --agent codex cursor -g -y
```

This installs the skill under `~/.agents/skills/csdd`. It does **not** create
or modify `.csdd/` in any project. See the
[installation guide](docs/installation.md) for prerequisites, verification,
updates, and uninstall steps.

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
| `npx skills add ... -g` | Makes the CSDD skill available to agents |
| `/csdd init` | Creates CSDD state in the current repository |

Initialization is Absent-only: it creates state only when the target repository
does not already contain `.csdd/`. A successful run creates exactly:

```text
your-project/
└── .csdd/
    ├── specs.md
    ├── todo.md
    ├── decisions.md
    └── handoff.md
```

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

As a manual fallback, copy the four files from
[`assets/templates`](assets/templates) into a repository-level `.csdd/`
directory. Prefer `/csdd init` when an agent can run the adoption workflow.

## The four documents

| Document | Canonical responsibility |
| --- | --- |
| [`specs.md`](assets/templates/specs.md) | Durable behavioral truth: requirements, constraints, invariants, interfaces, and accepted behavior |
| [`todo.md`](assets/templates/todo.md) | Current operational coordination: tasks, owners, agents, write scopes, dependencies, blockers, and bounded completion history |
| [`decisions.md`](assets/templates/decisions.md) | Accepted directions whose rationale, alternatives, or consequences should survive the session |
| [`handoff.md`](assets/templates/handoff.md) | Only current resumable state that another agent could otherwise misunderstand, repeat, or lose |

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

## Compatibility and validation

Compatibility is still a work in progress. CSDD currently supports Codex and
Cursor, but compatibility is dimensional rather than a binary
supported/unsupported label. See the
[compatibility matrix](docs/compatibility.md) for current evidence, limitations,
and validation status.

## Status and scope

CSDD is experimental public-beta software. The latest published version is
shown by the release badge above; release history is recorded in
[`changelog.md`](changelog.md).

The v0.2 protocol includes a Git-aware task lifecycle, six canonical TODO
states with bounded retention, boundary-driven replaceable handoffs, an
Absent-only initialization workflow, and primary templates.

Before `1.0`, document contracts and workflows may still evolve through
versioned releases. Current compatibility claims are intentionally narrow and
evidence-backed.

## Learn more

- [Installation and lifecycle](docs/installation.md)
- [Agent compatibility matrix](docs/compatibility.md)
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

## Branches and worktrees

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
│   └── compatibility.md
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
`SKILL.md` frontmatter, the T-025 runtime file boundary, the four primary
templates, canonical `todo.md` template headings and Retention, and relative
Markdown links. It is deterministic and does not use the network or model
output. Passing these checks does not replace the qualitative evaluations in
[`evals/`](evals).

## Versioning

CSDD follows semantic versioning.

- patch releases clarify wording or fix non-breaking protocol defects;
- minor releases add compatible rules, document fields, or workflows;
- major releases may change canonical document contracts or required behavior.

## License

See [`LICENSE`](LICENSE).
