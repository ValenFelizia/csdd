# TODO

## In Progress

- [ ] T-032 — Add Antigravity skill installation support
  - Owner: valen
  - Agent: codex-gpt-5.6
  - Scope: `README.md`, `docs/installation.md`, `docs/compatibility.md`, `evidence/t-032-antigravity.md`, `.csdd/todo.md`
  - Target: `main`
  - Base: `main`
  - Updated: 2026-07-29
  - Issue: #34
  - Note: Implement the verified project-local Antigravity path without claiming untested global or behavioral compatibility.

## Ready to Land

## Blocked

## Pending

## Deferred

## Recently Completed

Retention: 5

- [x] T-027 — Publish an evidence-backed agent compatibility matrix
  - Owner: valen
  - Agent: cursor-grok-4.5
  - Scope: released
  - Updated: 2026-07-23
  - Issue: #24
  - Landed: PR #33 @ `5af4746`
  - Note: Published the canonical evidence-backed Cursor/Codex compatibility matrix from a 4/4 PASS campaign; Global install and Discovery remain partial, and Implicit activation remains not tested.

- [x] T-026 — Add automated structural and repository validation in CI
  - Owner: valen
  - Agent: cursor-grok-4.5
  - Scope: released
  - Updated: 2026-07-22
  - Issue: #21
  - Landed: PR #32 @ `d016d23`
  - Note: Offline stdlib validator, unittest suite, and least-privilege GitHub Actions workflow landed; CI SUCCESS on PR #32.

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
