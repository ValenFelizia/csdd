# TODO

## In Progress

- [ ] T-task-identity-001 — Implement stable local task identity with explicit namespaces
  - Owner: valen
  - Agent: codex
  - Scope: `SKILL.md`, `references/**` identity guidance, `assets/templates/todo.md`, `docs/architecture.md` identity link, `README.md`, `changelog.md`, `evals/**` identity campaign, `.csdd/specs.md`, `.csdd/decisions.md`
  - Target: `main`
  - Base: `d30eb30b8f19292fe10ae8cc64d65bd22832e0dc`
  - Updated: 2026-10-03
  - Issue: https://github.com/ValenFelizia/csdd/issues/41
  - Note: task-identity allocation to codex for the human-approved #41 line. Fixture author owns only evals/fixtures/task_identity.py and evals/scenarios/09-task-identity.md; subjects write only disposable fixtures. #42 remains separate.

## Ready to Land

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

- [x] T-035 — Add CSDD contribution guidance and a pull request template
  - Owner: valen
  - Agent: codex
  - Scope: released
  - Updated: 2026-10-03
  - Issue: #20
  - Landed: PR #43 @ `d30eb30`
  - Note: Contribution guide, impact matrix, and PR template reachable from main; historical executor preserved.

- [x] T-034 — Formalize lightweight architecture and product-scope guardrails
  - Owner: valen
  - Agent: codex
  - Scope: released
  - Updated: 2026-10-03
  - Issue: #37
  - Landed: PR #43 @ `d30eb30`
  - Note: Canonical contributor architecture guidance reachable from main; no runtime change in that PR.

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
