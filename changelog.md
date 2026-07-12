# Changelog

All notable changes to CSDD will be documented in this file.

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

