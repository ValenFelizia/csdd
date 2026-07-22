# TODO

## In Progress

## Ready to Land

- [ ] T-025 — Add a one-command global installation path for the CSDD skill
  - Owner: valen
  - Agent: cursor-grok-4.5
  - Scope: `docs/installation.md`, `evidence/t-025-installation.md`, `README.md`, `.csdd/specs.md`, `.csdd/decisions.md`, `.csdd/todo.md`
  - Target: `main`
  - Base: `061ca5e`
  - Updated: 2026-07-22
  - Issue: #14
  - Landing: Branch `distribution/t-025-global-installation` pushed; open PR against `main` after review
  - Verification: Isolated-HOME CLI add/reinstall/update/remove and project `.csdd/` preservation passed; Cursor 3.12.30 and Codex Desktop new-session discovery passed against development checkout at `~/.agents/skills/csdd` ref `7594550` (see `evidence/t-025-installation.md`)

## Blocked

## Pending

## Deferred

## Recently Completed

Retention: 5

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

- [x] T-020 — Make handoffs boundary-driven
  - Owner: valen
  - Scope: released
  - Updated: 2026-07-19
  - Landed: PR #13 @ `d0883fb`
  - Note: Boundary-driven handoffs: boundary + concrete risk, replaceable snapshots, remove-or-replace consumption.
