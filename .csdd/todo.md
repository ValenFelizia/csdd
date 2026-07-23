# TODO

## In Progress

## Ready to Land

- [ ] T-027 — Publish an evidence-backed agent compatibility matrix
  - Owner: valen
  - Agent: cursor-grok-4.5
  - Scope: `README.md`, `.csdd/specs.md`, `.csdd/todo.md`, `docs/compatibility.md`, `evidence/t-027-compatibility.md`, `evals/runs/t027-01-cursor-fixture-a.md`, `evals/runs/t027-01-cursor-fixture-a.json`, `evals/runs/t027-02-codex-fixture-a.md`, `evals/runs/t027-02-codex-fixture-a.json`, `evals/runs/t027-03-cursor-fixture-b.md`, `evals/runs/t027-03-cursor-fixture-b.json`, `evals/runs/t027-04-codex-fixture-b.md`, `evals/runs/t027-04-codex-fixture-b.json`
  - Target: main
  - Base: `e2c91873f18acb22b6f9ac7ee19056e8223dd6d1`
  - Updated: 2026-07-23
  - Issue: #24
  - Landing: Draft PR #33 open against main; pending review and merge
  - Verification: four campaign runs PASS; 19 unit tests passed; `validate_repository.py` passed; `git diff --check` passed; four JSON records valid; relative Markdown links valid
  - Note: Campaign 4/4 PASS under development checkout / live profile. Global install and Discovery remain **partial**; Implicit activation **not tested**. Model not recorded; Codex harness version not user-visible.

## Blocked

## Pending

## Deferred

## Recently Completed

Retention: 5

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

- [x] T-022 — Update templates and write the v0.1 to v0.2 migration guide
  - Owner: valen
  - Scope: released
  - Updated: 2026-07-21
  - Landed: PR #17 @ `39f0f82`
  - Note: Materialized v0.2 primary templates, removed archive template, and added conservative v0.1 → v0.2 migration guide with README/SKILL routing.
