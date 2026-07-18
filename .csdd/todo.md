# TODO

## In Progress

## Ready to Land

- [ ] T-019 — Standardize TODO states, grouping, and retention
  - Owner: valen
  - Agent: cursor/t-019-todo-states
  - Scope: `references/protocol.md`, `references/document-contracts.md`, `SKILL.md`
  - Target: `main`
  - Base: `00d06fb`
  - Issue: `#3`
  - Updated: 2026-07-18
  - Landing: PR #12
  - Verification: `git diff --check` passed; protocol, document-contracts, and SKILL aligned to issue #3; only principal Scope plus the shared TODO coordination surface changed; T-018 reconciled against merged PR #10 with Retention: 5 compaction

## Blocked

## Pending

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

## Deferred

## Recently Completed

Retention: 5

- [x] T-018 — Define the Git-aware task lifecycle
  - Owner: valen
  - Scope: released
  - Updated: 2026-07-18
  - Landed: PR #10 @ `00d06fb`
  - Note: Git-aware lifecycle contract merged to `main`.

- [x] T-017 — Publish Field Report 001
  - Owner: valen
  - Scope: released
  - Updated: 2026-07-17
  - Note: Capture qualitative v0.1 usage across four real projects and derive the evidence base for v0.2.0.

- [x] T-016 — v0.1.0 launch

- [x] T-015 — README and public documentation

- [x] T-014 — Tighten closure and canonical-truth contracts
  - Owner: valen
  - Scope: released
  - Updated: 2026-07-12
  - Note: Added closure claim-release rules, protected historical Agent metadata, and clarified canonical specs/decisions boundaries.
