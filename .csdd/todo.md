# TODO

## In Progress

## Ready to Land

- [ ] T-023 — Add real-world-derived v0.2 evaluation scenarios
  - Owner: valen
  - Agent: cursor-grok-4.5
  - Scope: evals/scenarios/06-git-divergence.md, evals/scenarios/07-landing-todo-handoff.md, evals/scenarios/08-existing-repo-init.md, evals/README.md, .csdd/todo.md, evals/scenarios/01-trivial-edit.md, evals/scenarios/02-session-resume.md, evals/scenarios/03-overlapping-scopes.md, evals/scenarios/04-stale-claim.md, evals/scenarios/05-phase-archive.md, evals/runs/01-trivial-edit.md, evals/runs/02-session-resume.md, evals/runs/03-overlapping-scopes.md, evals/runs/04-stale-claim.md, evals/runs/05-phase-archive.md, evals/runs/06-git-divergence-a.md, evals/runs/07-landing-todo-handoff-a.md, evals/runs/08-existing-repo-init-a.md, evals/results.md, .gitignore
  - Target: main
  - Base: 65b7ef68a8b7887a843ec535c490aa79b1e10f9e
  - Updated: 2026-07-21
  - Issue: #7
  - Note: Validate Git races, lifecycle truthfulness, TODO hygiene, handoff boundaries, and existing-repository initialization. Depends on T-022.
  - Landing: eval/t-023-v02-scenarios → main; PR pending
  - Verification: Scenarios 06–08 Run A passed; critical failures none; Run B not warranted; branch reconciled against current origin/main

## Blocked

## Pending

- [ ] T-024 — Prepare and release CSDD v0.2.0
  - Owner: valen
  - Note: Release only after migration documentation and v0.2 evaluations are complete.

## Deferred

## Recently Completed

Retention: 5

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
