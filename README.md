# CSDD

**Collaborative Spec-Driven Development for ephemeral coding agents.**

CSDD is a lightweight protocol for preserving and coordinating project state
across AI coding sessions, agents, harnesses, branches, and worktrees.

Agents are temporary. Project state should not be.

CSDD externalizes the minimum sufficient project context into small,
version-controlled documents so that a new agent can understand what is true,
what is active, what was decided, and what remains unfinished.

> CSDD does not give agents shared memory. It gives the project durable,
> inspectable state.

## Status

CSDD is experimental.

The current release is `v0.2.0`. It builds on the `v0.1.0` protocol foundation
with a Git-aware task lifecycle, six canonical TODO states and bounded
retention, boundary-driven replaceable handoffs, an Absent-only `/csdd init`
adoption workflow, v0.2 primary templates plus a v0.1 → v0.2 migration guide,
and real-world-derived evaluation scenarios 06–08. Field Report 001 is the
evidence source for the milestone.

## Core documents

A CSDD-enabled repository uses a canonical `.csdd/` directory with four
primary documents:

```text
.csdd/
├── specs.md
├── todo.md
├── decisions.md
└── handoff.md
```

### `specs.md`

Durable behavioral truth:

- requirements;
- constraints;
- invariants;
- interfaces;
- accepted system behavior.

### `todo.md`

Current operational coordination:

- active tasks;
- human owners;
- operational agents;
- write scopes;
- dependencies;
- blocked work;
- a small recently completed window.

### `decisions.md`

Accepted directions whose rationale, alternatives, or consequences should
survive the implementation session.

### `handoff.md`

Only the current resumable state that another agent could otherwise
misunderstand, repeat, or lose.

### Optional `archive/`

Projects may add optional cold context containing semantic summaries of
completed phases or superseded project context. The archive is not part of
initial adoption or default hydration.

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
| 0 — Direct | Trivial isolated edits | Target file only |
| 1 — Local | Small bounded changes | Local files and nearby contracts |
| 2 — Operational | Multi-file, resumable, or coordinated work | Relevant TODO, handoff, specs, decisions |
| 3 — Deep | Architecture, contradiction, migration, or phase closure | Broader project and protocol context |

The agent should classify the task before hydrating context.

A trivial label change should not require reading project history. A stale
claim, architectural migration, or phase closure should not proceed without
relevant project state.

## Task and claim semantics

CSDD distinguishes:

- **Owner** — the responsible human or team;
- **Agent** — the current operational executor;
- **Scope** — the active write boundary.

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

## Quick start

### Install the skill (Codex and Cursor)

Install CSDD globally with the Agent Skills CLI so Codex and Cursor can
discover it:

```bash
npx skills add ValenFelizia/csdd --skill csdd --agent codex cursor -g -y
```

This installs the skill under `~/.agents/skills/csdd`. It does **not** create
project `.csdd/` files. Full install, verify, update, and uninstall steps are
in [`docs/installation.md`](docs/installation.md).

### Initialize a project with `/csdd init`

`/csdd init` is the primary adoption path for a repository that does not yet
have CSDD state. It is a portable workflow name, not a guaranteed native slash
command. Equivalent explicit skill or natural-language requests to initialize
CSDD are sufficient. Skill installation and `/csdd init` are separate steps.

After the skill is installed, ask the agent to initialize CSDD, for example:

```text
/csdd init
```

or:

```text
Initialize CSDD in this repository.
```

A successful initialization creates only the four primary documents:

```text
your-project/
├── .csdd/
│   ├── specs.md
│   ├── todo.md
│   ├── decisions.md
│   └── handoff.md
└── ...
```

The skill also applies when a repository already contains `.csdd/`. Existing
recognizable v0.1 projects should follow the
[v0.1 → v0.2 migration guide](references/migration-v0.1-to-v0.2.md) rather than
running `/csdd init`.

### Manual alternative

As a secondary alternative, copy the initialization templates from
[`assets/templates`](assets/templates) into a repository-level `.csdd/`
directory. Prefer `/csdd init` when an agent can run the adoption workflow.

For ordinary work after adoption, invoke the skill using the syntax supported
by your harness, for example:

```text
/csdd

Implement the pending password-reset task and verify the result.
```

or:

```text
$csdd

Resume T-201.
```

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
│   └── installation.md
├── assets/
│   └── templates/
├── references/
│   ├── protocol.md
│   ├── document-contracts.md
│   └── migration-v0.1-to-v0.2.md
├── evals/
│   ├── scenarios/
│   ├── runs/
│   └── results.md
└── dogfooding/
```

- [`SKILL.md`](SKILL.md) is the operational router.
- [`docs/installation.md`](docs/installation.md) is the global skill installation guide.
- [`references/protocol.md`](references/protocol.md) defines the full protocol.
- [`references/document-contracts.md`](references/document-contracts.md) defines document semantics.
- [`references/migration-v0.1-to-v0.2.md`](references/migration-v0.1-to-v0.2.md) is the operational v0.1 → v0.2 migration guide.
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

## Non-goals and limitations

CSDD is not:

- shared agent memory;
- a distributed lock service;
- a task scheduler;
- a replacement for Git;
- a guarantee that every agent observes every branch or worktree;
- a substitute for tests, code review, or human project ownership.

The current evaluations are manual and cover a limited set of models and
harnesses. Explicit skill invocation has been tested more extensively than
implicit activation.

## Versioning

CSDD follows semantic versioning.

- patch releases clarify wording or fix non-breaking protocol defects;
- minor releases add compatible rules, document fields, or workflows;
- major releases may change canonical document contracts or required behavior.

## License

See [`LICENSE`](LICENSE).