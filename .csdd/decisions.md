# Decisions

## DEC-001 — Use `.csdd/` as the canonical v0 project-state location

- Status: accepted
- Date: 2026-07-10

### Context

Flexible discovery would introduce ambiguity, additional context consumption, and inconsistent behavior across agent harnesses.

### Decision

The four primary CSDD documents live under `.csdd/` in v0.

### Rationale

A deterministic location simplifies discovery, onboarding, portability, and future adapters.

### Consequences

Configurable locations and root-level alternatives are outside the scope of v0.

## DEC-002 — Keep the initial implementation instruction-first

- Status: accepted
- Date: 2026-07-10

### Context

CSDD needs real-world validation before introducing runtime enforcement or harness-specific integrations.

### Decision

The initial implementation consists of an Agent Skill, conceptual references, and Markdown templates.

### Rationale

This is the smallest implementation capable of validating the protocol.

### Consequences

Hooks, plugins, MCP integrations, commands, scripts, and adapters are deferred until concrete failures justify them.

## DEC-003 — Use adaptive rather than unconditional context hydration

- Status: accepted
- Date: 2026-07-10

### Context

Reading all project-state documents for every task would create unnecessary token cost and coordination overhead.

### Decision

Agents load only the minimum project context needed to execute safely, escalating hydration when scope, uncertainty, dependencies, or overlap require it.

### Rationale

CSDD must remain useful for both trivial edits and complex collaborative work.

### Consequences

The skill must classify context needs before loading CSDD state.

## DEC-004 — Keep the initial skill as a concise operational router

- Status: accepted
- Date: 2026-07-10

### Context

The skill must be immediately actionable without copying the full CSDD
protocol into every invocation. Detailed document, concurrency, reconciliation,
and archive rules are already maintained in conceptual references.

### Decision

Keep `SKILL.md` limited to applicability, adaptive context routing, the core
operational lifecycle, persistence routing, safety guards, closing behavior,
and links to progressive references. Keep detailed protocol semantics in
`references/protocol.md`, document-specific rules in
`references/document-contracts.md`, and reusable structures in
`assets/templates/`.

### Rationale

A short router minimizes routine context cost while progressive references keep
non-trivial, conflicting, and historical cases precise and maintainable.

### Consequences

The future skill must remain useful without unconditional reference loading.
Reference links and routing cues become part of its operational contract, and
protocol changes must preserve alignment between the fast path and detailed
references.

### Alternatives Considered

Embedding the complete protocol in `SKILL.md` was rejected because it would
raise context cost for trivial and local work and duplicate authoritative
material.

## DEC-005 — Distribute CSDD through the standard Agent Skills CLI

- Status: accepted
- Date: 2026-07-22

### Context

T-025 / issue #14 needs a one-command global installation path for the CSDD
skill without inventing packaging infrastructure. The Agent Skills CLI
(`npx skills`, currently `1.5.20`) already installs from GitHub into
`~/.agents/skills`, and Codex and Cursor both consume that universal location.
The CLI copies the versioned repository snapshot excluding `.git` and does not
currently offer `.skillignore` or an equivalent install-time filter.

### Decision

- Adopt the standard Agent Skills ecosystem as the distribution path.
- Do not create a custom installer, registry, manifest, or bootstrap for v0.2.1.
- Keep `SKILL.md` at the repository root for now.
- Accept that the CLI distributes the full snapshot (minus `.git`), including
  files beyond the runtime set (`SKILL.md`, `references/**`,
  `assets/templates/**`).
- Reconsider repository layout or filtering only if a real cost appears or the
  CLI gains official filtering support.

### Rationale

The smallest durable path is to document and verify the existing CLI contract
for Codex and Cursor rather than maintain parallel packaging. Explicit
`--agent codex cursor` avoids unintended installs to other detected agents
while still using one shared global copy.

### Consequences

Installation docs must separate skill install from `/csdd init`, warn against
hand-editing the managed copy, and record evidence without claiming untested
harnesses. Development checkouts that live at `~/.agents/skills/csdd` must not
be overwritten casually by `skills add` / `update` / `remove`.

### Alternatives Considered

A custom installer or trimmed package tree was rejected for now: it adds
maintenance cost without fixing a demonstrated blocker, and the CLI already
provides the required happy path.

