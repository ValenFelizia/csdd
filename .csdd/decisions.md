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
