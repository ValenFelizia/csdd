# TODO

## In Progress

## Ready to Land

- [ ] T-036 — Add a read-only `/csdd doctor` workflow
  - Owner: valen
  - Agent: cursor-grok-4.7
  - Scope: `SKILL.md`, `references/protocol.md`, `references/document-contracts.md`, `references/read-only-workflows.md`, `README.md`, `changelog.md`, `evals/README.md`, `evals/scenarios/11-doctor-states.md`, `evals/scenarios/12-doctor-false-positives.md`, `evals/scenarios/13-doctor-visibility-limits.md`, `.csdd/todo.md`
  - Target: `main`
  - Base: `8f0b9f603ff2a75c7085906aa37f9f4584ad05dc`
  - Updated: 2026-10-06
  - Issue: #25
  - Landing: `design/t-036-csdd-doctor` → `main`; PR #44
  - Verification: 19 unit tests PASS; `scripts/validate_repository.py` PASS; `git diff --check` clean. Scenarios 11–13 are pre-run contracts and have not been executed.
  - Note: Rebased onto main after #46/#47. Doctor scenarios renumbered to 11–13. Finding severities and namespaced/duplicate ID checks are part of the doctor contract. `/csdd status` is a separate workflow.

- [ ] T-037 — Add a read-only `/csdd status` workflow
  - Owner: valen
  - Agent: cursor-grok-4.7
  - Scope: `SKILL.md`, `references/protocol.md`, `references/document-contracts.md`, `references/read-only-workflows.md`, `README.md`, `changelog.md`, `evals/README.md`, `evals/scenarios/14-status-snapshot.md`, `evals/scenarios/15-status-limits.md`, `.csdd/todo.md`
  - Target: `main`
  - Base: `245e826f207cf0cebd68170a464f162bca036155`
  - Updated: 2026-10-06
  - Issue: #26
  - Depends on: T-036
  - Landing: `design/t-037-csdd-status` → `main`; PR #45
  - Verification: 19 unit tests PASS; `scripts/validate_repository.py` PASS; `git diff --check` clean. Scenarios 14–15 are pre-run contracts and have not been executed.
  - Note: Stacked on rebased T-036. Status scenarios renumbered to 14–15. Derived snapshot only. Merge after #44.

- [ ] T-todo-integration-001 — Reduce shared TODO integration work with task-wise reconciliation
  - Owner: valen
  - Agent: codex
  - Scope: `SKILL.md`, `references/**` shared-state/landing guidance, `assets/templates/todo.md`, `README.md`, `changelog.md`, `docs/architecture.md`, `evals/**` scenario 10, `.csdd/specs.md`, `.csdd/decisions.md`
  - Target: `main`
  - Base: `cd2ff965385e743e9bc622229ebdf07db2faae32`
  - Updated: 2026-10-04
  - Issue: https://github.com/ValenFelizia/csdd/issues/42
  - Landing: Draft PR https://github.com/ValenFelizia/csdd/pull/47 from `codex/todo-task-reconciliation` to `main`; human review and target integration pending.
  - Verification: 19 unit tests, offline repository validation, and whitespace checks passed. Independent scenario 10: 13 PASS, 1 PARTIAL, zero FAIL; bounded metrics and the partial-case defect are recorded in `evals/runs/10-todo-integration-a.md`. CI results tracked on the PR.
  - Note: todo-integration coordinated for the human-approved #42 line; codex is the sole project-task allocator. Fixture author edits only scenario/materializer; subjects act only in disposable fixtures. Claims and waiting states remain visible; storage stays in four documents.

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

- [x] T-task-identity-001 — Implement stable local task identity with explicit namespaces
  - Owner: valen
  - Agent: codex
  - Scope: released
  - Updated: 2026-10-04
  - Issue: https://github.com/ValenFelizia/csdd/issues/41
  - Landed: PR #46 @ `cd2ff96`
  - Verification: Reviewed PR merged into main; 19 tests, offline validator, and final-head CI passed. Scenario 09: 9 independent subjects PASS.
  - Note: task-identity namespace remains reserved; evaluation limitations are in evals/runs/09-task-identity-a.md.

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