## DEC-006 — Allow the v0.2.1 beta before completing the independent onboarding pilot

- Status: accepted
- Date: 2026-08-05

### Context

T-029 / issue #28 originally made two independent onboarding attempts a hard
gate for v0.2.1. After roughly two weeks, one acquaintance had agreed to help
but had not started, and one low-exposure Reddit recruitment attempt received
no response. No external onboarding session was completed.

Waiting indefinitely would create a circular dependency: CSDD needs real users
to validate onboarding, while a small public release is the practical way to
reach those users. The missing evidence still leaves onboarding risk unknown.

### Decision

- Defer T-029 until an independent adopter agrees to run the frozen onboarding
  flow or provides equivalent diagnosable onboarding evidence.
- Allow T-030 to prepare and publish v0.2.1 as an experimental public beta under
  an explicit exception to the original T-029 release gate.
- Keep issue #28 open and do not claim that onboarding was externally validated.
- Use the staged T-031 launch and early adoption to recruit the first pilot
  participants, without substituting agent self-evaluation for human evidence.

### Rationale

A narrow, reversible beta can expose the onboarding path to real adopters
without overstating confidence. This preserves the value of the original pilot
while avoiding an indefinite pre-release stall.

### Consequences

Release notes for v0.2.1 must state that the independent-user pilot is pending.
No external blocker can be ruled out from zero completed sessions. Any concrete
install, initialization, destructive-behavior, or first-use blocker reported by
an adopter receives priority triage and correction before broader promotion.

## DEC-007 — Keep the handoff workspace-local and the other three documents committed

- Status: accepted
- Date: 2026-11-02

### Context

v0.2 treated all four `.csdd/` documents as committed, branch-local state. In
practice the handoff carries transient same-workspace resumption state. Committing
it created several problems: handoff churn polluted diffs and review, concurrent
branches conflicted over a file that describes one workspace, and the committed
copy implied the handoff was a reliable channel between people and machines.
`specs.md` and `decisions.md` stayed current; `todo.md` stayed committed but is
increasingly replaced by GitHub issues for the maintainer.

### Decision

- Keep `.csdd/specs.md`, `.csdd/todo.md`, and `.csdd/decisions.md` committed.
- Make `.csdd/handoff.md` workspace-local and untracked through a committed
  `.csdd/.gitignore` containing an uncommented `handoff.md` rule.
- Keep the canonical path `.csdd/handoff.md`. Do not rename existing documents or
  add a fifth one.
- `/csdd init` creates the three committed documents plus `.csdd/.gitignore` and
  does not create `handoff.md`.
- Treat a tracked handoff as legacy v0.2 state. Offer the v0.2 → v0.3 migration
  explicitly; never untrack, delete, or rewrite it automatically.
- Default the handoff close action to deletion. Keep one short replaceable
  snapshot only when committed state cannot recover a concrete resumption risk.
- Keep `todo.md` committed for now. Do not split or localize it.

### Rationale

The split follows transport, not document count. Committed documents are the
only surfaces that survive clones, branches, worktrees, and machines. The handoff
is one workspace's current snapshot and should not pretend to be shared truth.
Removing it from Git eliminates review noise and cross-branch conflicts while
preserving same-workspace continuity. Adding `.csdd/.gitignore` rather than a
root `.gitignore` keeps the policy local to the state directory and independent
of a project's existing ignore rules.

### Consequences

The release is `0.3.0`. v0.3 reads v0.2 state, but a v0.2 skill may treat a
missing handoff as partial state and may create or commit one. Migration needs
`git rm --cached .csdd/handoff.md`; adding the ignore rule alone does not untrack
the file. `assets/templates/handoff.md` is deleted because the contract owns the
handoff shape and init no longer creates the file. Structural validation requires
three primary templates and a `gitignore` template with an active `handoff.md`
rule.

### Alternatives Considered

Keeping the handoff committed preserves cross-person transfer but keeps the
conflict and review costs that motivated the change. Deleting the handoff
entirely removes same-workspace continuity, which the field evidence still
supports. A root `.gitignore` rule was rejected because it would not travel with
`.csdd/` and could collide with project policy. Auto-migrating tracked handoffs
during `init` was rejected because it is destructive and violates the init
contract.
