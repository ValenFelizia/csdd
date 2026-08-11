# Changelog

All notable changes to CSDD will be documented in this file.

## [0.2.1] — 2026-08-11

### Added

- One-command global installation path for Codex and Cursor via the Agent
  Skills CLI, with a documented install / verify / update / uninstall lifecycle.
- Deterministic offline structural validator and unittest suite, wired into a
  least-privilege GitHub Actions workflow.
- Evidence-backed dimensional compatibility matrix for Codex and Cursor.
- Partial project-local Antigravity distribution path and evidence; discovery
  and behavioral dimensions remain not tested.
- Public-beta README onboarding polish covering install, Absent-only
  `/csdd init`, status, and non-guarantees.

### Changed

- No normative changes to the CSDD v0.2 protocol, skill runtime
  (`SKILL.md`, `references/**`, `assets/templates/**`), or document contracts.
- Upgrading from v0.2.0 does not require a migration.

### Known limitations

- CSDD remains an experimental public beta.
- The independent-user onboarding pilot (T-029 / #28) is deferred under
  DEC-006; zero external sessions were completed. Do not treat onboarding as
  externally validated.
- Compatibility remains dimensional: Global install and Discovery stay partial
  for Codex and Cursor; Implicit activation remains not tested.
- Antigravity support is limited to partial project-local installation evidence.
- CSDD does not provide shared runtime memory, distributed locking, or
  automatic synchronization.

## [0.2.0] — 2026-07-21

### Added

- Real-world Field Report 001 as the evidence source for the v0.2 milestone.
- Git-aware task lifecycle with truthful landing semantics (`Landing:`,
  `Verification:`, and `Landed:` only when reachable from `Target`).
- Six canonical TODO states, Ready-to-Land fields, and bounded Recently
  Completed retention.
- Boundary-driven, replaceable handoffs that exist only when a real execution
  boundary has concrete resumption risk.
- Explicit Absent-only `/csdd init` adoption workflow with mutually exclusive
  destination classification and pre-write revalidation.
- v0.2 primary templates (`specs.md`, `todo.md`, `decisions.md`, `handoff.md`)
  and a conservative v0.1 → v0.2 migration guide.
- Real-world-derived evaluation scenarios 06–08 covering Git divergence and
  live collision, landing/TODO/handoff truthfulness, and existing-repository
  initialization.

### Validated

- Scenarios 06–08 Run A all passed.
- No critical failures were found.
- Run B was not warranted under the T-023 campaign rule.

### Known limitations

- Evaluations remain manual.
- Harness and model coverage remains limited.
- Explicit invocation has more evidence than implicit activation.
- CSDD does not provide distributed locking, shared runtime memory, or
  automatic synchronization.

## [0.1.0] — 2026-07-12

### Added

- Initial CSDD protocol and operational skill.
- Canonical `.csdd/` document model.
- Adaptive hydration levels 0–3.
- Task ownership, agent, scope, overlap, and stale-claim semantics.
- Branch and worktree reconciliation rules.
- Truthful closure and completed-scope release.
- Semantic phase archival.
- Bootstrap templates.
- Manual evaluation scenarios and recorded runs.

### Validated

- Trivial fast-path execution.
- Session resume using durable project state.
- Overlapping-scope detection before editing.
- Evidence-based stale-agent reclamation.
- Human Owner preservation.
- Historical Agent preservation.
- Phase closure and semantic archive creation.



### Fixed during evaluation

- Prevented stale-agent reclamation from silently changing human ownership.
- Required completed tasks to release write scopes.
- Prevented phase-closing agents from overwriting historical executor metadata.
- Clarified canonical placement of behavioral requirements versus decisions.
- Added explicit branch/worktree reconciliation behavior.



### Known limitations

- Evaluations are currently manual.
- Harness and model coverage is limited.
- Explicit invocation has greater coverage than implicit activation.
- CSDD does not provide global locks or shared runtime memory.
