# TODO

## In Progress

## Ready to Land

- [ ] T-030 — Prepare and release CSDD v0.2.1 public beta
  - Owner: valen
  - Agent: cursor-grok-4.5
  - Scope: `.csdd/todo.md`, `changelog.md`, `evidence/t-030-release-readiness.md`
  - Target: `main`
  - Base: `caf43dba97087afeac8e597401cff232fb8430a8`
  - Updated: 2026-08-11
  - Issue: #29
  - Depends on: Accepted T-029 release-gate exception in DEC-006
  - Landing: `release/t-030-v0.2.1` → `main`; PR #38 open (Refs #29)
  - Verification: 19 unit tests PASS; `scripts/validate_repository.py` PASS; `git diff --check` clean; 119 relative links resolve; no `SKILL.md`/`references/`/`assets/templates/` drift since `v0.2.0`
  - Note: Preparation only. Tag, GitHub Release, post-merge lifecycle checks, and issue closure remain pending. T-029 stays Deferred under DEC-006.

## Blocked

## Pending

## Deferred

- [ ] T-029 — Validate v0.2.1 onboarding with independent users
  - Owner: valen
  - Scope: released
  - Updated: 2026-08-05
  - Issue: #28
  - Reason: Two recruitment attempts produced no completed sessions; holding an experimental beta indefinitely would prevent real adopters from providing the missing evidence.
  - Resume when: An independent adopter agrees to complete the frozen onboarding flow, or a real onboarding report provides equivalent diagnosable evidence.
  - Note: Zero external onboarding sessions completed; v0.2.1 may proceed under DEC-006 without claiming externally validated onboarding.

## Recently Completed

Retention: 5

- [x] T-032 — Add Antigravity skill installation support
  - Owner: valen
  - Agent: codex-gpt-5.6
  - Scope: released
  - Updated: 2026-07-29
  - Issue: #34
  - Landed: PR #35 @ `80d26a8`
  - Note: Added partial project-local Antigravity distribution evidence; global CLI install, discovery, and behavior remain not tested.

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
