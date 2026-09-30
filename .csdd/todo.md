# TODO

## In Progress

## Ready to Land

- [ ] T-036 — Add a read-only `/csdd doctor` workflow
  - Owner: valen
  - Agent: cursor-grok-4.7
  - Scope: `SKILL.md`, `references/protocol.md`, `references/document-contracts.md`, `references/read-only-workflows.md`, `README.md`, `changelog.md`, `evals/README.md`, `evals/scenarios/09-doctor-states.md`, `evals/scenarios/10-doctor-false-positives.md`, `evals/scenarios/11-doctor-visibility-limits.md`, `.csdd/todo.md`
  - Target: `main`
  - Base: `d30eb30b8f19292fe10ae8cc64d65bd22832e0dc`
  - Updated: 2026-09-30
  - Issue: #25
  - Landing: `design/t-036-csdd-doctor` → `main`; PR #44
  - Verification: 19 unit tests PASS; `scripts/validate_repository.py` PASS; `git diff --check` clean. Scenarios 09–11 are pre-run contracts and have not been executed.
  - Note: README addition is a new diagnosis section. It does not edit the architecture or contributing links from T-034 and T-035. `/csdd status` is a separate workflow.

- [ ] T-034 — Formalize lightweight architecture and product-scope guardrails
  - Owner: valen
  - Agent: codex
  - Scope: `docs/architecture.md`, `README.md` architecture link
  - Target: `main`
  - Base: `4f8e43315e38d002f01ae2ccc869073e6be6166f`
  - Updated: 2026-09-30
  - Issue: #37
  - Landing: `codex/architecture-contribution-guardrails` → `main`; draft PR #43
  - Verification: 19 unit tests PASS; offline repository validator PASS; current skill, protocol, and templates unchanged.
  - Note: Contributor design policy only; current protocol contracts and #41/#42 solution choices remain unchanged. README edits are sequenced with T-035 by the same executor.

- [ ] T-035 — Add CSDD contribution guidance and a pull request template
  - Owner: valen
  - Agent: codex
  - Scope: `CONTRIBUTING.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `README.md` contribution link
  - Target: `main`
  - Base: `4f8e43315e38d002f01ae2ccc869073e6be6166f`
  - Updated: 2026-09-30
  - Issue: #20
  - Depends on: T-034 architecture guidance
  - Landing: `codex/architecture-contribution-guardrails` → `main`; draft PR #43
  - Verification: 19 unit tests PASS; offline repository validator PASS; documentation reviewed against protocol, CI, versioning, and evaluation contracts.
  - Note: Same-executor sequencing of the shared README; no new workflow or protocol behavior.

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

- [x] T-030 — Prepare and release CSDD v0.2.1 public beta
  - Owner: valen
  - Scope: released
  - Updated: 2026-09-27
  - Issue: #29
  - Landed: PR #38 @ `0279d53`; PR #39 @ `545a2ed`
  - Verification: 19 tests and structural validator PASS on release SHA; main push CI SUCCESS; isolated install lifecycle, Cursor/Codex init smokes, and 8-file installed runtime hash match PASS.
  - Note: Published `v0.2.1` as Latest at `545a2ed`; post-publication evidence in `evidence/t-030-release-readiness.md`. T-029 remains Deferred under DEC-006.

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
