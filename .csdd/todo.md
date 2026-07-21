# TODO

## In Progress

## Ready to Land

- [ ] T-022 — Update templates and write the v0.1 to v0.2 migration guide
  - Owner: valen
  - Agent: cursor/t-022-v02-templates-migration
  - Scope: `assets/templates/specs.md`, `assets/templates/todo.md`, `assets/templates/decisions.md`, `assets/templates/handoff.md`, `assets/templates/archive-index.md`, `references/migration-v0.1-to-v0.2.md`, `README.md`, `SKILL.md`, `references/document-contracts.md`, `.csdd/todo.md`
  - Target: main
  - Base: `3f198f6a8ebf4571b1bbaf952228b8677d37bd28`
  - Updated: 2026-07-21
  - Issue: #6
  - Depends on: T-018, T-019, T-020, T-021
  - Landing: branch `design/t-022-v02-templates-migration` → review → PR → merge to `main`
  - Verification: `git diff --check` clean; principal template/docs paths plus `.csdd/todo.md` changed; `assets/templates/archive-index.md` deleted (no archive template under `assets/templates/`); four primary templates match init contract (six TODO headings + `Retention: 5`, no fictional DEC/tasks/handoffs); migration guide is conservative in-place and does not create archive; README makes `/csdd init` primary; SKILL routes recognizable v0.1 to the guide with explicit intent; optional archive contract intact in protocol/document-contracts; Status/`v0.1.0`/Versioning/evals unchanged; `protocol.md` untouched.

## Blocked

## Pending

- [ ] T-023 — Add real-world-derived v0.2 evaluation scenarios
  - Owner: valen
  - Note: Validate Git races, lifecycle truthfulness, TODO hygiene, handoff boundaries, and existing-repository initialization. Depends on T-022.

- [ ] T-024 — Prepare and release CSDD v0.2.0
  - Owner: valen
  - Note: Release only after migration documentation and v0.2 evaluations are complete.

## Deferred

## Recently Completed

Retention: 5

- [x] T-021 — Add the `/csdd init` adoption workflow
  - Owner: valen
  - Scope: released
  - Updated: 2026-07-20
  - Landed: PR #16 @ `5c3efc2`
  - Note: Instruction-first `/csdd init` adoption workflow with mutually exclusive destination classification, pre-write revalidation, and failure-versus-success separation.

- [x] T-020 — Make handoffs boundary-driven
  - Owner: valen
  - Scope: released
  - Updated: 2026-07-19
  - Landed: PR #13 @ `d0883fb`
  - Note: Boundary-driven handoffs: boundary + concrete risk, replaceable snapshots, remove-or-replace consumption.

- [x] T-019 — Standardize TODO states, grouping, and retention
  - Owner: valen
  - Updated: 2026-07-18
  - Landed: PR #12 @ `7fb098c`
  - Note: Standardized canonical TODO states, grouping, Deferred behavior, Ready to Land presentation, and bounded retention.

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
