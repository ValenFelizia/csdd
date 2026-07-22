# Specifications

## Project Summary

CSDD (Collaborative Spec-Driven Development) is a lightweight, text-first protocol for preserving project state and coordinating work across ephemeral AI coding agents.

CSDD externalizes the minimum sufficient state required for agents to orient, resume, coordinate, and hand off work without depending on shared chat history.

The authoritative conceptual protocol is defined in:

- `references/protocol.md`
- `references/document-contracts.md`

## Requirements

- CSDD MUST remain human-readable and harness-agnostic at the protocol level.
- CSDD MUST use `.csdd/` as the canonical project-state location in v0.
- CSDD MUST support adaptive context hydration.
- CSDD MUST preserve distinct responsibilities for specifications, tasks, decisions, and handoffs.
- CSDD MUST avoid imposing collaborative overhead on trivial isolated tasks.
- The initial skill MUST be usable without scripts, hooks, plugins, MCP, or runtime dependencies.
- The skill MUST guide agents to reconcile documentation with repository reality.
- The skill MUST NOT claim to provide true shared memory or reliable distributed locking.

## Constraints

- The initial implementation is instruction-first.
- `SKILL.md` is the primary operational entrypoint.
- Supporting protocol detail belongs in `references/`.
- Project-state templates belong in `assets/templates/`.
- The first version targets portable Agent Skills behavior.
- Codex, Cursor, and Antigravity are initial dogfooding environments, without requiring harness-specific adapters.
- Context loading must remain proportional to task need.
- Coordination overhead must not exceed task complexity.

## Invariants

- Agents are ephemeral; project state is durable.
- Persist consequential knowledge, not activity.
- The four primary documents remain plain Markdown.
- `todo.md` remains the primary coordination surface.
- `handoff.md` transfers resumable state and does not duplicate task tracking.
- Archive content, when present, is cold context and is never loaded by default.
- Active scope overlap is never knowingly ignored.
- Durable decisions are never silently reversed.

## Interfaces and Contracts

- Agent Skills entrypoint: `SKILL.md`
- Conceptual protocol: `references/protocol.md`
- Document semantics: `references/document-contracts.md`
- Distributed project templates: `assets/templates/`
- Runtime project state: `.csdd/`

## Distribution (non-normative for protocol semantics)

These distribution facts do not change the v0.2 protocol rules in
`references/`. They describe how the skill itself is obtained.

- Agent Skills (`npx skills`) is the standard distribution mechanism for the
  CSDD skill.
- Current explicit install targets are Codex and Cursor only.
- The skill installs globally to the universal location `~/.agents/skills/csdd`.
- Runtime required for execution: `SKILL.md`, `references/**`, and
  `assets/templates/**`. The CLI may also copy additional repository files;
  those extras are distributed but not required at runtime.
- Installing the skill and adopting CSDD in a project (`/csdd init` creating
  `.csdd/`) are distinct operations. Skill install/update/remove must not be
  treated as creating or deleting project `.csdd/` state.

## Structural validation (non-normative for protocol semantics)

These facts describe repository tooling. They do not change the v0.2 protocol
rules in `references/`.

- The repository provides reproducible structural validation for the skill
  package, shipped templates, and relative Markdown links.
- CI and contributors run the same validation logic locally and in GitHub
  Actions.
- Validation is offline: it must not depend on network access or model output.
- Failures identify the file, violated rule, and expected condition.
- Passing CI does not prove harness compatibility or semantic/protocol
  correctness; qualitative evidence remains in `evals/`.
