# TODO

## In Progress

- [ ] T-026 — Add automated structural and repository validation in CI
  - Owner: valen
  - Agent: cursor-grok-4.5
  - Scope: `.github/workflows/validate.yml`, `scripts/validate_repository.py`, `tests/test_repository_validation.py`, `README.md`, `.csdd/specs.md`, `.csdd/todo.md`
  - Target: `main`
  - Base: `18154fd`
  - Updated: 2026-07-22
  - Issue: #21
  - Note: Checkpoint published on `validation/t-026-structural-ci`; local validation approved. Real GitHub Actions CI still pending a PR. Next safe action: open PR to execute the workflow.

## Ready to Land

## Blocked

## Pending

## Deferred

## Recently Completed

Retention: 5

- [x] T-025 — Add a one-command global installation path for the CSDD skill
  - Owner: valen
  - Agent: cursor-grok-4.5
  - Scope: released
  - Updated: 2026-07-22
  - Issue: #14
  - Landed: PR #31 @ `8ed582b`
  - Note: Global Agent Skills install path for Codex/Cursor documented and verified; evidence in `evidence/t-025-installation.md`.

- [x] T-024 — Prepare and release CSDD v0.2.0
  - Owner: valen
  - Agent: cursor-grok-4.5
  - Scope: released
  - Updated: 2026-07-21
  - Issue: #8
  - Landed: PR #22 @ `9bf9609`
  - Note: Published v0.2.0 from `9bf9609` at https://github.com/ValenFelizia/csdd/releases/tag/v0.2.0; scenarios 06–08 Run A passed with no critical failures; no remaining release blockers.

- [x] T-023 — Add real-world-derived v0.2 evaluation scenarios
  - Owner: valen
  - Scope: released
  - Updated: 2026-07-21
  - Landed: PR #18 @ `6ec208f`
  - Note: Added focused v0.2 scenario contracts 06–08, separated historical runs, recorded Run A PASS reports, and evaluation workspace `.gitignore`.

- [x] T-022 — Update templates and write the v0.1 to v0.2 migration guide
  - Owner: valen
  - Scope: released
  - Updated: 2026-07-21
  - Landed: PR #17 @ `39f0f82`
  - Note: Materialized v0.2 primary templates, removed archive template, and added conservative v0.1 → v0.2 migration guide with README/SKILL routing.

- [x] T-021 — Add the `/csdd init` adoption workflow
  - Owner: valen
  - Scope: released
  - Updated: 2026-07-20
  - Landed: PR #16 @ `5c3efc2`
  - Note: Instruction-first `/csdd init` adoption workflow with mutually exclusive destination classification, pre-write revalidation, and failure-versus-success separation.
