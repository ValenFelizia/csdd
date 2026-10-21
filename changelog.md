# Changelog

All notable changes to CSDD will be documented in this file.

## [Unreleased]

## [0.3.0]

Prepared notes since v0.2.1. This version is not tagged in the commit that
adds these notes.

### Breaking

- Fresh `/csdd init` writes `specs.md`, `decisions.md`, and `handoff.md` only.
  `.csdd/todo.md` is opt-in through a whole-line phrase fence. A valid trio
  with that path absent is Current board-off. Doctor does not emit
  `docs.missing` for it and does not treat it as external mode. An empty
  local board still reports six counts of zero.
- `/csdd todo enable` is the only post-init writer, and only from Current
  board-off. The same shape is unchanged and is not recopied. A different
  shape, a stub field mismatch, or an invalid existing path is a refusal.
  Nothing deletes the file. Enable writes a blank template and does not
  resurrect task text. Restore a deleted board from Git instead of enabling
  over the restored file.
- Existing valid local boards and valid stubs stay valid. Do not delete them
  to match the new init default.

### Added

- Scenarios 18 and 19, with Run A for each. A session that is not running
  Poteto mode did not open the composition reference. An instructed delegation
  named `composer-2.5-fast` instead of the parent model. One Cursor subject
  each, at skill commit `a6ac88f`. The compatibility matrix is unchanged.
- Subagent model and effort fallback in `SKILL.md`. When CSDD is loaded and
  the harness can delegate, the child model matches the subtask. The parent
  is not inherited unless a harness, orchestrator, or project rule says so.
  No model catalog. Sessions that never load the skill are unchanged.
- Adaptive Poteto-mode composition. The skill loads
  `references/poteto-composition.md` only when the current session is running
  Poteto mode. Other sessions do not load it and do not change claims,
  handoffs, hydration, or initialization. On board-off or a stub, that
  session does not create `.csdd/todo.md` to hold `Agent`.
- Claude Code distribution docs: personal `~/.claude/skills/csdd/` and project
  `.claude/skills/csdd/` install via Agent Skills CLI (`--agent claude-code`)
  and manual copy/clone/symlink; README Supported agents section; T-033
  distribution evidence. Discovery and behavior remain not tested.
- Opt-in task surfaces at `.csdd/todo.md`: a six-heading local board and an
  external stub (`Mode: external`, `Tracker:`, `Next:`). Package templates
  stay `assets/templates/todo.md` and `assets/templates/todo.external.md`.
  Mixed shapes stay malformed. Scenarios 16–17, 20, and 21 are the new
  contracts. Scenarios 16–17 and 20–21 are unexecuted.
- Compatible local task-ID convention with explicitly coordinated bounded
  namespaces, optional external issue relationships, and duplicate repair.
- Offline identity fixtures and a qualitative evaluation scenario.
- Shared-state write economy and task-wise landing reconciliation, with
  visible claims and waiting states and combined retention after verified
  landing.
- Reproducible offline integration fixtures comparing the baseline, each
  change separately, and their combination, with separate safety cases.
- Read-only `/csdd doctor` workflow for diagnosing CSDD state without writing,
  repairing, or migrating. Structural TODO checks reuse the repository
  validator's heading and retention rules on a local board. Evaluation
  contracts are scenarios 11–13 and have not been executed.
- Read-only `/csdd status` workflow that derives a brief operational snapshot
  from canonical documents and observable Git state. It does not persist a
  status file. Current briefs include `task surface:`. Evaluation contracts
  are scenarios 14–15 and have not been executed.

### Migration

- To opt in, put a fence line in the init utterance, or run
  `/csdd todo enable` later on Current board-off. A recognizable v0.1
  `todo.md` is still transformed in place. It is not deleted.

### Adoption

- No release is published with these notes.
- Existing IDs remain valid. No renumbering, fifth primary document, tracker
  sync service, or runtime service is required. Valid local boards and valid
  stubs need no migration. Parallel-integration guidance does not create
  `todo.md`. Savings remain workload-dependent.

## [0.2.1] — 2026-09-27

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
