# TODO

## In Progress

## Pending

- [ ] T-018 — Define the Git-aware task lifecycle
  - Owner: valen
  - Note: Define refresh checkpoints, Git evidence, implementation vs landing, and truthful completion semantics. Depends on T-017.

- [ ] T-019 — Standardize TODO states, grouping, and retention
  - Owner: valen
  - Note: Resolve Deferred/Icebox behavior, workstream grouping, canonical headings, and bounded Recently Completed retention. Depends on T-018.

- [ ] T-020 — Make handoffs boundary-driven
  - Owner: valen
  - Note: Prevent progress-log churn and define transfer, ready-to-land, blocked, and collision handoffs. Depends on T-018.

- [ ] T-021 — Add the `/csdd init` adoption workflow
  - Owner: valen
  - Note: Initialize `.csdd/` from an existing repository without copying documentation blindly or inventing project truth.

- [ ] T-022 — Update templates and write the v0.1 to v0.2 migration guide
  - Owner: valen
  - Note: Apply accepted lifecycle, TODO, handoff, and initialization contracts. Depends on T-018 through T-021.

- [ ] T-023 — Add real-world-derived v0.2 evaluation scenarios
  - Owner: valen
  - Note: Validate Git races, lifecycle truthfulness, TODO hygiene, handoff boundaries, and existing-repository initialization. Depends on T-022.

- [ ] T-024 — Prepare and release CSDD v0.2.0
  - Owner: valen
  - Note: Release only after migration documentation and v0.2 evaluations are complete.

## Blocked

## Recently Completed

- [x] T-013 — Define branch and worktree baseline reconciliation
  - Owner: valen
  - Agent: cursor/csdd-branch-baseline
  - Scope: released
  - Updated: 2026-07-12
  - Note: Added Trigger→Close procedure and divergence classes in protocol.md; locality/evidence rules in document-contracts.md; concise router guidance in SKILL.md.

- [x] T-014 — Tighten closure and canonical-truth contracts
  - Owner: valen
  - Agent: cursor/csdd-contracts
  - Scope: released
  - Updated: 2026-07-12
  - Note: Added closure claim-release rules, protected historical Agent metadata, and clarified canonical specs/decisions boundaries.

- [x] T-015 — README and public documentation

- [x] T-016 — v0.1.0 launch

- [x] T-017 — Publish Field Report 001
  - Owner: valen
  - Agent: cursor/field-report
  - Scope: `field-reports/001-v0.1-real-world-usage.md`, `.csdd/todo.md`
  - Updated: 2026-07-17
  - Note: Capture qualitative v0.1 usage across four real projects and derive the evidence base for v0.2.0.